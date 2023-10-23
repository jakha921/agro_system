import datetime

import boto3
import magic
from sqlalchemy.orm import joinedload

from src import models
from src.base_service.base_service import BaseService

from sqlalchemy import or_, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

# region AWS S3
# create a session with AWS using boto3 library in IAM user
session = boto3.Session(
    aws_access_key_id="AKIAQLSZYWF72GE6SHWL",
    aws_secret_access_key="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",
)

KB = 1024
MB = 1024 * KB

SUPPORTED_FILE_TYPES = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/gif": "gif"
}

AWS_BUCKET = "agro-project-media"
s3 = session.resource("s3")
bucket = s3.Bucket(AWS_BUCKET)


async def s3_upload(contents: bytes, key: str):
    print(f"Uploading to S3")
    bucket.put_object(Key=key, Body=contents)


async def upload_file(file):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    contents = await file.read()
    file_size = len(contents)

    if not 0 < file_size < 10 * MB:
        raise HTTPException(status_code=400, detail="File size is too large or too small (0 < file_size < 10 MB)")

    file_type = magic.from_buffer(buffer=contents, mime=True)
    if file_type not in SUPPORTED_FILE_TYPES:
        raise HTTPException(status_code=400, detail=f"File type {file_type} is not supported")

    # save to S3 bucket with photo
    print("file is ", file.filename.split(".")[0])
    file_name = f"{file.filename.split('.')[0]}.{SUPPORTED_FILE_TYPES[file_type]}"
    await s3_upload(contents=contents, key=file_name)

    #     get the url of the image
    return f"https://{AWS_BUCKET}.s3.amazonaws.com/{file_name}"


# endregion

class ComplainService(BaseService):
    def get_entity_name(self):
        return "Complain"

    async def get_entity_by_name(self, entity_name: str, session: AsyncSession):
        """
        Get entity by name
        """
        pass

    async def get_entities(self, session: AsyncSession, offset: int = None, limit: int = None, search: str = None):
        """
        Get all entities
        """
        try:
            query = select(self.model)

            length_query = select(func.count(self.model.id))

            query = query.options(joinedload(self.model.complain_status))
            query = query.options(joinedload(self.model.users))

            if self.model.action_district:
                query = query.options(joinedload(self.model.action_district).
                                      joinedload(models.District.city).
                                      joinedload(models.City.region).
                                      joinedload(models.Region.country)
                                      )

            if self.model.action_city:
                query = query.options(joinedload(self.model.action_city).
                                      joinedload(models.City.region).
                                      joinedload(models.Region.country)
                                      )

            if search:
                query = query.where(
                    or_(
                        func.lower(self.model.title).contains(search.lower()),
                        func.lower(self.model.description).contains(search.lower())
                    )
                )

            if offset and limit:
                query = query.offset((offset - 1) * limit).limit(limit)

            query = query.order_by(self.model.created_at.desc())

            return {
                "status": "success",
                "detail": f"{self.get_entity_name()} retrieved successfully",
                "data": {
                    "total": (await session.execute(length_query)).scalar(),
                    "items": (await session.execute(query)).scalars().all()
                }
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "detail": f"{self.get_entity_name()} not retrieved",
                "data": str(e) if str(e) else None
            })

    async def get_entity(self, entity_id: int, session: AsyncSession):
        """
        Get entity by id
        """
        try:
            query = select(self.model)

            # if in keys of model exists {some_name}_id then joined load model name for get module.
            if self.get_addition_entity_name():
                query = query.options(self.get_addition_entity_name())

            query = query.where(self.model.id == entity_id)
            entity = (await session.execute(query)).scalars().first()

            if entity is None:
                raise HTTPException(status_code=404, detail=f"{self.get_entity_name()} not found")
            return {
                "status": "success",
                "detail": f"{self.get_entity_name()} retrieved successfully",
                "data": entity
            }
        except HTTPException as e:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "detail": e.detail,
                "data": None
            })
        except Exception as e:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "detail": f"{self.get_entity_name()} not retrieved",
                "data": str(e) if str(e) else None
            })

    async def create_entity(self, entity_data, session: AsyncSession):
        """
        Create entity
        """
        try:
            entity = self.model(**entity_data.dict())
            session.add(entity)
            await session.commit()
            return {
                "status": "success",
                "detail": f"{self.get_entity_name()} created successfully",
                "data": entity
            }
        except HTTPException as e:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "detail": e.detail,
                "data": None
            })
        except Exception as e:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "detail": f"{self.get_entity_name()} not created",
                "data": str(e) if str(e) else None
            })

    async def update_entity(self, entity_id: int, entity_data, session: AsyncSession):
        """
        Update entity by id
        """
        try:
            query = select(self.model).where(self.model.id == entity_id)
            entity = (await session.execute(query)).scalars().first()
            if entity is None:
                raise HTTPException(status_code=404, detail=f"{self.get_entity_name()} not found")
            for key, value in entity_data.dict().items():
                if value is not None:
                    setattr(entity, key, value)
            await session.commit()
            return {
                "status": "success",
                "detail": f"{self.get_entity_name()} updated successfully",
                "data": entity
            }
        except HTTPException as e:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "detail": e.detail,
                "data": None
            })
        except Exception as e:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "detail": f"{self.get_entity_name()} not updated",
                "data": str(e) if str(e) else None
            })

    async def delete_entity(self, entity_id: int, session: AsyncSession):
        """
        Delete entity by id
        """
        try:
            query = select(self.model).where(self.model.id == entity_id)
            entity = (await session.execute(query)).scalars().first()
            if entity is None:
                raise HTTPException(status_code=404, detail=f"{self.get_entity_name()} not found")

            # set deleted_at field to current timestamp
            setattr(entity, "deleted_at", datetime.datetime.utcnow())
            await session.commit()
            return {
                "status": "success",
                "detail": f"{self.get_entity_name()} deleted successfully",
                "data": entity
            }
        except HTTPException as e:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "detail": e.detail,
                "data": None
            })
        except Exception as e:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "detail": f"{self.get_entity_name()} not deleted",
                "data": str(e) if str(e) else None
            })
