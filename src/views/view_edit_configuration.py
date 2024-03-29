"""
View for editing the configuration.
"""

import wx

from src.models.id_manager import IdManager
from src.models.time_converter import TimeConverter


class ViewEditConfiguration(wx.Dialog):

    _GAP = 5

    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY, "Edit Configuration")

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_time_settings_box(self), 0, wx.EXPAND | wx.ALL, self._GAP)
        box.Add(self._create_buttons_box(self), 0, wx.ALIGN_RIGHT | wx.ALL, self._GAP)

        self.SetSizer(box)
        self.SetInitialSize()
        self.CenterOnParent()

        self.Bind(wx.EVT_TEXT, self._on_time_change, self._txt_sample_time)
        self.Bind(wx.EVT_TEXT, self._on_time_change, self._txt_end_time)
        self.Bind(wx.EVT_COMBOBOX, self._on_time_change, self._cmb_sample_time)
        self.Bind(wx.EVT_COMBOBOX, self._on_time_change, self._cmb_end_time)
        self.Bind(wx.EVT_RADIOBUTTON, self._on_time_change, self._radio_end_time)
        self.Bind(wx.EVT_RADIOBUTTON, self._on_time_change, self._radio_continuous)

    def _create_time_settings_box(self, parent):
        box = wx.StaticBoxSizer(wx.StaticBox(parent, wx.ID_ANY, " Time settings: "), wx.VERTICAL)

        lbl_sample_time = wx.StaticText(parent, wx.ID_ANY, "Sample time:")
        self._txt_sample_time = wx.TextCtrl(parent, IdManager.ID_SAMPLE_TIME, size=(50, -1))
        self._cmb_sample_time = wx.ComboBox(parent, IdManager.ID_SAMPLE_TIME_UNITS,
                                            style=wx.CB_READONLY, choices=TimeConverter.TIME_UNITS)
        self._radio_end_time = wx.RadioButton(parent, IdManager.ID_FIXED, "Fixed end time:")
        self._txt_end_time = wx.TextCtrl(parent, IdManager.ID_END_TIME, size=(50, -1))
        self._cmb_end_time = wx.ComboBox(parent, IdManager.ID_END_TIME_UNITS, style=wx.CB_READONLY,
                                         choices=TimeConverter.TIME_UNITS)
        self._radio_continuous = wx.RadioButton(parent, IdManager.ID_CONTINUOUS, "Continuous mode:")
        lbl_continuous = wx.StaticText(parent, wx.ID_ANY, "Process must be stopped manually.")
        lbl_total_samples = wx.StaticText(parent, wx.ID_ANY, "Total samples:")
        self._lbl_total_samples = wx.StaticText(parent, IdManager.ID_TOTAL_SAMPLES, "-")

        grid = wx.GridBagSizer(self._GAP, self._GAP)
        grid.Add(lbl_sample_time, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_sample_time, (0, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_sample_time, (0, 2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._radio_end_time, (1, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_end_time, (1, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_end_time, (1, 2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._radio_continuous, (2, 0), wx.DefaultSpan, wx.ALIGN_TOP)
        grid.Add(lbl_continuous, (2, 1), (1, 2), wx.ALIGN_TOP)
        grid.Add(lbl_total_samples, (3, 0), wx.DefaultSpan)
        grid.Add(self._lbl_total_samples, (3, 1), wx.DefaultSpan)

        box.Add(grid, 0, wx.EXPAND | wx.ALL, self._GAP)

        return box

    def _create_buttons_box(self, parent):
        btn_ok = wx.Button(parent, wx.ID_OK, "Ok")
        btn_cancel = wx.Button(parent, wx.ID_CANCEL, "Cancel")

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(btn_ok, 0, wx.ALL, self._GAP)
        box.Add(btn_cancel, 0, wx.ALL, self._GAP)

        return box

    ##################
    # Event handlers #
    ##################

    def _on_time_change(self, event):
        self._update_total_samples()
        event.Skip()

    ###########
    # Private #
    ###########

    @staticmethod
    def _get_time(value_control, units_control):
        value = 0
        try:
            value = int(value_control.GetValue().strip())
        except ValueError:
            pass
        unit = units_control.GetValue()
        return TimeConverter.convert_time_with_unit_to_seconds(value, unit)

    def _update_total_samples(self):
        total_samples = "-"
        if not self._radio_continuous.GetValue():
            sample_time = self._get_time(self._txt_sample_time, self._cmb_sample_time)
            end_time = self._get_time(self._txt_end_time, self._cmb_end_time)
            if sample_time > 0 and end_time > 0:
                total_samples = int(end_time / sample_time) + 1

        self._lbl_total_samples.SetLabel(str(total_samples))

    ##########
    # Public #
    ##########

    def get_sample_time(self):
        return self._get_time(self._txt_sample_time, self._cmb_sample_time)

    def set_sample_time(self, value):
        value, units = TimeConverter.convert_seconds_to_time_with_unit(value)
        self._txt_sample_time.SetValue(str(value))
        self._cmb_sample_time.SetValue(units)
        self._update_total_samples()

    def get_end_time(self):
        return self._get_time(self._txt_end_time, self._cmb_end_time)

    def set_end_time(self, value):
        value, units = TimeConverter.convert_seconds_to_time_with_unit(value)
        self._txt_end_time.SetValue(str(value))
        self._cmb_end_time.SetValue(units)
        self._update_total_samples()

    def get_continuous_mode(self):
        return self._radio_continuous.GetValue()

    def set_continuous_mode(self, value):
        self._radio_continuous.SetValue(value)
        self._radio_end_time.SetValue(not value)
        self._update_total_samples()


if __name__ == "__main__":

    from tests.unit_tests.test_gui.test_controller_configuration import TestControllerConfiguration

    TestControllerConfiguration().run(True)
