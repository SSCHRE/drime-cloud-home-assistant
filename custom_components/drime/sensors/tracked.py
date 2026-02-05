from homeassistant.components.sensor import SensorEntity

class DrimeTrackedFilesSensor(SensorEntity):
    _attr_name = "Drime Tracked Files"
    _attr_icon = "mdi:file-multiple"

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_unique_id = "drime_files_overview"

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def native_value(self):
        files = self.coordinator.data.get("pagination", {}).get("data", [])
        return len(files)

    @property
    def extra_state_attributes(self):
        files_raw = self.coordinator.data.get("pagination", {}).get("data", [])

        # Compose list of files with wanted properties
        files = [
            {
                "id": f["id"],
                "name": f["name"],
                "type": f.get("type"),
                "file_size": f.get("file_size"),
                "views": f.get("views_number"),
                "downloads": f.get("dl_number"),
            }
            for f in files_raw
        ]

        files.sort(key=lambda f: f["name"].lower())

        # Fetch a fixed 50 items
        return {
            "files": files,
            "per_page": 50,
        }
