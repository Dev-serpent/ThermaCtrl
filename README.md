# ❄️ SmartCooler

<div align="center">

### Intelligent External Laptop Cooling System for Arch Linux + Arduino

Automatically monitors your laptop's temperature and controls a high-power external cooling fan using an Arduino.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Arduino](https://img.shields.io/badge/Arduino-Compatible-00979D?logo=arduino)
![Linux](https://img.shields.io/badge/Arch%20Linux-Supported-1793D1?logo=arch-linux)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 📖 Overview

SmartCooler is a lightweight Python application that continuously monitors your laptop's **CPU** and **GPU** temperatures on **Arch Linux**. When the system gets hot, it automatically tells an **Arduino** to switch on an external cooling fan. Once the temperature drops, the fan is turned off using configurable hysteresis.

Designed with reliability in mind, SmartCooler automatically reconnects to the Arduino, detects sensors, logs events, and starts automatically at boot using **systemd**.

---

## ✨ Features

* 🌡️ Automatic CPU & GPU temperature monitoring
* 🔍 Reads sensors directly from `/sys/class/hwmon`
* 🖥️ AMD & Intel CPU support
* 🎮 AMD GPU support (when available)
* 🔄 Configurable hysteresis (default: ON 65°C / OFF 55°C)
* 🔌 Automatic Arduino USB detection
* ♻️ Automatic serial reconnection
* 📜 Rotating log files
* ⚙️ JSON configuration
* 🚀 systemd auto-start
* 🧩 Modular architecture for future expansion

---

## 🏗️ Architecture

```text
Laptop Sensors
      │
      ▼
Python Application
      │
      ▼
Temperature Logic
      │
      ▼
USB Serial
      │
      ▼
Arduino
      │
      ▼
MOSFET / Relay
      │
      ▼
External Cooling Fan
```

---

## 📂 Project Structure

```text
SmartCooler/
├── arduino/
│   └── SmartCooler.ino
│
├── python/
│   ├── main.py
│   ├── sensor_manager.py
│   ├── serial_manager.py
│   ├── fan_controller.py
│   ├── config.py
│   └── logger.py
│
├── config/
│   └── config.json
│
├── service/
│   └── smartcooler.service
│
├── docs/
├── logs/
├── install.sh
├── requirements.txt
└── README.md
```

---

# 🔧 Hardware Setup

## Components

* Arduino Uno / Nano
* Logic-Level N-Channel MOSFET (Recommended: IRLZ44N)
* Flyback Diode (1N4007 or similar)
* External Cooling Fan
* External Power Supply
* USB Cable
* Connecting Wires

### Wiring Diagram

```text
               Laptop
                  │
             USB Cable
                  │
                  ▼
          +----------------+
          |    Arduino     |
          |                |
          | D8 ─────────────── Gate
          | GND─────────────── GND
          +----------------+
                     │
                     ▼
              N-Channel MOSFET
                     │
        +------------+------------+
        |                         |
 External PSU (+)             External PSU (-)
        |                         |
        |                     MOSFET Source
        |
      Cooling Fan
        |
        +---------------------------+
                                    |
                              MOSFET Drain

Flyback Diode:
Cathode → Fan +
Anode   → Fan -
```

> **Important:** The Arduino **must not power the fan directly**. The fan should always use its own external power supply.

---

# 💻 Software Setup

## 1. Install Dependencies

```bash
sudo pacman -Syu

sudo pacman -S python python-pip python-pyserial lm_sensors git
```

Detect available sensors:

```bash
sudo sensors-detect

sensors
```

---

## 2. Clone the Repository

```bash
git clone https://github.com/<your-username>/SmartCooler.git

cd SmartCooler
```

---

## 3. Install

```bash
chmod +x install.sh

./install.sh
```

The installer will:

* Install Python dependencies
* Create configuration files
* Create log directory
* Install systemd service

---

## ⚙️ Configuration

Edit:

```text
config/config.json
```

Example:

```json
{
    "temperature": {
        "fan_on": 65,
        "fan_off": 55,
        "poll_interval": 1
    }
}
```

---

## ▶️ Running

Run manually:

```bash
python python/main.py
```

Enable automatic startup:

```bash
sudo systemctl enable smartcooler.service

sudo systemctl start smartcooler.service
```

Check service status:

```bash
systemctl status smartcooler.service
```

Live logs:

```bash
journalctl -u smartcooler.service -f
```

---

## 📜 Logging

Logs are stored in:

```text
~/SmartCooler/logs/
```

Each log entry includes:

* Timestamp
* CPU Temperature
* GPU Temperature
* Fan State
* Serial Connection Status
* Errors & Warnings

---

## 🛣️ Roadmap

* ✅ Automatic Arduino detection
* ✅ Automatic sensor detection
* ⏳ PWM fan speed control
* ⏳ OLED display
* ⏳ RGB status LEDs
* ⏳ Desktop GUI
* ⏳ Web Dashboard
* ⏳ Telegram & Discord notifications
* ⏳ Temperature graphs
* ⏳ Multiple fan support
* ⏳ AI-based fan prediction

---

## 🤝 Contributing

Contributions, suggestions, and bug reports are always welcome. Feel free to fork the project, open issues, or submit pull requests.

---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a star!

Made with ❤️ for Linux and hardware enthusiasts.

</div>
