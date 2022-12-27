import winreg
import sys

try:
    version = sys.argv[1]
except:
    version = '2023'

def getVrayversion():
    result = {}
    try:
        # Open the key and return the handle object.
        hKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                              "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\V-Ray for 3dsmax "+version+" for x64")
                              
        # Read the values.                      
        result['ver'] = winreg.QueryValueEx(hKey, "DisplayVersion")[0].encode('utf-8')
        result['path'] = winreg.QueryValueEx(hKey, "DisplayIcon")[0].encode('utf-8')

        # Return only the value from the resulting tuple (value, type_as_int).
        return result
    except:
        result['ver'] = False
        result['path'] = False
        return result

print(getVrayversion())
