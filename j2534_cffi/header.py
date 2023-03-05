J2534_HEADER = """
typedef struct
{
	unsigned long	Parameter;	// Name of parameter
	unsigned long	Value;		// Value of the parameter
} SCONFIG;

typedef struct
{
	unsigned long	NumOfParams;	// Number of SCONFIG elements
	SCONFIG*		ConfigPtr;		// Array of SCONFIG
} SCONFIG_LIST;

typedef struct
{
	unsigned long	NumOfBytes;		// Number of bytes in the array
	unsigned char*	BytePtr;		// Array of bytes
} SBYTE_ARRAY;

typedef struct
{
	unsigned long	ProtocolID;
	unsigned long	RxStatus;
	unsigned long	TxFlags;
	unsigned long	Timestamp;
	unsigned long	DataSize;
	unsigned long	ExtraDataIndex;
	unsigned char	Data[4128];
} PASSTHRU_MSG;

long PassThruOpen(void *pName, unsigned long *pDeviceID);
long PassThruClose(unsigned long DeviceID);
long PassThruConnect(unsigned long DeviceID, unsigned long ProtocolID, unsigned long Flags, unsigned long BaudRate, unsigned long *pChannelID);
long PassThruDisconnect(unsigned long ChannelID);
long PassThruReadMsgs(unsigned long ChannelID, PASSTHRU_MSG *pMsg, unsigned long *pNumMsgs, unsigned long Timeout);
long PassThruWriteMsgs(unsigned long ChannelID, PASSTHRU_MSG *pMsg, unsigned long *pNumMsgs, unsigned long Timeout);
long PassThruStartPeriodicMsg(unsigned long ChannelID, PASSTHRU_MSG *pMsg, unsigned long *pMsgID, unsigned long TimeInterval);
long PassThruStopPeriodicMsg(unsigned long ChannelID, unsigned long MsgID);
long PassThruStartMsgFilter(unsigned long ChannelID, unsigned long FilterType, PASSTHRU_MSG *pMaskMsg, PASSTHRU_MSG *pPatternMsg, PASSTHRU_MSG *pFlowControlMsg, unsigned long *pFilterID);
long PassThruStopMsgFilter(unsigned long ChannelID, unsigned long FilterID);
long PassThruSetProgrammingVoltage(unsigned long DeviceID, unsigned long PinNumber, unsigned long Voltage);
long PassThruReadVersion(unsigned long DeviceID, char *pFirmwareVersion, char *pDllVersion, char *pApiVersion);
long PassThruGetLastError(char *pErrorDescription);
long PassThruIoctl(unsigned long ChannelID, unsigned long IoctlID, void *pInput, void *pOutput);
"""
