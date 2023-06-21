from typing import Optional
from fastapi import HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src import models
from src.base_service.base_service import BaseService


class CountryService(BaseService):
    def get_entity_name(self):
        return "Country"

    async def delete_entity(self, entity_id: int, session: AsyncSession):
        """
        Delete entity by id
        """
        try:
            # get by country id exists in cities
            cities_query = select(models.Region).where(models.Region.country_id == entity_id)
            cities = (await session.execute(cities_query)).scalars().all()
            if cities:
                raise HTTPException(status_code=400,
                                    detail=f"Country has cities {[city.name_ru for city in cities]}")

            query = select(self.model).where(self.model.id == entity_id)
            entity = (await session.execute(query)).scalars().first()
            if entity is None:
                raise HTTPException(status_code=404, detail=f"{self.get_entity_name()} not found")
            await session.delete(entity)
            await session.commit()
            return {
                "status": "success",
                "detail": f"{self.get_entity_name()} deleted successfully",
                "data": None
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

    async def get_country_by_name(self, country_name: str, session: AsyncSession):
        """
        Get country by name
        """
        try:
            query = select(models.Country).where(
                models.Country.name_ru.lower() == country_name.lower() or
                models.Country.name_en.lower() == country_name.lower() or
                models.Country.name_uz.lower() == country_name.lower()
            )

            country = (await session.execute(query)).scalars().first()
            if country is None:
                raise HTTPException(status_code=404, detail="Country not found")
            return {
                "status": "success",
                "detail": "Country retrieved successfully",
                "data": country
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
                "detail": "Country not retrieved",
                "data": str(e) if str(e) else None
            })

    async def get_countries_by_obj(self, session: AsyncSession):
        """
        Get all countries
        """
        try:
            # select all countries left join regions left join cities left join districts
            query = select(models.Country).options(
                selectinload(models.Country.regions).options(
                    selectinload(models.Region.cities).options(
                        selectinload(models.City.districts)
                    )
                )
            )

            countries = (await session.execute(query)).scalars().all()
            return {
                "status": "success",
                "detail": "Countries retrieved successfully",
                "data": countries
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "detail": "Countries not retrieved",
                "data": str(e) if str(e) else None
            })
