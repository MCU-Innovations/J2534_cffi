from enum import IntEnum


class ProtocolID(IntEnum):
    # J2534-1 v04.04 ProtocolID Values
    J1850VPW = 0x01
    J1850PWM = 0x02
    ISO9141 = 0x03
    ISO14230 = 0x04
    CAN = 0x05
    ISO15765 = 0x06
    SCI_A_ENGINE = 0x07
    SCI_A_TRANS = 0x08
    SCI_B_ENGINE = 0x09
    SCI_B_TRANS = 0x0A
    # J2534-2 ProtocolID Values
    J1850VPW_PS = 0x00008000
    J1850PWM_PS = 0x00008001
    ISO9141_PS = 0x00008002
    ISO14230_PS = 0x00008003
    CAN_PS = 0x00008004
    ISO15765_PS = 0x00008005
    J2610_PS = 0x00008006
    SW_ISO15765_PS = 0x00008007
    SW_CAN_PS = 0x00008008
    GM_UART_PS = 0x00008009
    CAN_CH1 = 0x00009000
    CAN_CH2 = CAN_CH1 + 1
    CAN_CH128 = CAN_CH1 + 127
    J1850VPW_CH1 = 0x00009080
    J1850VPW_CH2 = J1850VPW_CH1 + 1
    J1850VPW_CH128 = J1850VPW_CH1 + 127
    J1850PWM_CH1 = 0x00009160
    J1850PWM_CH2 = J1850PWM_CH1 + 1
    J1850PWM_CH128 = J1850PWM_CH1 + 127
    ISO9141_CH1 = 0x00009240
    ISO9141_CH2 = ISO9141_CH1 + 1
    ISO9141_CH128 = ISO9141_CH1 + 127
    ISO14230_CH1 = 0x00009320
    ISO14230_CH2 = ISO14230_CH1 + 1
    ISO14230_CH128 = ISO14230_CH1 + 127
    ISO15765_CH1 = 0x00009400
    ISO15765_CH2 = ISO15765_CH1 + 1
    ISO15765_CH128 = ISO15765_CH1 + 127
    SW_CAN_CAN_CH1 = 0x00009480
    SW_CAN_CAN_CH2 = SW_CAN_CAN_CH1 + 1
    SW_CAN_CAN_CH128 = SW_CAN_CAN_CH1 + 127
    SW_CAN_ISO15765_CH1 = 0x00009560
    SW_CAN_ISO15765_CH2 = SW_CAN_ISO15765_CH1 + 1
    SW_CAN_ISO15765_CH128 = SW_CAN_ISO15765_CH1 + 127
    J2610_CH1 = 0x00009640
    J2610_CH2 = J2610_CH1 + 1
    J2610_CH128 = J2610_CH1 + 127
    ANALOG_IN_CH1 = 0x0000C000
    ANALOG_IN_CH2 = 0x0000C001
    ANALOG_IN_CH32 = 0x0000C01F


class ErrorValue(IntEnum):
    STATUS_NOERROR = 0x00
    ERR_NOT_SUPPORTED = 0x01
    ERR_INVALID_CHANNEL_ID = 0x02
    ERR_INVALID_PROTOCOL_ID = 0x03
    ERR_NULL_PARAMETER = 0x04
    ERR_INVALID_IOCTL_VALUE = 0x05
    ERR_INVALID_FLAGS = 0x06
    ERR_FAILED = 0x07
    ERR_DEVICE_NOT_CONNECTED = 0x08
    ERR_TIMEOUT = 0x09
    ERR_INVALID_MSG = 0x0A
    ERR_INVALID_TIME_INTERVAL = 0x0B
    ERR_EXCEEDED_LIMIT = 0x0C
    ERR_INVALID_MSG_ID = 0x0D
    ERR_DEVICE_IN_USE = 0x0E
    ERR_INVALID_IOCTL_ID = 0x0F
    ERR_BUFFER_EMPTY = 0x10
    ERR_BUFFER_FULL = 0x11
    ERR_BUFFER_OVERFLOW = 0x12
    ERR_PIN_INVALID = 0x13
    ERR_CHANNEL_IN_USE = 0x14
    ERR_MSG_PROTOCOL_ID = 0x15
    ERR_INVALID_FILTER_ID = 0x16
    ERR_NO_FLOW_CONTROL = 0x17
    ERR_NOT_UNIQUE = 0x18
    ERR_INVALID_BAUDRATE = 0x19
    ERR_INVALID_DEVICE_ID = 0x1A


class ConnectFlag(IntEnum):
    # J2534-1 v04.04 Connect Flags
    CAN_29BIT_ID = 0x0100
    ISO9141_NO_CHECKSUM = 0x0200
    CAN_ID_BOTH = 0x0800
    ISO9141_K_LINE_ONLY = 0x1000


class FilterType(IntEnum):
    # J2534-1 v04.04 Filter Type Values
    PASS_FILTER = 0x01
    BLOCK_FILTER = 0x02
    FLOW_CONTROL_FILTER = 0x03


class PinNumber(IntEnum):
    # J2534-1 v04.04 Programming Voltage Pin Numbers
    AUXILIARY_OUTPUT_PIN = 0x0
    SAE_J1962_CONNECTOR_PIN_6 = 0x6
    SAE_J1962_CONNECTOR_PIN_9 = 0x9
    SAE_J1962_CONNECTOR_PIN_11 = 0xB
    SAE_J1962_CONNECTOR_PIN_12 = 0xC
    SAE_J1962_CONNECTOR_PIN_13 = 0xD
    SAE_J1962_CONNECTOR_PIN_14 = 0xE
    SAE_J1962_CONNECTOR_PIN_15 = 0xF


class VoltageValue(IntEnum):
    # J2534-1 v04.04 Programming Voltage Values
    SHORT_TO_GROUND = 0xFFFFFFFE
    VOLTAGE_OFF = 0xFFFFFFFF


class IoctlIDValues(IntEnum):
    # J2534-1 v04.04 IOCTL ID Values
    GET_CONFIG = 0x01
    SET_CONFIG = 0x02
    READ_VBATT = 0x03
    FIVE_BAUD_INIT = 0x04
    FAST_INIT = 0x05
    CLEAR_TX_BUFFER = 0x07
    CLEAR_RX_BUFFER = 0x08
    CLEAR_PERIODIC_MSGS = 0x09
    CLEAR_MSG_FILTERS = 0x0A
    CLEAR_FUNCT_MSG_LOOKUP_TABLE = 0x0B
    ADD_TO_FUNCT_MSG_LOOKUP_TABLE = 0x0C
    DELETE_FROM_FUNCT_MSG_LOOKUP_TABLE = 0x0D
    READ_PROG_VOLTAGE = 0x0E
    # J2534-2 IOCTL ID Values
    SW_CAN_HS = 0x00008000
    SW_CAN_NS = 0x00008001
    SET_POLL_RESPONSE = 0x00008002
    BECOME_MASTER = 0x00008003


class ConfigParamValue(IntEnum):
    # J2534-1 v04.04 Configuration Parameter Values
    DATA_RATE = 0x01
    LOOPBACK = 0x03
    NODE_ADDRESS = 0x04
    NETWORK_LINE = 0x05
    P1_MIN = 0x06
    P1_MAX = 0x07
    P2_MIN = 0x08
    P2_MAX = 0x09
    P3_MIN = 0x0A
    P3_MAX = 0x0B
    P4_MIN = 0x0C
    P4_MAX = 0x0D
    W0 = 0x19
    W1 = 0x0E
    W2 = 0x0F
    W3 = 0x10
    W4 = 0x11
    W5 = 0x12
    TIDLE = 0x13
    TINIL = 0x14
    TWUP = 0x15
    PARITY = 0x16
    BIT_SAMPLE_POINT = 0x17
    SYNC_JUMP_WIDTH = 0x18
    T1_MAX = 0x1A
    T2_MAX = 0x1B
    T3_MAX = 0x24
    T4_MAX = 0x1C
    T5_MAX = 0x1D
    ISO15765_BS = 0x1E
    ISO15765_STMIN = 0x1F
    ISO15765_BS_TX = 0x22
    ISO15765_STMIN_TX = 0x23
    DATA_BITS = 0x20
    FIVE_BAUD_MOD = 0x21
    ISO15765_WFT_MAX = 0x25
    # J2534-2 Configuration Parameter Values
    CAN_MIXED_FORMAT = 0x00008000
    J1962_PINS = 0x00008001
    SW_CAN_HS_DATA_RATE = 0x00008010
    SW_CAN_SPEEDCHANGE_ENABLE = 0x00008011
    SW_CAN_RES_SWITCH = 0x00008012
    ACTIVE_CHANNELS = 0x00008020
    SAMPLE_RATE = 0x00008021
    SAMPLES_PER_READING = 0x00008022
    READINGS_PER_MSG = 0x00008023
    AVERAGING_METHOD = 0x00008024
    SAMPLE_RESOLUTION = 0x00008025
    INPUT_RANGE_LOW = 0x00008026
    INPUT_RANGE_HIGH = 0x00008027


class MixedModeFormat(IntEnum):
    # J2534-2 Mixed-Mode/Format CAN Definitions
    CAN_MIXED_FORMAT_OFF = 0x0
    CAN_MIXED_FORMAT_ON = 0x1
    CAN_MIXED_FORMAT_ALL_FRAMES = 0x2


class AnalogAveragingMethod(IntEnum):
    # J2534-2 Analog Channel Averaging Method Definitions
    SIMPLE_AVERAGE = 0x0
    MAX_LIMIT_AVERAGE = 0x1
    MIN_LIMIT_AVERAGE = 0x2
    MEDIAN_AVERAGE = 0x3


class RxStatus(IntEnum):
    # J2534-1 v04.04 RxStatus Definitions
    TX_MSG_TYPE = 0x0001
    START_OF_MESSAGE = 0x0002
    RX_BREAK = 0x0004
    TX_INDICATION = 0x0008
    ISO15765_PADDING_ERROR = 0x0010
    ISO15765_ADDR_TYPE = 0x0080
    CAN_29BIT_ID = 0x0100
    # J2534-2 RxStatus Definitions
    SW_CAN_HV_RX = 0x00010000
    SW_CAN_HS_RX = 0x00020000
    SW_CAN_NS_RX = 0x00040000
    OVERFLOW_ = 0x00010000


class TxFlag(IntEnum):
    # J2534-1 v04.04 TxFlags Definitions
    ISO15765_FRAME_PAD = 0x0040
    ISO15765_ADDR_TYPE = 0x0080
    CAN_29BIT_ID = 0x0100
    WAIT_P3_MIN_ONLY = 0x0200
    SCI_MODE = 0x400000
    SCI_TX_VOLTAGE = 0x800000
    # J2534-2 TxFlags Definitions
    SW_CAN_HV_TX = 0x00000400


### CUSTOM


class BaudRate(IntEnum):
    SCI = 7813
    SCI_HIGHSPEED = 62500
    ISO9141_10400 = 10400
    ISO9141_10000 = 10000
    ISO14230_10400 = 10400
    ISO14230_10000 = 10000
    J1850PWM_41600 = 41600
    J1850PWM_83300 = 83300
    J1850VPW_10400 = 10400
    J1850VPW_41600 = 41600
    CAN_125K = 125000
    CAN_250K = 250000
    CAN_500K = 500000