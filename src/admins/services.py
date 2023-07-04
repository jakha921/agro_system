import datetime

from sqlalchemy.orm import defer, joinedload

from src import models
from src.auth.hashing import hash_password, verify_password
from src.base_service.base_service import BaseService

from sqlalchemy import or_, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from src.config import jwt_config


class AdminService(BaseService):
    def get_entity_name(self):
        return "Admin"

    async def get_entities(self, session: AsyncSession, offset: int = None, limit: int = None, search: str = None):
        """
        Get all entities except password field
        """
        try:
            query = select(self.model)
            length_query = select(func.count(self.model.id))

            query = query.options(joinedload(self.model.role))

            if search:
                query = query.where(
                    or_(
                        func.lower(self.model.username).contains(search.lower()),
                        func.lower(self.model.email).contains(search.lower())
                    ),
                )

            if offset and limit:
                query = query.offset((offset - 1) * limit).limit(limit)

            # remove password field
            query = query.options(defer(self.model.password))

            return {
                "status": "success",
                "detail": f"{self.get_entity_name()} retrieved successfully",
                "data": {
                    "total": (await session.execute(length_query)).scalar(),
                    "data": (await session.execute(query)).scalars().all()
                }
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "detail": f"{self.get_entity_name()} not retrieved",
                "data": str(e) if str(e) else None
            })

    async def get_entity_by_email(self, entity_name: str, session: AsyncSession):
        """
        Get entity by name
        """
        try:
            query = select(self.model).where(self.model.email == entity_name)
            entity = (await session.execute(query)).scalars().first()
            # if entity is None:
            #     raise HTTPException(status_code=404, detail=f"{self.get_entity_name()} not found")
            return {
                "status": "success",
                "detail": f"{self.get_entity_name()} retrieved successfully",
                "data": entity if entity is not None else None
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

    async def get_entity(self, entity_id: int, session: AsyncSession):
        """
        Get entity by id
        """
        try:
            query = select(self.model)

            query = query.options(joinedload(self.model.role))

            query = query.where(self.model.id == entity_id)
            entity = (await session.execute(query)).scalars().first()

            # exclude password field
            entity.password = None

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
            get_entity = await self.get_entity_by_email(entity_data.email, session)
            print('get_entity', get_entity)
            if get_entity["status"] == "success" and get_entity["data"]:
                raise HTTPException(status_code=400,
                                    detail=f"{self.get_entity_name()} with {entity_data.email} already exists")

            entity_data.password = hash_password(entity_data.password, jwt_config.SECRET_KEY)
            entity = self.model(**entity_data.dict())
            session.add(entity)
            await session.commit()

            # remove password field
            entity.password = None
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
            get_entity = await self.get_entity_by_email(entity_data.email, session)
            if get_entity["status"] == "success" and get_entity["data"] is not None and get_entity[
                "data"].id != entity_id:
                raise HTTPException(status_code=400, detail=f"{self.get_entity_name()} already exists")

            query = select(self.model).where(self.model.id == entity_id)
            entity = (await session.execute(query)).scalars().first()
            if entity is None:
                raise HTTPException(status_code=404, detail=f"{self.get_entity_name()} not found")

            print('entity_data', entity_data)
            if entity_data.password:
                hashed_password = hash_password(entity_data.password, jwt_config.SECRET_KEY)
                entity_data.password = hashed_password
                print('hashed_password', hashed_password)
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

    async def delete_entity(self, entity_ids: list[int], session: AsyncSession):
        """
        Delete entity by id
        """
        try:
            deleted = []
            for entity_id in entity_ids:
                query = select(self.model).where(self.model.id == entity_id)
                entity = (await session.execute(query)).scalars().first()
                if entity is None:
                    raise HTTPException(status_code=404, detail=f"{self.get_entity_name()} not found")
                if entity.email == "admin@gmail.com":
                    raise HTTPException(status_code=404, detail="Admin with admin@gmail.com email can't be deleted")
                await session.delete(entity)
                await session.commit()
                deleted.append(entity)
            return {
                "status": "success",
                "detail": f"{self.get_entity_name()} deleted successfully",
                "data": deleted
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

    async def get_authenticate_admin(self, email: str, password: str, session: AsyncSession):
        """
        Authenticate user
        """
        try:
            query = select(self.model).where(self.model.email == email)
            entity = (await session.execute(query)).scalars().first()
            if entity is None:
                raise HTTPException(status_code=404, detail=f"{self.get_entity_name()} not found")
            if not verify_password(password, jwt_config.SECRET_KEY, entity.password):
                raise HTTPException(status_code=404, detail="Incorrect password")
            return {
                "status": "success",
                "detail": f"{self.get_entity_name()} authenticated successfully",
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
                "detail": f"{self.get_entity_name()} not authenticated",
                "data": str(e) if str(e) else None
            })
