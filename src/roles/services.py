from typing import Optional

from fastapi import HTTPException
from sqlalchemy import insert, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.roles import schemas


class RoleService:

    @staticmethod
    async def get_roles(session: AsyncSession):
        """
        Get all roles
        """
        try:
            query = select(models.Role)
            return {
                "status": "success",
                "detail": "Roles retrieved successfully",
                "data": (await session.execute(query)).scalars().all()
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "detail": "Roles not retrieved",
                "data": str(e) if str(e) else None
            })

    @staticmethod
    async def get_role(role_id: int, session: AsyncSession):
        """
        Get role by id
        """
        try:
            query = select(models.Role).where(models.Role.id == role_id)
            role = (await session.execute(query)).scalars().first()
            if role is None:
                raise HTTPException(status_code=404, detail="Role not found")
            return {
                "status": "success",
                "detail": "Role retrieved successfully",
                "data": role
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
                "detail": "Role not retrieved",
                "data": str(e) if str(e) else None
            })

    @staticmethod
    async def create_role(role: schemas.RoleCreate, session: AsyncSession):
        """
        Create role
        """
        try:
            role_db = models.Role(**role.dict())
            session.add(role_db)
            await session.commit()
            return {
                "status": "success",
                "detail": "Role created successfully",
                "data": role_db
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "detail": "Role not created",
                "data": str(e) if str(e) else None
            })

    @staticmethod
    async def update_role(role_id: int, role: schemas.RoleCreate, session: AsyncSession):
        """
        Update role by id
        """
        try:
            query = select(models.Role).where(models.Role.id == role_id)
            role_db = (await session.execute(query)).scalars().first()
            if role_db is None:
                raise HTTPException(status_code=404, detail="Role not found")
            for key, value in role.dict().items():
                if value is not None:
                    setattr(role_db, key, value)
            await session.commit()
            return {
                "status": "success",
                "detail": "Role updated successfully",
                "data": role_db
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
                "detail": "Role not updated",
                "data": str(e) if str(e) else None
            })

    @staticmethod
    async def delete_role(role_id: int, session: AsyncSession):
        """
        Delete role by id
        """
        try:
            query = select(models.Role).where(models.Role.id == role_id)
            role = (await session.execute(query)).scalars().first()
            if role is None:
                raise HTTPException(status_code=404, detail="Role not found")
            await session.delete(role)
            await session.commit()
            return {
                "status": "success",
                "detail": "Role deleted successfully",
                "data": role
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
                "detail": "Role not deleted",
                "data": str(e) if str(e) else None
            })

    @staticmethod
    async def get_role_permissions(role_id: int, session: AsyncSession):
        """
        Get role permissions
        """
        try:
            permission_ids = (await session.execute(
                select(models.role_permission.c.permission_id).where(models.role_permission.c.role_id == role_id)
            )).scalars().all()
            query = select(models.Permission.alias).where(models.Permission.id.in_(permission_ids))

            return (await session.execute(query)).scalars().all()
        except Exception as e:
            raise HTTPException(status_code=400, detail="Permissions not retrieved")
