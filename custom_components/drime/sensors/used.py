from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from ..coordinator import DrimeDataCoordinator

class DrimeUsedSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Drime Used Space"
        self._attr_unique_id = "drime_used_space"

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
