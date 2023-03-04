import cffi
from .header import J2534_HEADER
from .defines import IoctlIDValues, ProtocolID, FilterType, ErrorValue

ffi = cffi.FFI()
ffi.cdef(J2534_HEADER)


def build_msg(protocol_id, tx_flags, data=b"", arbid=None):
    msg = ffi.new("PASSTHRU_MSG *")
    msg.ProtocolID = protocol_id
    msg.TxFlags = tx_flags
    msg.Timestamp = 0
    msg.ExtraDataIndex = 0
    offset = 0
    if arbid is not None:
        for b in arbid.to_bytes(4, "big"):
            msg.Data[offset] = b
            offset += 1
    for b in data:
        msg.Data[offset] = b
        offset += 1
    msg.DataSize = offset
    return msg


class J2534PassThru:
    def __init__(self, dll_path):
        self.device_id = None
        self.dll = ffi.dlopen(dll_path)
        device_id = ffi.new("unsigned long *")
        result = self.dll.PassThruOpen(ffi.NULL, device_id)
        if result == 0:
            self.device_id = device_id[0]
        ffi.release(device_id)
        if self.device_id is None:
            raise Exception("PassThruOpen failed")

    def __del__(self):
        result = self.dll.PassThruClose(self.device_id)
        ffi.dlclose(self.dll)
        if result != 0:
            raise Exception("PassThruClose failed")

    def get_last_error(self):
        error = ffi.new("char[80]")
        self.dll.PassThruGetLastError(error)
        _error = ffi.string(error).decode()
        ffi.release(error)
        return _error

    def read_vbatt(self):
        _voltage = None
        voltage = ffi.new("unsigned long *")
        result = self.dll.PassThruIoctl(
            self.device_id, IoctlIDValues.READ_VBATT, ffi.NULL, voltage
        )
        if result == 0:
            _voltage = voltage[0]
        ffi.release(voltage)
        if _voltage is None:
            raise Exception("PassThruIoctl failed")
        return _voltage / 1000.0

    def read_version(self):
        _version = None
        firmware_version = ffi.new("char[80]")
        dll_version = ffi.new("char[80]")
        api_version = ffi.new("char[80]")
        result = self.dll.PassThruReadVersion(
            self.device_id, firmware_version, dll_version, api_version
        )
        if result == 0:
            _version = (
                ffi.string(firmware_version).decode(),
                ffi.string(dll_version).decode(),
                ffi.string(api_version).decode(),
            )
        ffi.release(firmware_version)
        ffi.release(dll_version)
        ffi.release(api_version)
        if _version is None:
            raise Exception("PassThruReadVersion failed")
        return _version

    def connect(self, protocol_id, flags, baud_rate):
        _channel_id = None
        channel_id = ffi.new("unsigned long *")
        result = self.dll.PassThruConnect(
            self.device_id, protocol_id, flags, baud_rate, channel_id
        )
        if result == 0:
            _channel_id = channel_id[0]
        ffi.release(channel_id)
        if _channel_id is None:
            raise Exception("PassThruConnect failed")
        return _channel_id

    def disconnect(self, channel_id):
        result = self.dll.PassThruDisconnect(channel_id)
        if result != 0:
            raise Exception("PassThruDisconnect failed")

    def clear_periodic_msgs(self, channel_id):
        result = self.dll.PassThruIoctl(
            channel_id, IoctlIDValues.CLEAR_PERIODIC_MSGS, ffi.NULL, ffi.NULL
        )
        if result != 0:
            raise Exception("PassThruIoctl failed")

    def clear_msg_filters(self, channel_id):
        result = self.dll.PassThruIoctl(
            channel_id, IoctlIDValues.CLEAR_MSG_FILTERS, ffi.NULL, ffi.NULL
        )
        if result != 0:
            raise Exception("PassThruIoctl failed")

    def start_ecu_filter(
        self,
        channel_id,
        protocol_id,
        mask=ffi.NULL,
        pattern=ffi.NULL,
        flow_control=ffi.NULL,
        tx_flags=0,
    ):
        _filter_id = None
        filter_id = ffi.new("unsigned long *")
        if protocol_id == ProtocolID.ISO15765:
            mask_msg = build_msg(protocol_id, tx_flags, arbid=mask)
            pattern_msg = build_msg(protocol_id, tx_flags, arbid=pattern)
            flow_control_msg = build_msg(protocol_id, tx_flags, arbid=flow_control)
            result = self.dll.PassThruStartMsgFilter(
                channel_id,
                FilterType.BLOCK_FILTER,
                mask_msg,
                pattern_msg,
                flow_control_msg,
                filter_id,
            )
        else:
            mask_msg = build_msg(protocol_id, 0, arbid=mask)
            pattern_msg = build_msg(protocol_id, 0, arbid=pattern)
            flow_control_msg = ffi.NULL
            result = self.dll.PassThruStartMsgFilter(
                channel_id,
                FilterType.FLOW_CONTROL_FILTER,
                mask_msg,
                pattern_msg,
                flow_control_msg,
                filter_id,
            )
        if result == 0:
            _filter_id = filter_id[0]
        if mask_msg != ffi.NULL:
            ffi.release(mask_msg)
        if pattern_msg != ffi.NULL:
            ffi.release(pattern_msg)
        if flow_control_msg != ffi.NULL:
            ffi.release(flow_control_msg)
        ffi.release(filter_id)
        if _filter_id is None:
            raise Exception("PassThruStartMsgFilter failed")
        return _filter_id

    def clear_rx_buffer(self, channel_id):
        result = self.dll.PassThruIoctl(
            channel_id, IoctlIDValues.CLEAR_RX_BUFFER, ffi.NULL, ffi.NULL
        )
        if result != 0:
            raise Exception("PassThruIoctl failed")

    def clear_tx_buffer(self, channel_id):
        result = self.dll.PassThruIoctl(
            channel_id, IoctlIDValues.CLEAR_TX_BUFFER, ffi.NULL, ffi.NULL
        )
        if result != 0:
            raise Exception("PassThruIoctl failed")

    def write_msg(self, channel_id, msg, timeout):
        num_msgs = ffi.new("unsigned long *", 1)
        result = self.dll.PassThruWriteMsgs(channel_id, msg, num_msgs, timeout)
        ffi.release(num_msgs)
        ffi.release(msg)
        if result != 0:
            raise Exception("PassThruWriteMsgs failed")

    def read_msg(self, channel_id, timeout):
        _msg = None
        msg = ffi.new("PASSTHRU_MSG *")
        num_msgs = ffi.new("unsigned long *", 1)
        result = self.dll.PassThruReadMsgs(channel_id, msg, num_msgs, timeout)
        ffi.release(num_msgs)
        if result == 0:
            _msg = bytes(ffi.unpack(msg.Data, msg.DataSize))
        ffi.release(msg)
        if _msg is None:
            raise Exception("PassThruReadMsgs failed")
        return _msg

    def get_config(self, channel_id, parameter):
        _value = None
        sconfig = ffi.new("SCONFIG *", (parameter, 0))
        sconfig_list = ffi.new("SCONFIG_LIST *", (1, sconfig))
        result = self.dll.PassThruIoctl(
            channel_id,
            IoctlIDValues.GET_CONFIG,
            sconfig_list,
            ffi.NULL,
        )
        if result == 0:
            _value = sconfig.Value
        ffi.release(sconfig)
        ffi.release(sconfig_list)
        if _value is None:
            raise Exception("PassThruIoctl failed", ErrorValue(result))
        return _value

    def set_config(self, channel_id, parameter, value):
        sconfig = ffi.new("SCONFIG *", (parameter, value))
        sconfig_list = ffi.new("SCONFIG_LIST *", (1, sconfig))
        result = self.dll.PassThruIoctl(
            channel_id,
            IoctlIDValues.SET_CONFIG,
            sconfig_list,
            ffi.NULL,
        )
        if result != 0:
            raise Exception("PassThruIoctl failed", ErrorValue(result))

    # UNTESTED BELOW THIS LINE

    def read_prog_voltage(self, channel_id):
        _voltage = None
        voltage = ffi.new("unsigned long *")
        result = self.dll.PassThruIoctl(
            channel_id, IoctlIDValues.READ_PROG_VOLTAGE, ffi.NULL, voltage
        )
        if result == 0:
            _voltage = voltage[0]
        ffi.release(voltage)
        if _voltage is None:
            raise Exception("PassThruIoctl failed")
        return _voltage / 1000.0

    def clear_funct_msg_lookup_table(self, channel_id):
        result = self.dll.PassThruIoctl(
            channel_id,
            IoctlIDValues.CLEAR_FUNCT_MSG_LOOKUP_TABLE,
            ffi.NULL,
            ffi.NULL,
        )
        if result != 0:
            raise Exception("PassThruIoctl failed")
