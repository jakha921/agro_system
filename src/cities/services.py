from src.base_service.base_service import BaseService


class CityService(BaseService):
    def get_entity_name(self):
        return "City"

    def get_addition_entity_name(self):
        return self.model.region
