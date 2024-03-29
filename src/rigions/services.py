from sqlalchemy.orm import joinedload

from src.base_service.base_service import BaseService


class RegionService(BaseService):
    def get_entity_name(self):
        return "Region"

    def get_addition_entity_name(self):
        return joinedload(self.model.country)