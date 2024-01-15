"""
Instrument model.
"""

import lily_unit_test


class Instrument(object):

    KEY_CHANNELS = 'channels'
    KEY_INFO = 'info'
    KEY_INTERFACE = 'interface'
    KEY_NAME = 'name'
    KEY_TYPE = 'type'

    DEFAULT_NAME = 'unknown'
    DEFAULT_INFO = 'no info'

    def __init__(self, instrument_definition):
        self._name = instrument_definition.get(self.KEY_NAME, self.DEFAULT_NAME)
        self._info = instrument_definition.get(self.KEY_INFO, self.DEFAULT_INFO)
        self._interface = instrument_definition.get(self.KEY_INTERFACE, {})
        self._channels = instrument_definition.get(self.KEY_CHANNELS, {})

    ##########
    # Public #
    ##########

    def get_name(self):
        return self._name

    def get_info(self):
        return self._info

    def get_interface_type(self):
        return self._interface.get(self.KEY_TYPE, None)


class TestInstrument(lily_unit_test.TestSuite):

    def test_default_values(self):
        instrument = Instrument({})
        self.fail_if(instrument.get_name() != instrument.DEFAULT_NAME,
                     'The default name is not correct {}'.format(instrument.get_name()))
        self.fail_if(instrument.get_info() != instrument.DEFAULT_INFO,
                     'The default info is not correct {}'.format(instrument.get_info()))
        self.fail_if(instrument.get_interface_type() is not None,
                     'The default interface type is not correct {}'.format(instrument.get_interface_type()))


if __name__ == '__main__':

    TestInstrument().run()
