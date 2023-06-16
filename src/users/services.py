from src.auth.hashing.hash import hash_password
from src.base_service.base_service import BaseService

from sqlalchemy import or_, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException


class UserService(BaseService):
    def get_entity_name(self):
        return "User"

    async def get_entities(self, session: AsyncSession):
        """
        Get all entities except password field
        """
        try:
            query = select(self.model)
            return {
                "status": "success",
                "detail": f"{self.get_entity_name()} retrieved successfully",
                "data": (await session.execute(query)).scalars().all()
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
        pass

    async def create_entity(self, entity_data, session: AsyncSession):
        """
        Create entity
        """
        try:
            password = entity_data.password
            print(password)
            salt, hashed_password = hash_password(password)
            entity_data.password = hashed_password
            print(entity_data.password)
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
