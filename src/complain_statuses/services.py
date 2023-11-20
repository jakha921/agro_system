from fastapi import HTTPException
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.base_service.base_service import BaseService


class ComplainStatusService(BaseService):
    def get_entity_name(self):
        return "ComplainStatus"

    async def get_entities(self, session: AsyncSession, offset: int = None, limit: int = None, search: str = None,
                           lang: str = None):
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
                        func.lower(self.model.name_ru).contains(search.lower()),
                        func.lower(self.model.name_en).contains(search.lower()),
                        func.lower(self.model.name_uz).contains(search.lower())
                    )
                )
            if offset and limit:
                query = query.offset((offset - 1) * limit).limit(limit)

            # Sort by title column by chosen language
            if lang:
                query = query.order_by(getattr(self.model, f"name_{lang}").asc())

            result = (await session.execute(query)).unique().scalars().all()

            if lang:
                result = [
                    {
                        "id": item.id,
                        "name": getattr(item, f"name_{lang}"),
                        "description": item.description
                    } for item in result
                ]

            return {
                "status": "success",
                "detail": f"{self.get_entity_name()} retrieved successfully",
                "data": {
                    "total": (await session.execute(length_query)).scalar(),
                    "items": result
                }
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "detail": f"{self.get_entity_name()} not retrieved",
                "data": str(e) if str(e) else None
            })
