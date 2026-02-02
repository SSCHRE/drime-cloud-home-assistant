from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

class DrimeNotesSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Drime Notes"

    @property
    def native_value(self):
        data = self.coordinator.data if self.coordinator.data else []
        return len(data)

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data if self.coordinator.data else []
        for note in data:
            note["url"] = f"https://app.drime.cloud/notes/{note['id']}/edit"
        return {"notes": data}

    @property
    def native_unit_of_measurement(self):
        return None


class DrimeNotesCountSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Drime Notes Count"

    @property
    def native_value(self):
        notes_data = self.coordinator.data if self.coordinator.data else []
        return len(notes_data)
