from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from ..coordinator import DrimeDataCoordinator

API_URL = "https://app.drime.cloud/api/v1/user/space-usage"

class DrimeAvailableSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, hass, api_key):
        coordinator = DrimeDataCoordinator(hass, api_key, API_URL)
        super().__init__(coordinator)
        self._attr_name = "Drime Available Space"

    @property
    def native_value(self):
        data = self.coordinator.data
        total_bytes = data.get("available")
        used_bytes = data.get("used")
        if total_bytes is None or used_bytes is None:
            return None
        available = total_bytes - used_bytes

        return round(available / (1024**3), 2)

    @property
    def native_unit_of_measurement(self):
        return "GB"
