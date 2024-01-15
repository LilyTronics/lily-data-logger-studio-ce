"""
Instrument model for the multimeter simulator
"""

import lily_unit_test

from src.models.instrument import Instrument


simulator_multimeter = Instrument({
    'name': 'Simulator multimeter',
    'info': 'Read random values for voltage (4.9...5.1V) and current (0.39...0.41)'
})


class TestSimulatorMultimeter(lily_unit_test.TestSuite):

    def test_properties(self):
        self.fail_if(simulator_multimeter.get_name() != 'Simulator multimeter',
                     'The name is not correct {}'.format(simulator_multimeter.get_name()))
        self.fail_if(simulator_multimeter.get_info() == simulator_multimeter.DEFAULT_INFO,
                     'The info has the default value')


if __name__ == '__main__':

    TestSimulatorMultimeter().run()
