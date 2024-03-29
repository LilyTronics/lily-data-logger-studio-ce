"""
Controller for editing instruments.
"""

import wx

from src.models.id_manager import IdManager
from src.models.instruments import Instruments
from src.models.interfaces import Interfaces
from src.views.view_dialogs import ViewDialogs
from src.views.view_edit_instrument import ViewEditInstrument


class ControllerEditInstrument:

    _dlg = None

    ###########
    # Private #
    ###########

    @classmethod
    def _update_instrument_settings_controls(cls, instrument_name, instrument_settings=None):
        settings_controls = {}
        if instrument_settings is None:
            instrument_settings = {}
        instrument = Instruments.get_instrument_by_name(instrument_name)
        if instrument is not None:
            cls._dlg.set_instrument_info(instrument.get_info())
            interface_type = instrument.get_interface_type()
            if interface_type is not None:
                interface = Interfaces.get_interface_by_name(interface_type)
                if interface is not None:
                    settings_controls = interface.get_settings_controls()
                    instrument_defaults = instrument.get_interface_settings()
                    for key in instrument_defaults.keys():
                        settings_controls[key]["default"] = str(instrument_defaults[key])
                    for key in instrument_settings.keys():
                        if key in settings_controls:
                            settings_controls[key]["default"] = str(instrument_settings[key])
        cls._dlg.update_instrument_settings_controls(settings_controls)

    ##################
    # Event handlers #
    ##################

    @classmethod
    def _on_instrument_select(cls, event):
        cls._dlg.set_instrument_info("")
        cls._dlg.update_instrument_settings_controls({})
        instrument_name = cls._dlg.get_selected_instrument_name()
        if instrument_name != "":
            cls._update_instrument_settings_controls(instrument_name)
        event.Skip()

    @classmethod
    def _on_settings_test(cls, event):
        cls._dlg.clear_console()
        name = cls._dlg.get_name()
        label = "Name"
        cls._dlg.write_to_console(f"{label:12}: '{name}'")
        instrument_name = cls._dlg.get_selected_instrument_name()
        label = "Instrument"
        cls._dlg.write_to_console(f"{label:12}: '{instrument_name}'")
        settings = cls._dlg.get_settings()
        for key in settings.keys():
            cls._dlg.write_to_console(f"{key:12}: '{settings[key]}'")
        interface_object = None
        try:
            assert instrument_name != "", "no instrument selected"
            instrument = Instruments.get_instrument_by_name(instrument_name)
            assert instrument is not None, "instrument does not exist"
            interface_type = instrument.get_interface_type()
            assert interface_type is not None, "No interface defined"
            interface = Interfaces.get_interface_by_name(interface_type)
            assert interface is not None, f"interface type '{interface_type}' does not exist"
            instrument_defaults = instrument.get_interface_settings()
            for key in instrument_defaults.keys():
                if key not in settings.keys():
                    settings[key] = instrument_defaults[key]
            interface_object = interface(**settings)
            instrument.set_interface_object(interface_object)
            input_channels = instrument.get_input_channels()
            assert len(input_channels) > 0, "no input channels available for testing"
            cls._dlg.write_to_console("\nInitialize instrument...")
            instrument.initialize()
            cls._dlg.write_to_console(
                f"Get value from channel: '{input_channels[0][instrument.KEY_NAME]}'")
            value = instrument.process_channel(input_channels[0]["name"])
            if isinstance(value, str) and value.startswith("ERROR: "):
                value = value.strip("ERROR: ")
                raise Exception(value)
            cls._dlg.write_to_console(f"Received value: '{value}'")
            cls._dlg.write_to_console("\nTest finished, all seems fine")
        except Exception as e:
            cls._dlg.write_to_console(f"\nERROR: {e}")
        finally:
            if interface_object is not None:
                interface_object.close()

        event.Skip()

    ##########
    # Public #
    ##########

    @classmethod
    def get_dialog(cls):
        return cls._dlg

    @classmethod
    def edit_instrument(cls, parent, configuration, name):
        dialog_title = "Add instrument"
        instrument_name = ""
        instrument_settings = {}
        if name != "":
            dialog_title = "Edit instrument"
            instrument = configuration.get_instrument(name)
            instrument_name = instrument[configuration.KEY_SETTINGS][
                configuration.KEY_INSTRUMENT_NAME]
            instrument_settings = instrument[configuration.KEY_SETTINGS][
                configuration.KEY_INSTRUMENT_SETTINGS]
        cls._dlg = ViewEditInstrument(parent, dialog_title, configuration, name)
        cls._dlg.set_instrument_names(Instruments.get_instrument_names())
        cls._dlg.set_name(name)
        cls._dlg.set_instrument_name(instrument_name)
        cls._update_instrument_settings_controls(instrument_name, instrument_settings)
        cls._dlg.Bind(wx.EVT_COMBOBOX, cls._on_instrument_select, id=IdManager.ID_CMB_INSTRUMENT)
        cls._dlg.Bind(wx.EVT_BUTTON, cls._on_settings_test, id=IdManager.ID_BTN_SETTINGS_TEST)
        if cls._dlg.ShowModal() == wx.ID_OK:
            new_name = cls._dlg.get_name()
            settings = {
                configuration.KEY_INSTRUMENT_NAME: cls._dlg.get_selected_instrument_name(),
                configuration.KEY_INSTRUMENT_SETTINGS: cls._dlg.get_settings()
            }
            configuration.update_instrument(name, new_name, settings)
        cls._dlg.Destroy()
        cls._dlg = None
        wx.YieldIfNeeded()

    @classmethod
    def delete_instrument(cls, parent, configuration):
        dialog_title = "Delete instrument"
        name = parent.get_selected_instrument()
        if name == "":
            ViewDialogs.show_message(parent, "Select an instrument first", dialog_title)
        else:
            buttons = wx.YES_NO
            message = f"Do you want to delete instrument '{name}'?"
            used_items = configuration.get_used_items_for_instrument(name)
            if len(used_items) > 0:
                measurements = ", ".join(map(lambda x: f"'{x[configuration.KEY_NAME]}'",
                                             used_items))
                buttons |= wx.CANCEL
                message = (f"The instrument '{name}' is used in one or more measurements.\n"
                           "Do you want to delete the following measurements also?\n"
                           f"Measurements: {measurements}\n\n"
                           "Click Yes to delete the instrument and the measurements.\n"
                           "Click No to delete only the instrument.\n"
                           "Click Cancel to abort.")
            button = ViewDialogs.show_confirm(parent, message, dialog_title, buttons)
            if button in (wx.ID_YES, wx.ID_NO):
                configuration.delete_instrument(name)
                if button == wx.ID_YES:
                    for measurement in used_items:
                        configuration.delete_measurement(measurement[configuration.KEY_NAME])
        wx.YieldIfNeeded()


if __name__ == "__main__":

    from tests.unit_tests.test_gui.test_controller_edit_instrument import (
        TestControllerEditInstrument)

    TestControllerEditInstrument().run(True)
