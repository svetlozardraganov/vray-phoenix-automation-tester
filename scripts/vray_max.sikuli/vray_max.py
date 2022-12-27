from sikuli import * 
import os #needed of OS-operations like getting parrent dir etc.
import socket #needed to get PC-name and IP-address
import func #import fuctions
import func_max
import sys #needed to get sys.argv arguments
import subprocess



#this try:except block is used to define where builds and buildsDir variables are taken from. If try code is executed variables are taken from sys.argv of .bat file, if not they are hardcoded into except block.
try:
    builds = sys.argv #get builds as list as sys.argv arguments from drag and drop operation to .bat file
    builds = builds[1:] #remove first argument, it's not needed since it's this script
    buildDirSeparator = builds[0].rfind('\\') # get right most separator in order to split builds dir path. example: D:\builds-->\<--vray_adv_41001_max2019_x64.exe
    buildsDir = builds[0][:buildDirSeparator] # get builds directory
except:
    buildsDir = r"C:\builds" #directory where builds are located
    
#send_mail_script = 'send_email.py' #python 2 script that sends email after test completion

#func_max.ftp_download(buildsDir)
#wait(5)

###################GLOBAL-SETTINGS###################
Settings.MinSimilarity = 0.97
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


###################START-SIKULI-JOB###################

try:
    #App.close("3dsmax.exe") #doesn't always work
    func_max.close3dsMax()
    #check if builds variable is alredy defined, i.e. builds are taken from sys.argv parameter via drag and drop arguments.
    #if variable is emply get the builds from the hardcoded buildsDir variable
    if not builds:
        builds = func.getBuilds(buildsDir,'.exe') #get a list of builds
        
    
    #LOOP THROUGH ALL THE BUILDS IN THE INPUT FOLDER (buildsDir)
    for build in builds:
        vray_version =build[build.find('_adv_')+5] #build.split("_")[2][0] #get VRay version   
        max_version = build[build.find('_max')+4 : build.find('_max')+8] #build.split("_")[3][3:] #get 3dsMax version

        build_type = func.buildType(build)

        func_max.installVrayGui(build)
        # func.closeBrowser()
        func_max.start3dsMax(max_version)        
        func_max.MaxCreateBasicScene(max_version)
                
        func_max.renderVrayCpu(build,max_version)
        func_max.renderVrayIprCpu(build)
        func_max.renderVrayCuda(build, max_version)
        func_max.renderVrayIprCuda(build)
        wait(5)
        #App.close("3dsmax.exe") #doesn't always work
        func_max.exportVrscene(build)       
        func_max.close3dsMax()

        func_max.renderStd(max_version,build,'-rtengine=0')
        func_max.renderStd(max_version,build,'-rtengine=1')
        func_max.renderStd(max_version,build,'-rtengine=5')

        
    Do.popup( "Test completed sucessfully" ,"Completed ...", 2)
       
except:
    Do.popup( "Something went wrong" ,"ERROR ...", 2)

#wait(5)

#func.sendEmail(send_mail_script,buildsDir)

###################TO-DO###################
# find a way to continue test if something fails.
# better way to check if 3dsmax is ready for using, right now it waits 30s after right-down toolbar is found
# improove browser minimizing after phoenix installation - it doesnt work every time
# run script on virtual machine
