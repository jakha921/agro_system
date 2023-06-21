from fastapi import APIRouter, Depends
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models import Department
from src.departments import schemas
from src.departments.services import DepartmentService

router = APIRouter(
    prefix="/departments",
    tags=["departments"],
    # responses={404: {"description": "Not found"}},
)
department_service = DepartmentService(Department)


@router.get("/")
async def get_departments(page: int = None, per_page: int = None, search: str = None,
                          session: AsyncSession = Depends(get_async_session)):
    return await department_service.get_entities(session, page, per_page, search)


@router.post("/")
async def create_department(department: schemas.DepartmentCreate, session: AsyncSession = Depends(get_async_session)):
    return await department_service.create_entity(department, session)


@router.get("/{department_id}")
async def get_department(department_id: int, session: AsyncSession = Depends(get_async_session)):
    return await department_service.get_entity(department_id, session)


@router.patch("/{department_id}")
async def update_department(department_id: int, department: schemas.DepartmentUpdate,
                          session: AsyncSession = Depends(get_async_session)):
    return await department_service.update_entity(department_id, department, session)


@router.delete("/{department_id}")
async def delete_department(department_id: int, session: AsyncSession = Depends(get_async_session)):
    return await department_service.delete_entity(department_id, session)
