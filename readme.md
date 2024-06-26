# Lily Data Logger Studio CE (Community Edition)

Universal data logger software aiming to work with any kind of electronics measurement devices
(multimeters, oscilloscopes, power supplies, etc.).

![main view](docs/images/main_view.png)

## Releases

We are excited to announce that we have released the first official release V1.0.

Download the packages at: https://www.lilytronics.nl/lily-data-logger-studio

The manual can be found here: https://lily-data-logger-studio-ce.readthedocs.io

Unfortunately Windows Defender sees our software as a threat. We can guaranty that this is not the issue.
To use the software you need to add it as exception to the Windows Defender.
We are looking into this to solve this in a more elegant way.

## Features

* Logging data (measurements) in a table.
* Free and open source for personal and professional use.
* Build in drivers for the following instruments:
  * Arduino DAQ: reading analog voltages, reading and writing digital IO. A sketch for the Arduino
    is included.
  * Multimeter simulator giving random values for voltage and current, for testing measurements.
* Fixed end time or continuous measurement.
* Smallest sample interval: 1 second.
* Adding your own instrument drivers (see manual)
* Data from the table can be copied and pasted to a spreadsheet (Excel, LibreOffice, etc.).
* Export to CSV for using data in other applications (databases, scripting, etc.).
* OS compatibility:
  * Developed and tested primarily for Windows 10/11.
  * Tested on Ubuntu (22.04 LTS version).
  * Not tested on MAC.

## About GPIB...

We get some questions if GPIB will be supported. GPIB is a standardized communication bus for instruments.
But the standardization is only on the GPIB part. The command and response structure are standardized.
What is not standardized is the GPIB PC controller. In the past PCs used ISA cards. 
Nowadays, you need to have a USB to GPIB controller. And in this controller lies the problem. 
Supporting the GPIB protocol is fairly easy. Supporting all available GPIB controllers on the market
is a headache. Every GPIB controller requires its own specific driver. And to test it, we need a 
sample of each controller available. And those controllers are not cheap. So for now it is not very 
feasible to have GPIB supported. But... if someone is willing to donate a GPIB controller, we will 
be happy to add support for it.

Some GPIB controllers are using a virtual com port. Those controllers might work using the
serial port interface. We say might work, because it has not been tested.

## Adding your own instruments

You can add your own instruments. A manual for that will be available on the first release.

## Development

Requirements for running the software:

* Python 3.10 (Ubuntu 22.04 LTS has Python 3.10)
* Upgrade pip: python -m pip install --upgrade pip
* pip install -r requirements.txt

Ubuntu:

* For installing wxPython you require the following packages:
  * `sudo apt install python3-dev`
  * `sudo apt install libgtk-3-dev`
* To use serial ports, you need to add the user to the dialout group:
  * `sudo adduser <username> dialout`
  * Log out and log in to make the change effective.

In `tests` is are several scripts for running the unit tests.
Test reports are written to `unit_test/test_reports`.

[![Documentation Status](https://readthedocs.org/projects/lily-data-logger-studio-ce/badge/?version=latest)](https://lily-data-logger-studio-ce.readthedocs.io/en/latest/?badge=latest)

2024 - LilyTronics (https://lilytronics.nl)
