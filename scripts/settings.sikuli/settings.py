from sikuli import * 
import os #needed of OS-operations like getting parrent dir etc.
import socket #needed to get PC-name and IP-address
from main import buildsDir

###################GLOBAL-SETTINGS###################
Settings.MinSimilarity = 0.85
#Settings.SlowMotionDelay = 0.1
#Settings.Highlight = True

Settings.UserLogs = True
Settings.UserLogPrefix = os.environ['COMPUTERNAME'] + '_' + socket.gethostbyname(socket.gethostname()) #PCname and IPaddress
Settings.UserLogTime = True
Debug.setUserLogFile(buildsDir + "\\userLog.txt")

Debug.on(3) 
Settings.ActionLogs = True
Settings.InfoLogs = True
Settings.DebugLogs = True
Settings.LogTime = True
Debug.setLogFile(buildsDir + "\\actionLog.txt")
