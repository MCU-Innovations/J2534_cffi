try:
    import winreg
except:
    winreg = None

def __find_j2534_passthru_dlls(base_key):
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
                tool_list.append([name, function_library])
                tool_info.append([idx, vendor, name, function_library])
                j2534_registry_info.append(tool_info)
    except Exception as err:
        if __debug__:
            print("j2535_cffi", err)
    return tool_list


def _find_j2534_passthru_dlls_wow6432():
    try:
        if winreg:
            base_key = winreg.OpenKeyEx(
                winreg.HKEY_LOCAL_MACHINE,
                r"Software\\WOW6432Node\\PassThruSupport.04.04\\",
                access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
            )
            return __find_j2534_passthru_dlls(base_key)
    except Exception as err:
        if __debug__:
            print("j2535_cffi", err)
    return []


def _find_j2534_passthru_dlls():
    try:
        if winreg:
            base_key = winreg.OpenKeyEx(
                winreg.HKEY_LOCAL_MACHINE, r"Software\\PassThruSupport.04.04\\"
            )
            return __find_j2534_passthru_dlls(base_key)
    except Exception as err:
        if __debug__:
            print("j2535_cffi", err)
    return []


def find_j2534_passthru_dlls():
    device_list = {}
    for device in _find_j2534_passthru_dlls_wow6432() + _find_j2534_passthru_dlls():
        if device[1] not in device_list:
            device_list[device[1]] = device
    return list(device_list.values())


if __name__ == "__main__":
    for i, dll in enumerate(find_j2534_passthru_dlls()):
        print(f"{i}: {dll}")
