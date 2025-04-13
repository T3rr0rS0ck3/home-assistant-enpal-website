
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_URL
from .const import DOMAIN, DEFAULT_NAME, DEFAULT_URL, DEFAULT_SCAN_INTERVAL

CONF_SCAN_INTERVAL = "scan_interval"
CONF_GROUPS = "groups"

GROUP_OPTIONS = ["Site Data", "Battery", "IoTEdgeDevice", "Inverter", "PowerSensor", "Unknown"]

class EnpalWebsiteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_URL, default=DEFAULT_URL): str,
                vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int
            })
        )

    async def async_step_import(self, user_input=None):
        return await self.async_step_user(user_input)

class EnpalWebsiteOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input,
                options={
                    CONF_URL: user_input[CONF_URL],
                    CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
                }
            )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(CONF_URL, default=self.config_entry.data.get(CONF_URL, DEFAULT_URL)): str,
                vol.Optional(CONF_SCAN_INTERVAL, default=self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)): int
            })
        )
