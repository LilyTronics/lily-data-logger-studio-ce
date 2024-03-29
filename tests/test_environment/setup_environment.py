"""
Script that runs before all tests to set up the environment
"""

import glob
import os
import shutil

from src.app_data import AppData
from src.models.list_serial_ports import get_available_serial_ports
from tests.test_environment.check_arduino_daq import get_arduino_daq_serial_port
from tests.test_environment.check_serial_loopback import get_serial_loopback_port


def clear_reports(report_path):
    print(f"Clear report path: {report_path}")
    for item in os.listdir(report_path):
        full_path = os.path.join(report_path, item)
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            raise Exception(f"ERROR: could not remove item '{item}'")


def check_for_instruments(skip_instruments=False):
    if skip_instruments:
        exclude_tests = [
            "TestSerialPortInterface",
            "TestArduinoDAQ"
        ]
    else:
        exclude_tests = []
        print("Detect available serial ports")
        serial_ports = get_available_serial_ports()
        print(f"Available ports: {serial_ports}")
        if get_serial_loopback_port(serial_ports) is None:
            exclude_tests.append("TestSerialPortInterface")
        if get_arduino_daq_serial_port(serial_ports) is None:
            exclude_tests.append("TestArduinoDAQ")

    return exclude_tests


def setup_user_folder():
    ignore_files = [
        os.path.join(AppData.USER_FOLDER, "LilyDataLoggerStudioCE.json"),
        os.path.join(AppData.USER_FOLDER, "LilyDataLoggerStudioCE.log")
    ]
    matches = list(filter(lambda x: x not in ignore_files,
                          glob.glob(os.path.join(AppData.USER_FOLDER, "*.*"))))
    for item in matches:
        print(f"Delete {item}")
        os.unlink(item)


if __name__ == "__main__":

    clear_reports("..\\test_reports")
    print("Exclude:", check_for_instruments())
