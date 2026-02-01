import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_API_KEY

VALIDATION_URL = "https://app.drime.cloud/api/v1/cli/loggedUser"


class CannotConnect(HomeAssistantError):
    """Cannot connect to Drime Cloud API."""


class InvalidAuth(HomeAssistantError):
    """Cannot authenticate using provided API key."""


class DrimeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            api_key = user_input[CONF_API_KEY]

            try:
                await self._validate_api_key(api_key)
                return self.async_create_entry(
                    title="Drime Cloud",
                    data={CONF_API_KEY: api_key},
                )

            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except CannotConnect:
                errors["base"] = "cannot_connect"

        schema = vol.Schema(
            {vol.Required(CONF_API_KEY): str}
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    async def _validate_api_key(self, api_key: str) -> None:
        session = async_get_clientsession(self.hass)
        headers = {"Authorization": f"Bearer {api_key}"}

        try:
            async with async_timeout.timeout(10):
                async with session.get(VALIDATION_URL, headers=headers) as resp:

                    # Serverside error
                    if resp.status >= 500:
                        raise CannotConnect

                    # Invalid api key or expired
                    if resp.status in (401, 403):
                        raise InvalidAuth

                    resp.raise_for_status()
                    data = await resp.json()

                    # Call API to verify if API key is valid (user != null)
                    if data.get("user") is None:
                        raise InvalidAuth

        except InvalidAuth:
            raise
        except aiohttp.ClientError:
            raise CannotConnect
        except Exception:
            raise CannotConnect