import time
import cffi
from _cffi_backend import _CDataBase
from .header import J2534_HEADER
from .defines import IoctlIDValues, FilterType, ErrorValue


def wait(delta) -> None:
    now: float = time.perf_counter()
    while time.perf_counter() - now < delta:
        continue


class J2534PassThru:
    def __init__(self, dll_path) -> None:
        self.ffi = cffi.FFI()
        self.ffi.cdef(J2534_HEADER)
        self.dll_path = dll_path
        self.device_id: None | int = None
        self.dll = None
        self.dll: object = self.ffi.dlopen(self.dll_path)
        device_id: _CDataBase = self.ffi.new("unsigned long *")
        result: ErrorValue = ErrorValue(self.dll.PassThruOpen(self.ffi.NULL, device_id))
        if result == 0:
            self.device_id = device_id[0]
        self.ffi.release(device_id)

    def __build_msg(self, protocol_id, tx_flags, data=b"", arbid=None) -> _CDataBase:
        msg: _CDataBase = self.ffi.new("PASSTHRU_MSG *")
        msg.ProtocolID = protocol_id
        msg.TxFlags = tx_flags
        msg.Timestamp = 0
        msg.ExtraDataIndex = 0
        offset = 0
        if arbid is not None:
            for byt in arbid.to_bytes(4, "big"):
                msg.Data[offset] = byt
                offset += 1
        for byt in data:
            msg.Data[offset] = byt
            offset += 1
        msg.DataSize = offset
        return msg

    def __del__(self) -> None:
        if self.dll is not None:
            if self.device_id is not None:
                self.dll.PassThruClose(self.device_id)
                self.device_id = None
            self.ffi.dlclose(self.dll)
            del self.dll
        self.dll = None

    def get_last_error(self) -> tuple[None | str, ErrorValue]:
        _error: None | str = None
        error: _CDataBase = self.ffi.new("char[80]")
        result: ErrorValue = ErrorValue(self.dll.PassThruGetLastError(error))
        if result is ErrorValue.STATUS_NOERROR:
            _error = self.ffi.string(error).decode("latin1")
        self.ffi.release(error)
        return _error, result

    def read_vbatt(self) -> tuple[None | float, ErrorValue]:
        _voltage: None | float = None
        voltage: _CDataBase = self.ffi.new("unsigned long *")
        result: ErrorValue = ErrorValue(
            self.dll.PassThruIoctl(
                self.device_id, IoctlIDValues.READ_VBATT, self.ffi.NULL, voltage
            )
        )
        if result is ErrorValue.STATUS_NOERROR:
            _voltage = voltage[0] / 1000.0
        self.ffi.release(voltage)
        return _voltage, result

    def read_version(self) -> tuple[None | tuple[str, str, str], ErrorValue]:
        _version: None | tuple[str, str, str] = None
        firmware_version: _CDataBase = self.ffi.new("char[80]")
        dll_version: _CDataBase = self.ffi.new("char[80]")
        api_version: _CDataBase = self.ffi.new("char[80]")
        result: ErrorValue = ErrorValue(
            self.dll.PassThruReadVersion(
                self.device_id, firmware_version, dll_version, api_version
            )
        )
        if result is ErrorValue.STATUS_NOERROR:
            _version = (
                self.ffi.string(firmware_version).decode(),
                self.ffi.string(dll_version).decode(),
                self.ffi.string(api_version).decode(),
            )
        self.ffi.release(firmware_version)
        self.ffi.release(dll_version)
        self.ffi.release(api_version)
        return _version, result

    def connect(self, protocol_id, flags, baud_rate) -> tuple[None | int, ErrorValue]:
        _channel_id: None | int = None
        channel_id: _CDataBase = self.ffi.new("unsigned long *")
        result: ErrorValue = ErrorValue(
            self.dll.PassThruConnect(
                self.device_id, protocol_id, flags, baud_rate, channel_id
            )
        )
        if result == 0:
            _channel_id = channel_id[0]
        self.ffi.release(channel_id)
        return _channel_id, result

    def disconnect(self, channel_id) -> tuple[None, ErrorValue]:
        return None, ErrorValue(self.dll.PassThruDisconnect(channel_id))

    def clear_periodic_msgs(self, channel_id) -> tuple[None, ErrorValue]:
        return None, ErrorValue(
            self.dll.PassThruIoctl(
                channel_id,
                IoctlIDValues.CLEAR_PERIODIC_MSGS,
                self.ffi.NULL,
                self.ffi.NULL,
            )
        )

    def clear_msg_filters(self, channel_id) -> tuple[None, ErrorValue]:
        return None, ErrorValue(
            self.dll.PassThruIoctl(
                channel_id,
                IoctlIDValues.CLEAR_MSG_FILTERS,
                self.ffi.NULL,
                self.ffi.NULL,
            )
        )

    def start_ecu_filter(
        self,
        channel_id: int,
        protocol_id: int,
        mask: None | int = None,
        pattern: None | int = None,
        flow_control: None | int = None,
        tx_flags: int = 0,
        filter_type: FilterType = FilterType.FLOW_CONTROL_FILTER,
    ) -> tuple[int | None, ErrorValue]:
        _filter_id: None | int = None
        filter_id: _CDataBase = self.ffi.new("unsigned long *")
        if filter_type == FilterType.FLOW_CONTROL_FILTER:
            mask_msg: _CDataBase = self.__build_msg(protocol_id, tx_flags, arbid=mask)
            pattern_msg: _CDataBase = self.__build_msg(
                protocol_id, tx_flags, arbid=pattern
            )
            flow_control_msg: _CDataBase = self.__build_msg(
                protocol_id, tx_flags, arbid=flow_control
            )
        else:
            mask_msg = self.__build_msg(protocol_id, tx_flags, arbid=mask)
            pattern_msg = self.__build_msg(protocol_id, tx_flags, arbid=pattern)
            flow_control_msg = self.ffi.NULL
        result: ErrorValue = ErrorValue(
            self.dll.PassThruStartMsgFilter(
                channel_id,
                filter_type,
                mask_msg,
                pattern_msg,
                flow_control_msg,
                filter_id,
            )
        )
        if result == ErrorValue.STATUS_NOERROR:
            _filter_id = filter_id[0]
        if mask_msg != self.ffi.NULL:
            self.ffi.release(mask_msg)
        if pattern_msg != self.ffi.NULL:
            self.ffi.release(pattern_msg)
        if flow_control_msg != self.ffi.NULL:
            self.ffi.release(flow_control_msg)
        self.ffi.release(filter_id)
        return _filter_id, result

    def clear_rx_buffer(
        self,
        channel_id: int,
    ) -> tuple[None, ErrorValue]:
        return None, ErrorValue(
            self.dll.PassThruIoctl(
                channel_id, IoctlIDValues.CLEAR_RX_BUFFER, self.ffi.NULL, self.ffi.NULL
            )
        )

    def clear_tx_buffer(
        self,
        channel_id: int,
    ) -> tuple[None, ErrorValue]:
        return None, ErrorValue(
            self.dll.PassThruIoctl(
                channel_id, IoctlIDValues.CLEAR_TX_BUFFER, self.ffi.NULL, self.ffi.NULL
            )
        )

    def write_msg(
        self,
        channel_id: int,
        protocol_id: int,
        tx_flags,
        data,
        arbid: None | int,
        timeout: int,
    ) -> tuple[None, ErrorValue]:
        num_msgs: _CDataBase = self.ffi.new("unsigned long *", 1)
        msg: _CDataBase = self.__build_msg(protocol_id, tx_flags, data, arbid=arbid)
        result: ErrorValue = ErrorValue(
            self.dll.PassThruWriteMsgs(channel_id, msg, num_msgs, timeout)
        )
        self.ffi.release(num_msgs)
        self.ffi.release(msg)
        return None, result

    def read_msg(
        self,
        channel_id: int,
        timeout: int,
    ) -> tuple[bytes | None, ErrorValue]:
        _msg: None | bytes = None
        msg: _CDataBase = self.ffi.new("PASSTHRU_MSG *")
        num_msgs: _CDataBase = self.ffi.new("unsigned long *", 1)
        result: ErrorValue = ErrorValue(
            self.dll.PassThruReadMsgs(channel_id, msg, num_msgs, timeout)
        )
        if result == 0:
            _msg = bytes(self.ffi.unpack(msg.Data, msg.DataSize))
        self.ffi.release(num_msgs)
        self.ffi.release(msg)
        return _msg, result

    def get_config(
        self,
        channel_id: int,
        parameter: int,
    ) -> tuple[int | None, ErrorValue]:
        _value: None | int = None
        sconfig: _CDataBase = self.ffi.new("SCONFIG *", (parameter, 0))
        sconfig_list: _CDataBase = self.ffi.new("SCONFIG_LIST *", (1, sconfig))
        result: ErrorValue = ErrorValue(
            self.dll.PassThruIoctl(
                channel_id,
                IoctlIDValues.GET_CONFIG,
                sconfig_list,
                self.ffi.NULL,
            )
        )
        if result == 0:
            _value = sconfig.Value
        self.ffi.release(sconfig)
        self.ffi.release(sconfig_list)
        return _value, result

    def set_config(
        self,
        channel_id: int,
        parameter: int,
        value: int,
    ) -> tuple[None, ErrorValue]:
        sconfig: _CDataBase = self.ffi.new("SCONFIG *", (parameter, value))
        sconfig_list: _CDataBase = self.ffi.new("SCONFIG_LIST *", (1, sconfig))
        result: ErrorValue = ErrorValue(
            self.dll.PassThruIoctl(
                channel_id,
                IoctlIDValues.SET_CONFIG,
                sconfig_list,
                self.ffi.NULL,
            )
        )
        return None, result

    def fast_init(
        self,
        channel_id: int,
        protocol_id: int,
        tx_flags: int,
    ) -> tuple[None, ErrorValue]:
        msg: _CDataBase = self.__build_msg(protocol_id, tx_flags)
        result: ErrorValue = ErrorValue(
            self.dll.PassThruIoctl(
                channel_id,
                IoctlIDValues.FAST_INIT,
                msg,
                self.ffi.NULL,
            )
        )
        self.ffi.release(msg)
        return None, result

    # UNTESTED BELOW THIS LINE

    # def read_prog_voltage(self, channel_id):
    #     _voltage = None
    #     voltage = self.ffi.new("unsigned long *")
    #     result = self.dll.PassThruIoctl(
    #         channel_id, IoctlIDValues.READ_PROG_VOLTAGE, self.ffi.NULL, voltage
    #     )
    #     if result == 0:
    #         _voltage = voltage[0] / 1000.0
    #     self.ffi.release(voltage)
    #     return _voltage, result

    # def clear_funct_msg_lookup_table(self, channel_id):
    #     return None, self.dll.PassThruIoctl(
    #         channel_id,
    #         IoctlIDValues.CLEAR_FUNCT_MSG_LOOKUP_TABLE,
    #         self.ffi.NULL,
    #         self.ffi.NULL,
    #     )
