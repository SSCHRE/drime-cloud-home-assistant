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
USAGE_API_URL = "https://app.drime.cloud/api/v1/user/space-usage"
NOTES_API_URL = "https://app.drime.cloud/api/v1/notes"
FILES_API_URL = "https://app.drime.cloud/api/v1/track/all?perPage=50"

async def async_setup_entry(hass, config_entry, async_add_entities):
    api_key = config_entry.data[CONF_API_KEY]

    usage_coordinator = DrimeDataCoordinator(hass, api_key, USAGE_API_URL)
    await usage_coordinator.async_config_entry_first_refresh()

    notes_coordinator = DrimeDataCoordinator(hass, api_key, NOTES_API_URL)
    await notes_coordinator.async_config_entry_first_refresh()

    tracked_files_coordinator = DrimeDataCoordinator(hass, api_key, FILES_API_URL)
    await tracked_files_coordinator.async_config_entry_first_refresh()

    sensors = [
        DrimeUsedSensor(usage_coordinator),
        DrimeAvailableSensor(usage_coordinator),
        DrimeTotalSensor(usage_coordinator),
        DrimeUsagePercentageSensor(usage_coordinator),
        DrimeNotesSensor(notes_coordinator),
        DrimeNotesCountSensor(notes_coordinator),
        DrimeTrackedFilesSensor(tracked_files_coordinator)
    ]
    async_add_entities(sensors, True)
