import datetime

from sqlalchemy.orm import defer, joinedload

from src import models
from src.auth.hashing.hash import hash_password, verify_password
from src.base_service.base_service import BaseService

from sqlalchemy import or_, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from src.config import jwt_config


class UserService(BaseService):
    def get_entity_name(self):
        return "User"

    async def get_entities(self, session: AsyncSession, offset: int = None, limit: int = None, search: str = None):
        """
        Get all entities except password field
        """
        try:
            query = select(self.model)
            length_query = select(func.count(self.model.id))

            # join district, city, region, country
            query = query.options(
                joinedload(self.model.district).joinedload(models.District.city).
                joinedload(models.City.region).joinedload(models.Region.country)
            )

            # join gender, status, device
            query = query.options(
                joinedload(self.model.gender),
                joinedload(self.model.status)
            )

            if search:
                query = query.where(
                    (self.model.deleted_at == None).options(
                        defer(self.model.password)
                    ),
                    or_(
                        func.lower(self.model.username).contains(search.lower()),
                        func.lower(self.model.phone_number).contains(search.lower()),
                        func.lower(self.model.address).contains(search.lower())
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
        pass

    async def create_entity(self, entity_data, session: AsyncSession):
        """
        Create entity
        """
        try:
            password = entity_data.password
            print(password)
            hashed_password = hash_password(password, jwt_config.SECRET_KEY)
            print(hashed_password)
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

    async def delete_entity(self, entity_id: int, session: AsyncSession):
        """
        Delete entity by id
        """
        try:
            query = select(self.model).where(self.model.id == entity_id, self.model.deleted_at == None)
            entity = (await session.execute(query)).scalars().first()
            if entity is None:
                raise HTTPException(status_code=404, detail=f"{self.get_entity_name()} not found")
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

    async def get_authenticate_user(self, phone_number: str, password: str, session: AsyncSession):
        """
        Authenticate user
        """
        try:
            query = select(self.model).where(
                self.model.phone_number == phone_number, self.model.deleted_at == None)
            user = (await session.execute(query)).scalars().first()
            print('user', user.password)
            if user is None:
                raise HTTPException(status_code=404, detail=f"{self.get_entity_name()} not found")
            print('is ver', verify_password(password, jwt_config.SECRET_KEY, user.password))
            if not verify_password(password, jwt_config.SECRET_KEY, user.password):
                raise HTTPException(status_code=400, detail=f"{self.get_entity_name()} password is incorrect")
            return {
                "status": "success",
                "detail": f"{self.get_entity_name()} authenticated successfully" if user else f"{self.get_entity_name()} not authenticated",
                "data": user
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
