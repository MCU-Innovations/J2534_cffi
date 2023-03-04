import unittest

from eculib.canbus import ISOTP

from J2534_cffi import J2534PassThru, build_msg
from J2534_cffi.defines import (
    ProtocolID,
    BaudRate,
    TxFlag,
    ConfigParamValue,
)


__DLL__ = "C:\WINDOWS\SysWOW64\op20pt64.dll"


class J2534TestCase(unittest.TestCase):
    def setUp(self):
        self.j2534 = J2534PassThru(__DLL__)

    def tearDown(self):
        del self.j2534


class TestTactrix_00_General(J2534TestCase):
    def test_01_read_version(self):
        firmware_version, dll_version, api_version = self.j2534.read_version()
        self.assertEqual(firmware_version, "1.17.4877")
        self.assertEqual(dll_version, "1.02.4943 Dec 10 2020 19:47:43")
        self.assertEqual(api_version, "04.04")

    def test_02_read_vbatt(self):
        voltage = self.j2534.read_vbatt()


class TestTactrix_10_CAN(J2534TestCase):

    _baudrate = BaudRate.CAN_500k

    def _send_message(self, protocol_id, tx_flags, arbid, data):
        channel_id = self.j2534.connect(protocol_id, 0, self._baudrate)
        self.j2534.set_config(channel_id, ConfigParamValue.DATA_RATE, self._baudrate)
        data_rate = self.j2534.get_config(channel_id, ConfigParamValue.DATA_RATE)
        self.assertEqual(data_rate, self._baudrate)
        self.j2534.set_config(channel_id, ConfigParamValue.LOOPBACK, 0)
        loopback = self.j2534.get_config(channel_id, ConfigParamValue.LOOPBACK)
        self.assertEqual(loopback, 0)
        self.j2534.clear_periodic_msgs(channel_id)
        self.j2534.clear_msg_filters(channel_id)
        self.j2534.start_ecu_filter(channel_id, protocol_id, 0x7A0, 0x7A0, 0x7A0)
        self.j2534.start_ecu_filter(channel_id, protocol_id, 0xFFFFFFFF, 0x7A8, 0x7A0)
        self.j2534.clear_rx_buffer(channel_id)
        self.j2534.clear_tx_buffer(channel_id)
        msg = build_msg(protocol_id, tx_flags, data, arbid=arbid)
        self.j2534.write_msg(channel_id, msg, 100)
        while True:
            resp = self.j2534.read_msg(channel_id, 100)
            arbid = int.from_bytes(resp[:4], "big")
            if arbid == 0x7A8:
                break
        self.j2534.disconnect(channel_id)
        return resp

    def test_01_test_present_CAN(self):
        resp = self._send_message(
            ProtocolID.CAN,
            0,
            0x7A0,
            b"\x02\x3E\x00",
        )
        self.assertEqual(resp[5:7], b"\x7E\x00")

    def test_02_test_present_ISO15765(self):
        resp = self._send_message(ProtocolID.ISO15765, 0, 0x7A0, b"\x3E\x00")
        self.assertEqual(resp[4:6], b"\x7E\x00")
