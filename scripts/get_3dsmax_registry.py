import winreg
import sys
import os

try:
    version = sys.argv[1]
except:
    version = '2023'

def getMaxversion():
    result = {}
    try:
        # Open the key and return the handle object.
        hKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 
                              "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Autodesk 3ds Max " + version)
                              
        # Read the values.                      
        result = _winreg.QueryValueEx(hKey, "InstallLocation")[0].encode('utf-8')
        
        # Return only the value from the resulting tuple (value, type_as_int).
        return result

        
    except:
        #result = False
        result = os.environ['ADSK_3DSMAX_x64_' + version]
        return result
output = getMaxversion()
print(getMaxversion())

# f = open("G:\\My Drive\\GitHub\\Release-Builds-Automatic-Tests\\scripts\\3dsmax_version.txt", "w")
# f.write(output)
# f.close()