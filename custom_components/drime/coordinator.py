import aiohttp
import asyncio
import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)
UPDATE_INTERVAL = timedelta(minutes=5)

class DrimeDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api_key, api_url):
        super().__init__(
            hass,
            _LOGGER,
            name=f"Drime Data: {api_url}",
            update_interval=UPDATE_INTERVAL,
        )
        self.api_key = api_key
        self.api_url = api_url
        self.data = {}

    async def _async_update_data(self):
        session = async_get_clientsession(self.hass)
        headers = {"Authorization": f"Bearer {self.api_key}"}
        timeout = aiohttp.ClientTimeout(total=10)

        try:
            async with session.get(self.api_url, headers=headers, timeout=timeout) as resp:
                resp.raise_for_status()
                data = await resp.json()

                if isinstance(data, dict):
                    if data.get("status") != "success":
                        _LOGGER.warning("Drime API error response: %s, keeping old data", data)
                        return self.data
                elif isinstance(data, list):
                    return data

                return data

        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            _LOGGER.warning("Drime API request failed: %s, keeping old data", err)
            return self.data
