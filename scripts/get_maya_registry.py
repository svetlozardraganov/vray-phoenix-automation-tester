import winreg
import sys

try:
    version = sys.argv[1]
except:
    version = '2023'

def getMayaversion():
    result = {}
    try:
        # Open the key and return the handle object.
        hKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                              #"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Autodesk Maya " + version)
                              "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{DA66134E-803F-32C7-AB31-F1167D447C1B}")
        # Read the values.                      
        #result = winreg.QueryValueEx(hKey, "InstallLocation")[0].encode('utf-8')
        result = winreg.QueryValueEx(hKey, "DisplayIcon")[0]
        result = str(result)
        # Return only the value from the resulting tuple (value, type_as_int).
        return result
    except:
        result = False
        return result

print(getMayaversion())
