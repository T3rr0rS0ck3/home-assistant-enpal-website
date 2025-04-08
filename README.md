# Enpal Website Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Install%20this%20integration-blue?style=for-the-badge&logo=home-assistant)](https://github.com/T3rr0rS0ck3/home-assistant-enpal-website)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge&logo=home-assistant)](https://github.com/T3rr0rS0ck3/home-assistant-enpal-website)

This custom integration fetches and parses sensor data from a local Enpal inverter/battery HTML dashboard and exposes it as sensors in Home Assistant.

---

## 🌟 Features

- Parses data from `http://192.168.X.X/deviceMessages`
- Supports Config Flow (no YAML required)
- Sensor auto-discovery with unit detection (°C, %, kWh, etc.)
- Icon support for battery, CPU, temperature, voltage, etc.
- Customizable polling interval
- Select which data groups to include (e.g. Battery, Site Data)
- HACS compatible

---

## 📦 Installation (via HACS)

1. Go to **HACS → Integrations → ⋮ → Custom repositories**
2. Add this repository URL:
   ```
   https://github.com/T3rr0rS0ck3/home-assistant-enpal-website
   ```
   and select "Integration" as category.
3. Install "Enpal Website"
4. Restart Home Assistant
5. Add the integration via **Settings → Devices & Services → Add Integration**

---

## ⚙️ Configuration

All configuration is done via the UI:

- Enter your Enpal IP address (e.g., `http://192.168.X.X/deviceMessages`)
- Set polling interval in seconds (e.g., 60)
- Select which sensor groups to monitor (Battery, Inverter, etc.)

You can change these later via the **⚙️ Configure** button in the integration.

---

## 🧪 Supported Units & Icons

| Type       | Unit  | Icon              |
|------------|-------|-------------------|
| Power      | W     | `mdi:lightning-bolt` |
| Energy     | kWh   | `mdi:transmission-tower` |
| Temperature| °C    | `mdi:thermometer` |
| Voltage    | V     | `mdi:flash`       |
| Current    | A     | `mdi:current-dc`  |
| CPU Load   | %     | `mdi:cpu-64-bit`  |
| Battery    | %     | `mdi:battery`     |

---

## 📄 Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history.

---

## 📜 License

MIT License

---

Made with ❤️ by [@T3rr0rS0ck3](https://github.com/T3rr0rS0ck3)
