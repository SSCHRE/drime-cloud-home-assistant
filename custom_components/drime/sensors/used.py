from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from ..coordinator import DrimeDataCoordinator

API_URL = "https://app.drime.cloud/api/v1/user/space-usage"

class DrimeUsedSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, hass, api_key):
        coordinator = DrimeDataCoordinator(hass, api_key, API_URL)
        super().__init__(coordinator)
        self._attr_name = "Drime Used Space"

    @property
    def native_value(self):
        data = self.coordinator.data
        used_bytes = data.get("used")
        if used_bytes is None:
            return None
        return round(used_bytes / (1024**3), 2)

    @property
    def native_unit_of_measurement(self):
        return "GB"
