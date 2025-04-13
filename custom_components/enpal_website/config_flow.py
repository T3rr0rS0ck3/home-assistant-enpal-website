
import voluptuous as vol
from typing import Any
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_URL
from .const import DOMAIN, DEFAULT_NAME, DEFAULT_URL, DEFAULT_SCAN_INTERVAL

CONF_SCAN_INTERVAL = "scan_interval"

class EnpalWebsiteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    reconfigure_support = True

    def __init__(self):
        self._data = {}

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            self._data = user_input
            await self.async_set_unique_id(user_input.get(CONF_NAME, "enpal"))
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_URL, default=DEFAULT_URL): str,
                vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
            })
        )

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        entry = self._get_reconfigure_entry()

        if user_input is not None:
            return self.async_update_reload_and_abort(
                entry,
                data_updates={
                    CONF_URL: user_input[CONF_URL],
                    CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
                },
            )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema({
                vol.Required(CONF_URL, default=entry.data.get(CONF_URL, DEFAULT_URL)): str,
                vol.Required(CONF_SCAN_INTERVAL, default=entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)): int,
            })
        )
