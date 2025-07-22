import os
import sys
import struct
try:
    import winreg
except ImportError:
    winreg = None

def test_dll(dll, allowed=[]):
    if os.path.isfile(dll):
        with open(dll, "rb") as f:
            if f.read(2) == b'MZ':
                f.seek(60)
                header_offset = struct.unpack("<L", f.read(4))[0]
                f.seek(header_offset + 4)
                if struct.unpack("<H", f.read(2))[0] in allowed:
                    return True
    return False


def _get_j2534_passthru_dlls(base_key):
    tool_info = []
    tool_list = []
    j2534_registry_info = []
    try:
        if winreg:
            count = winreg.QueryInfoKey(base_key)[0]
            for idx in range(count):
                device_key = winreg.OpenKeyEx(base_key, winreg.EnumKey(base_key, idx))
                name = winreg.QueryValueEx(device_key, "Name")[0]
                function_library = winreg.QueryValueEx(device_key, "FunctionLibrary")[0]
                vendor = winreg.QueryValueEx(device_key, "Vendor")[0]
                protos = []
                try:
                    if winreg.QueryValueEx(device_key, "ISO14230")[0]:
                        protos.append("kline")
                except Exception:
                    pass
                try:
                    if winreg.QueryValueEx(device_key, "ISO15765")[0]:
                        protos.append("can")
                except Exception:
                    pass
                tool_list.append([name, function_library, protos])
                tool_info.append([idx, vendor, name, function_library])
                j2534_registry_info.append(tool_info)
    except Exception as err:
        if __debug__:
            print("j2535_cffi: _get_j2534_passthru_dlls", err)
    return tool_list


def find_j2534_passthru_dlls():
    device_list = []
    dlls = []
    paths =  [r"Software\\WOW6432Node\\PassThruSupport.04.04\\", r"Software\\PassThruSupport.04.04\\"]
    allowed = [34404] if sys.maxsize > 2**32 else [332]
    for path in paths:
        base_key = None
        try:
            base_key = winreg.OpenKeyEx(
                winreg.HKEY_LOCAL_MACHINE,
            path,
                access=winreg.KEY_READ,
            )
        except Exception as err:
            if __debug__:
                print("j2535_cffi: find_j2534_passthru_dlls", err)
        if base_key is not None:
            for name, dll, protos in _get_j2534_passthru_dlls(base_key):
                if test_dll(dll, allowed=allowed):
                    if dll not in dlls:
                        dlls.append(dll)
                        device_list.append((name, dll, protos))
    return device_list


if __name__ == "__main__":
    for i, dll in enumerate(find_j2534_passthru_dlls()):
        print(f"{i}: {dll} ")
