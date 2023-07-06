from sqlalchemy import func, or_
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.strategy_options import defer

from src import models
from src.base_service.base_service import BaseService

from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


class DepartmentService(BaseService):
    def get_entity_name(self):
        return "Department"

    def get_addition_entity_name(self):
        return joinedload(models.Department.city).joinedload(models.City.region).joinedload(models.Region.country)

    async def get_entities(self, session: AsyncSession, offset: int = None, limit: int = None, search: str = None):
        """
        Get all entities
        """
        try:
            query = select(self.model)

            length_query = select(func.count(self.model.id))

            # join district, city, region, country
            query = query.options(self.get_addition_entity_name())

            if search:
                query = query.where(
                    or_(
                        func.lower(self.model.title_ru).contains(search.lower()),
                        func.lower(self.model.title_en).contains(search.lower()),
                        func.lower(self.model.title_uz).contains(search.lower()),
                        func.lower(self.model.phone_number).contains(search.lower()),
                        func.lower(self.model.address).contains(search.lower())
                    )
                )
            if offset and limit:
                query = query.offset((offset - 1) * limit).limit(limit)

            # remove phone numbers
            query = query.options(defer(self.model.phone_number))

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

    async def get_entity_by_name(self, entity_name: str, session: AsyncSession):
        """
        Get entity by name
        """
        try:
            query = select(self.model).where(
                func.lower(self.model.title_ru) == entity_name.lower(),
            )
            entity = (await session.execute(query)).scalars().first()
            return {
                "status": "success",
                "detail": f"{self.get_entity_name()} retrieved successfully" if entity else f"{self.get_entity_name()} not found",
                "data": entity if entity else None
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

            # if in keys of model exists {some_name}_id then joined load model name for get module.
            if self.get_addition_entity_name():
                query = query.options(self.get_addition_entity_name())

            # join district if exists
            if self.model.district_id:
                query = query.options(joinedload(models.Department.district))

            query = query.where(self.model.id == entity_id)
            entity = (await session.execute(query)).scalars().first()
            entity.phone_number = entity.phone_number.split(',') if entity.phone_number else []

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
            get_entity = await self.get_entity_by_name(entity_data.title_ru, session)
            if get_entity["status"] == "success" and get_entity["data"] is not None:
                raise HTTPException(status_code=400, detail=f"{self.get_entity_name()} already exists")

            entity = self.model(**entity_data.dict())
            entity.phone_number = \
                str(entity_data.phone_number).replace(' ', '').replace('[', '').replace(']', '').replace("'", '')
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
            get_entity = await self.get_entity_by_name(entity_data.title_ru, session)
            if get_entity["status"] == "success" and get_entity["data"] is not None and get_entity[
                "data"].id != entity_id:
                raise HTTPException(status_code=400, detail=f"{self.get_entity_name()} already exists")

            query = select(self.model).where(self.model.id == entity_id)
            entity = (await session.execute(query)).scalars().first()
            if entity is None:
                raise HTTPException(status_code=404, detail=f"{self.get_entity_name()} not found")

            entity_data.phone_number = \
                str(entity_data.phone_number).replace(' ', '').replace('[', '').replace(']', '').replace("'", '')

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
