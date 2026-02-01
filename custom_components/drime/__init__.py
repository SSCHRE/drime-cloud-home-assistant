from .const import DOMAIN, PLATFORMS, CONF_API_KEY

async def async_setup_entry(hass, entry):
    api_key = entry.data[CONF_API_KEY]

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = api_key

    await hass.config_entries.async_forward_entry_setups(
        entry, PLATFORMS
    )

    return True
