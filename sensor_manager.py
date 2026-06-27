"""
=========================================================
SmartCooler - Sensor Manager

Reads CPU and GPU temperatures directly from Linux.

Priority:
1. /sys/class/hwmon
2. lm_sensors (fallback)

Designed for Arch Linux.
=========================================================
"""

from pathlib import Path
import subprocess
from typing import Optional


class SensorManager:

    CPU_KEYWORDS = (
        "k10temp",          # AMD
        "coretemp",         # Intel
        "zenpower",
        "cpu"
    )

    GPU_KEYWORDS = (
        "amdgpu",
        "radeon",
        "nouveau",
        "nvidia",
        "gpu"
    )

    def __init__(self, config, logger):

        self.config = config
        self.logger = logger

        self.cpu_sensor = self._find_cpu_sensor()
        self.gpu_sensor = self._find_gpu_sensor()

        if self.cpu_sensor:
            self.logger.info(f"CPU sensor: {self.cpu_sensor}")

        if self.gpu_sensor:
            self.logger.info(f"GPU sensor: {self.gpu_sensor}")

    # -----------------------------------------------------

    def _find_sensor(self, keywords):

        hwmon_root = Path("/sys/class/hwmon")

        if not hwmon_root.exists():
            return None

        for hwmon in hwmon_root.iterdir():

            name_file = hwmon / "name"

            if not name_file.exists():
                continue

            try:
                name = name_file.read_text().strip().lower()
            except Exception:
                continue

            if any(keyword in name for keyword in keywords):

                for temp in sorted(hwmon.glob("temp*_input")):
                    return temp

        return None

    # -----------------------------------------------------

    def _find_cpu_sensor(self):

        return self._find_sensor(self.CPU_KEYWORDS)

    # -----------------------------------------------------

    def _find_gpu_sensor(self):

        return self._find_sensor(self.GPU_KEYWORDS)

    # -----------------------------------------------------

    def _read_hwmon(self, sensor: Optional[Path]) -> Optional[float]:

        if sensor is None:
            return None

        try:

            value = int(sensor.read_text().strip())

            return round(value / 1000.0, 1)

        except Exception:

            return None

    # -----------------------------------------------------

    def _fallback_lm_sensors(self):

        try:

            output = subprocess.check_output(
                ["sensors"],
                text=True
            )

            for line in output.splitlines():

                if "°C" not in line:
                    continue

                if "+" in line:

                    start = line.find("+") + 1
                    end = line.find("°")

                    value = float(line[start:end])

                    return value

        except Exception:

            return None

        return None

    # -----------------------------------------------------

    def get_cpu_temperature(self) -> Optional[float]:

        temp = self._read_hwmon(self.cpu_sensor)

        if temp is not None:
            return temp

        return self._fallback_lm_sensors()

    # -----------------------------------------------------

    def get_gpu_temperature(self) -> Optional[float]:

        return self._read_hwmon(self.gpu_sensor)
