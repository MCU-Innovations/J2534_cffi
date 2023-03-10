# j2534_cffi

This is an attempt to create a non-half-assed J2534 library for Python using CFFI.

## Usage

### Find available interfaces
Scans the Windows registry for installed PassThruSupport.04.04 interfaces
```
>>> from j2534_cffi import find_j2534_passthru_dlls
>>>
>>> for iface in find_j2534_passthru_dlls():
...     print(iface)
...
['6513-Honda', 'C:\\Program Files (x86)\\Bosch\\VTX-VCI\\VCI Software (6513-Honda)\\Products\\6513-Honda\\Dynamic Link Libraries\\BVTX4J32.dll']
['Intrepid neoOBD2Pro', 'C:\\WINDOWS\\system32\\icsJ2534neoOBD2Pro.dll']
['Intrepid neoVI Fire/Red', 'C:\\WINDOWS\\system32\\icsJ2534Fire.dll']
['Intrepid neoVI Fire2', 'C:\\WINDOWS\\system32\\icsJ2534Fire2.dll']
['Intrepid neoVI Plasma VNETB', 'C:\\WINDOWS\\system32\\icsJ2534PlasmaSlaveVNETB.dll']
['Intrepid neoVI Plasma/ION', 'C:\\WINDOWS\\system32\\icsJ2534PlasmaION.dll']
['Intrepid neoVI Plasma/ION VNETA', 'C:\\WINDOWS\\system32\\icsJ2534PlasmaIONSlaveVNETA.dll']
['Intrepid neoVI Red2', 'C:\\WINDOWS\\system32\\icsJ2534Red2.dll']
['Intrepid RADGalaxy', 'C:\\WINDOWS\\system32\\icsJ2534RADGalaxy.dll']
['Intrepid RADGigastar', 'C:\\WINDOWS\\system32\\icsJ2534RADGigastar.dll']
['Intrepid RADJupiter', 'C:\\WINDOWS\\system32\\icsJ2534RADJupiter.dll']
['Intrepid RADPluto', 'C:\\WINDOWS\\system32\\icsJ2534RADPluto.dll']
['Intrepid ValueCAN3', 'C:\\WINDOWS\\system32\\icsJ2534VCAN3.dll']
['Intrepid ValueCAN4-1', 'C:\\WINDOWS\\system32\\icsJ2534VCAN41.dll']
['Intrepid ValueCAN4-2', 'C:\\WINDOWS\\system32\\icsJ2534VCAN42.dll']
['Intrepid ValueCAN4-2EL', 'C:\\WINDOWS\\system32\\icsJ2534VCAN42-EL.dll']
['Intrepid ValueCAN4-4', 'C:\\WINDOWS\\system32\\icsJ2534VCAN44.dll']
['J2534 for Kvaser Hardware', 'C:\\Program Files\\Kvaser\\Drivers\\32\\j2534api.dll']
['OpenPort 2.0 J2534 ISO/CAN/VPW/PWM', 'C:\\WINDOWS\\SysWOW64\\op20pt32.dll']
['J2534 for Kvaser Hardware', 'C:\\Program Files\\Kvaser\\Drivers\\j2534api.dll']
```

### Open an interface
Load a J2534 interface by path; can be a dll listed in the registry or from a custom path.
```
>>> from j2534_cffi import J2534PassThru
>>> dll_path = "drivers/op20pt64.dll"
>>> iface = J2534PassThru(dll_path)
>>> iface.dll
<cffi.api._make_ffi_library.<locals>.FFILibrary object at 0x0000011888F73760>
>>> iface.device_id
1
```
