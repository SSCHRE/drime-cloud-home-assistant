from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from ..coordinator import DrimeDataCoordinator

API_URL = "https://app.drime.cloud/api/v1/user/space-usage"

class DrimeUsagePercentageSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, hass, api_key):
        coordinator = DrimeDataCoordinator(hass, api_key, API_URL)
        super().__init__(coordinator)
        self._attr_name = "Drime Usage Percentage"

    @property
    def native_value(self):
        data = self.coordinator.data
        used = data.get("used")
        available = data.get("available")
        if used is None or available is None:
            return None
        return round((used / available) * 100, 2)

    @property
    def native_unit_of_measurement(self):
        return "%"
