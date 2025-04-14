
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME, CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from bs4 import BeautifulSoup
import async_timeout
from datetime import timedelta
import logging
import re

_LOGGER = logging.getLogger(__name__)

CONF_SCAN_INTERVAL = "scan_interval"
CONF_GROUPS = "groups"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    name = entry.data[CONF_NAME]
    url = entry.options.get(CONF_URL, entry.data.get(CONF_URL))
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, 60))
    selected_groups = entry.options.get(CONF_GROUPS, [])

    session = async_get_clientsession(hass)

    async def fetch_data():
        try:
            async with async_timeout.timeout(10):
                response = await session.get(url)
                text = await response.text()
                return parse_html(text, selected_groups)
        except Exception as e:
            _LOGGER.error(f"Fehler beim Abrufen der Seite: {e}")
            return []

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="enpal_website",
        update_method=fetch_data,
        update_interval=timedelta(seconds=scan_interval),
    )

    await coordinator.async_config_entry_first_refresh()

    sensors = [
        EnpalWebsiteSensor(coordinator, key, group)
        for (key, _, group) in coordinator.data
    ]

    async_add_entities(sensors, True)

def parse_html(html, selected_groups):
    soup = BeautifulSoup(html, "html.parser")
    data = []
    cards = soup.find_all("div", class_="card")
    for card in cards:
        header = card.find("h2")
        group = header.get_text(strip=True) if header else "Unknown"
        if selected_groups and group not in selected_groups:
            continue
        rows = card.find_all("tr")
        for row in rows:
            columns = row.find_all("td")
            if len(columns) >= 2:
                key = columns[0].get_text(strip=True).replace(".", "_").replace(" ", "_")
                value = columns[1].get_text(strip=True)
                data.append((key, value, group))
                _LOGGER.warning(f"Key: {key}, Value: {value}, Group: {group}")
    return data

def detect_unit(value):
    _LOGGER.debug(f"Detecting unit for value: {value}")
    if re.search(r"\d+\.?\d*\s*kWh", value):
        return "kWh"
    if re.search(r"\d+\.?\d*\s*Wh", value):
        return "Wh"
    if re.search(r"\d+\.?\d*\s*W", value):
        return "W"
    if re.search(r"\d+\.?\d*\s*V", value):
        return "V"
    if re.search(r"\d+\.?\d*\s*A", value):
        return "A"
    if re.search(r"\d+\.?\d*\s*%", value):
        return "%"
    if re.search(r"°C", value) or re.search(r"\d+\.?\d*\s*C", value):
        return "°C"
    if re.search(r"\d+\.?\d*\s*Hz", value):
        return "Hz"
    return None

def extract_numeric(value):
    match = re.search(r"[-+]?\d*\.?\d+", value.replace(",", "."))
    if match:
        try:
            return float(match.group())
        except ValueError:
            return value
    return value

def detect_icon(key):
    key = key.lower()
    if "temperature" in key:
        return "mdi:thermometer"
    if "voltage" in key:
        return "mdi:flash"
    if "current" in key or "amper" in key:
        return "mdi:current-dc"
    if "power" in key:
        return "mdi:lightning-bolt"
    if "battery" in key:
        return "mdi:battery"
    if "cpu" in key:
        return "mdi:cpu-64-bit"
    if "memory" in key:
        return "mdi:memory"
    if "load" in key:
        return "mdi:gauge"
    return "mdi:information-outline"

class EnpalWebsiteSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, key, group):
        super().__init__(coordinator)
        self._key = key
        self._group = group
        self._attr_name = f"{group} {key}"
        self._attr_unique_id = f"{group.lower().replace(' ', '_')}_{key.lower()}"
        self._attr_device_info = {
            "identifiers": {(f"{group.lower()}_group",)},
            "name": group,
            "manufacturer": "Enpal",
            "model": "HTML Sensor",
        }

    @property
    def state(self):
        for (key, value, group) in self.coordinator.data:
            if key == self._key and group == self._group:
                return extract_numeric(value)
        return None

    @property
    def native_unit_of_measurement(self):
        for (key, value, group) in self.coordinator.data:
            if key == self._key and group == self._group:
                return detect_unit(value)
        return None

    @property
    def state_class(self):
        unit = self.native_unit_of_measurement
        if unit in ["kWh", "Wh"]:
            if self._key.endswith("_day"):
                return "total"
            if self._key.endswith("_lifetime"):
                return "total_increasing"
            return "total_increasing"
        elif unit in ["W", "V", "A", "%", "°C", "Hz"]:
            return "measurement"
        return None

    @property
    def last_reset(self):
        if self.state_class == "total":
            # dynamisch: Mitternacht heute
            now = datetime.now(timezone.utc)
            return datetime.combine(now.date(), time.min, tzinfo=timezone.utc)
        return None

    @property
    def device_class(self):
        key = self._key.lower()
        if "temperature" in key:
            return "temperature"
        if "voltage" in key:
            return "voltage"
        if "current" in key or "amper" in key:
            return "current"
        if "power" in key:
            return "power"
        if "energy" in key:
            return "energy"
        if "humidity" in key:
            return "humidity"
        if "battery" in key:
            return "battery"
        if "frequency" in key or "hz" in key:
            return "frequency"
        if "duration" in key:
            return "duration"
        return None

    @property
    def icon(self):
        return detect_icon(self._key)
