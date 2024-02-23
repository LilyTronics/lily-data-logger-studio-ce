"""
Progress dialog.
"""

import wx


class ProgressDialog(wx.ProgressDialog):

    _TIMER_INTERVAL = 100

    def __init__(self, parent, title, maximum):
        super().__init__(title, " ", maximum, parent, wx.PD_CAN_ABORT | wx.PD_APP_MODAL)
        parent.active_dialog = self
        self.Fit()
        self.CenterOnParent()
        self._timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._on_timer, self._timer)
        self._timer.Start(self._TIMER_INTERVAL)

    ##################
    # Event handlers #
    ##################

    def _on_timer(self, event):
        if not self.Update(self.GetValue())[0]:
            self.destroy()
        event.Skip()

    ##########
    # Public #
    ##########

    def destroy(self):
        self._timer.Stop()
        self.GetParent().active_dialog = None
        self.Destroy()

    def update(self, value, message=wx.EmptyString):
        do_continue = True
        if value < self.GetRange():
            do_continue = self.Update(value, message)[0]
            self.Fit()
            self.CenterOnParent()
        else:
            self.destroy()
        return do_continue


if __name__ == "__main__":

    import pylint
    from tests.unit_tests.test_gui.test_view_progress_dialog import TestViewProgressDialog

    TestViewProgressDialog().run()
    pylint.run_pylint([__file__])
