"""
=========================================================
SmartCooler Main Application

Author : Aditya Choudhary
Platform : Arch Linux
Python : 3.12+

Description:
Main entry point for the SmartCooler daemon.

Responsibilities:
- Load configuration
- Initialize logger
- Initialize sensor manager
- Initialize serial manager
- Initialize fan controller
- Run the monitoring loop

All business logic lives in the individual modules.
=========================================================
"""

from time import sleep
from config import Config
from logger import LoggerManager
from sensor_manager import SensorManager
from serial_manager import SerialManager
from fan_controller import FanController


class SmartCooler:
    """
    Main SmartCooler application.
    Coordinates all project modules.
    """

    def __init__(self):

        # -------------------------
        # Load configuration
        # -------------------------
        self.config = Config()

        # -------------------------
        # Logger
        # -------------------------
        self.logger = LoggerManager(self.config)

        # -------------------------
        # Temperature Sensors
        # -------------------------
        self.sensor_manager = SensorManager(
            self.config,
            self.logger
        )

        # -------------------------
        # Arduino Serial
        # -------------------------
        self.serial_manager = SerialManager(
            self.config,
            self.logger
        )

        # -------------------------
        # Fan Controller
        # -------------------------
        self.fan_controller = FanController(
            self.config,
            self.serial_manager,
            self.logger
        )

        self.logger.info("SmartCooler initialized successfully.")

    def run(self):
        """
        Main monitoring loop.
        """

        self.logger.info("Starting SmartCooler monitoring loop.")

        while True:

            try:

                # ----------------------------------
                # Read temperatures
                # ----------------------------------

                cpu_temp = self.sensor_manager.get_cpu_temperature()
                gpu_temp = self.sensor_manager.get_gpu_temperature()

                # ----------------------------------
                # Fan decision
                # ----------------------------------

                self.fan_controller.update(
                    cpu_temp=cpu_temp,
                    gpu_temp=gpu_temp
                )

                # ----------------------------------
                # Logging
                # ----------------------------------

                self.logger.log_temperature(
                    cpu_temp,
                    gpu_temp,
                    self.fan_controller.current_state
                )

            except KeyboardInterrupt:

                self.logger.info("Stopping SmartCooler.")
                break

            except Exception as error:

                self.logger.error(
                    f"Unexpected error: {error}"
                )

            sleep(self.config.poll_interval)


def main():

    app = SmartCooler()

    app.run()


if __name__ == "__main__":
    main()
