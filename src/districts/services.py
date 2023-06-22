from sqlalchemy.orm import joinedload

from src import models
from src.base_service.base_service import BaseService


class DistrictService(BaseService):
    def get_entity_name(self):
        return "District"

    def get_addition_entity_name(self):
        return joinedload(self.model.city). \
            joinedload(models.City.region). \
            joinedload(models.Region.country)
