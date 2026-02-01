import aiohttp
import asyncio
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import logging
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)
UPDATE_INTERVAL = timedelta(minutes=10)

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
                if resp.status >= 500:
                    _LOGGER.warning("Drime API server error %s, keeping old data", resp.status)
                    return self.data

                resp.raise_for_status()
                data = await resp.json()

                if data.get("status") != "success":
                    _LOGGER.warning("Drime API error response: %s, keeping old data", data)
                    return self.data

                return data

        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            _LOGGER.warning("Drime API request failed: %s, keeping old data", err)
            return self.data