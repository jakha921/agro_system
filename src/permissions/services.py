import asyncio

from sqlalchemy.orm import joinedload

from src import models
from src.base_service.base_service import BaseService

from sqlalchemy import or_, func, delete, insert
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException


class PermissionService(BaseService):
    def get_entity_name(self):
        return 'Permission'

    async def get_entities(self, session: AsyncSession, offset: int = None, limit: int = None, search: str = None):
        """
        Get all entities
        """
        try:
            query = select(self.model).options(
                joinedload(self.model.role)
            ).join(self.model.role)

            length_query = select(func.count(self.model.id))

            if search:
                query = query.where(
                    or_(
                        func.lower(self.model.name_ru).contains(search.lower()),
                        func.lower(self.model.name_en).contains(search.lower()),
                        func.lower(self.model.name_uz).contains(search.lower()),
                        func.lower(self.model.description).contains(search.lower()),
                        func.lower(self.model.alias).contains(search.lower())
                    )
                )
            if offset and limit:
                query = query.offset((offset - 1) * limit).limit(limit)

            return {
                "status": "success",
                "detail": f"{self.get_entity_name()} retrieved successfully",
                "data": {
                    "total": (await session.execute(length_query)).scalar(),
                    "items": (await session.execute(query)).unique().scalars().all()
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
            query = select(self.model).options(
                joinedload(self.model.role)
            ).join(self.model.role)

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

    async def get_entity_by_name(self, entity_name: str, session: AsyncSession):
        """
        Get entity by name
        """
        try:
            query = select(self.model).where(
                or_(
                    func.lower(self.model.alias) == func.lower(entity_name),
                    func.lower(self.model.name_ru) == func.lower(entity_name),
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
            get_entity = await self.get_entity_by_name(entity_data.alias, session)
            if get_entity["status"] == "success" and get_entity["data"] is not None:
                raise HTTPException(status_code=400, detail=f"{self.get_entity_name()} already exists")

            # from schema to model pop category_ids and create entity
            role_ids = entity_data.role_ids

            # except category_ids
            entity = self.model(**entity_data.dict(exclude={"role_ids"}))

            # Получаем категории по id
            role = await session.execute(select(models.Role).where(models.Role.id.in_(role_ids)))
            role = role.scalars().all()

            if len(role_ids) != len(role):
                raise HTTPException(status_code=404, detail=f"Category not found")

            # Добавляем категории в право
            entity.role.extend(role)

            print('entity', entity)
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
            for key, value in entity_data.dict(exclude={"role_ids"}).items():
                if value is not None:
                    setattr(entity, key, value)

            # Remove all categories from entity and add new categories
            await session.execute(delete(models.category_right).where(models.category_right.c.right_id == entity_id))

            # Get role by id
            role_ids = entity_data.role_ids
            role = await session.execute(select(models.Role).where(models.Role.id.in_(role_ids)))
            role = role.scalars().all()

            if len(role_ids) != len(role):
                raise HTTPException(status_code=404, detail=f"Category not found")

            # Add a role to permission
            entity.role.extend(role)

            session.add(entity)
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
