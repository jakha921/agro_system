from src.base_service.base_service import BaseService

from sqlalchemy import or_, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException


class CategoryService(BaseService):
    def get_entity_name(self):
        return "Category"

    async def get_entities(self, session: AsyncSession, offset: int = None, limit: int = None, search: str = None):
        """
        Get all entities
        """
        try:
            query = select(self.model)

            length_query = select(func.count(self.model.id))

            # if in keys of model exists {some_name}_id then joined load model name for get module.
            if self.get_addition_entity_name():
                query = query.options(self.get_addition_entity_name())

            if search:
                query = query.where(
                    or_(
                        func.lower(self.model.title_ru).contains(search.lower()),
                        func.lower(self.model.title_en).contains(search.lower()),
                        func.lower(self.model.title_uz).contains(search.lower()),
                        func.lower(self.model.short_description_ru).contains(search.lower()),
                        func.lower(self.model.short_description_en).contains(search.lower()),
                        func.lower(self.model.short_description_uz).contains(search.lower())
                    )
                )
            if offset and limit:
                query = query.offset((offset - 1) * limit).limit(limit)

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
                or_(
                    func.lower(self.model.title_ru) == func.lower(entity_name),
                    func.lower(self.model.short_description_ru) == func.lower(entity_name),
                )
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

    async def create_entity(self, entity_data, session: AsyncSession):
        """
        Create entity
        """
        try:
            get_entity = await self.get_entity_by_name(entity_data.title_ru, session)
            if get_entity["status"] == "success" and get_entity["data"] is not None:
                raise HTTPException(status_code=400, detail=f"{self.get_entity_name()} already exists")

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
            get_entity = await self.get_entity_by_name(entity_data.title_ru, session)
            if get_entity["status"] == "success" and get_entity["data"] is not None:
                raise HTTPException(status_code=400, detail=f"{self.get_entity_name()} already exists")

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
