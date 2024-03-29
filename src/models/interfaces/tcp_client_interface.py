"""
TCP client interface.
"""

import socket
import wx

from src.models.interfaces.interface import Interface


class TcpClientInterface(Interface):

    NAME = "Ethernet TCP"
    DEFAULT_TIMEOUT = 3

    def __init__(self, ip_address, ip_port, rx_timeout=DEFAULT_TIMEOUT, rx_buffer_size=1500):
        params_to_match = {
            "ip_address": ip_address,
            "ip_port": ip_port
        }
        super().__init__(params_to_match)
        self._server_ip_address = ip_address
        self._server_port = ip_port
        self._rx_timeout = rx_timeout
        self._rx_buffer_size = rx_buffer_size
        self._socket = None

    def is_open(self):
        return self._socket is not None

    def open(self):
        # There is no specific way to open this interface
        pass

    def send_command(self, command, expect_response, pre_response, post_response):
        response = b""
        try:
            self._socket = socket.create_connection(
                (self._server_ip_address, self._server_port), self._rx_timeout)
        except (Exception, ):
            self.raise_connection_exception(f"{self._server_ip_address}:{self._server_port}")

        self._socket.sendall(command)
        if expect_response:
            try:
                response = self._socket.recv(self._rx_buffer_size)
            except TimeoutError:
                self.raise_timeout_exception()

        return response

    def close(self):
        if self._socket is not None:
            self._socket.close()
            self._socket = None

    @classmethod
    def get_settings_controls(cls):
        return {
            "ip_address": {
                "label": "IP Address",
                "control": wx.TextCtrl,
                "default": ""
            },
            "ip_port": {
                "label": "Port",
                "control": wx.TextCtrl,
                "default": ""
            },
            "rx_timeout": {
                "label": "RX timeout",
                "control": wx.TextCtrl,
                "default": ""
            }
        }


if __name__ == "__main__":

    from tests.unit_tests.test_models.test_tcp_client_interface import TestTcpClientInterface

    TestTcpClientInterface().run(True)
