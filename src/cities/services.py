from sqlalchemy.orm import joinedload

from src import models
from src.base_service.base_service import BaseService


class CityService(BaseService):
    def get_entity_name(self):
        return "City"

    def get_addition_entity_name(self):
        return joinedload(self.model.region). \
            joinedload(models.Region.country)
