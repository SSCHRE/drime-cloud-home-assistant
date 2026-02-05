import logging
from .sensors.used import DrimeUsedSensor
from .sensors.available import DrimeAvailableSensor
from .sensors.total import DrimeTotalSensor
from .sensors.usage_percentage import DrimeUsagePercentageSensor
from .sensors.notes import DrimeNotesSensor, DrimeNotesCountSensor
from .sensors.tracked import DrimeTrackedFilesSensor
from .coordinator import DrimeDataCoordinator
from .const import CONF_API_KEY

_LOGGER = logging.getLogger(__name__)
NOTES_API_URL = "https://app.drime.cloud/api/v1/notes"
FILES_API_URL = "https://app.drime.cloud/api/v1/track/all?perPage=50"

async def async_setup_entry(hass, config_entry, async_add_entities):
    api_key = config_entry.data[CONF_API_KEY]

    notes_coordinator = DrimeDataCoordinator(hass, api_key, NOTES_API_URL)
    await notes_coordinator.async_config_entry_first_refresh()

    tracked_files_coordinator = DrimeDataCoordinator(hass, api_key, FILES_API_URL)
    await tracked_files_coordinator.async_config_entry_first_refresh()

    sensors = [
        DrimeUsedSensor(hass, api_key),
        DrimeAvailableSensor(hass, api_key),
        DrimeTotalSensor(hass, api_key),
        DrimeUsagePercentageSensor(hass, api_key),
        DrimeNotesSensor(notes_coordinator),
        DrimeNotesCountSensor(notes_coordinator),
        DrimeTrackedFilesSensor(files_coordinator)
    ]
    async_add_entities(sensors, True)
