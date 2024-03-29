"""
Container for simulator settings.
"""


class SimulatorSettings:

    class MultimeterUdp:
        IP = "localhost"
        PORT = 17000
        RX_TIME_OUT = 0.2

    class TemperatureMeterTcp:
        IP = "localhost"
        PORT = 17100
        RX_TIME_OUT = 0.2
