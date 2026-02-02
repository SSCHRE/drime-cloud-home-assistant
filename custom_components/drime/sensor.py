import logging
from .sensors.used import DrimeUsedSensor
from .sensors.available import DrimeAvailableSensor
from .sensors.usage_percentage import DrimeUsagePercentageSensor
from .const import CONF_API_KEY

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    api_key = config_entry.data[CONF_API_KEY]

    sensors = [
        DrimeUsedSensor(hass, api_key),
        DrimeAvailableSensor(hass, api_key),
        DrimeTotalSensor(hass, api_key),
        DrimeUsagePercentageSensor(hass, api_key)
    ]
    async_add_entities(sensors, True)
