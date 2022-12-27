from sikuli import * 
import os #needed of OS-operations like getting parrent dir etc.
import socket #needed to get PC-name and IP-address
import func #import fuctions
import func_maya

#buildsDir = r"e:\builds" #directory where builds are located
buildsDir = r"C:\builds"
#send_mail_script = 'send_email.py' #python 2 script that sends email after test completion


###################GLOBAL-SETTINGS###################
Settings.MinSimilarity = 0.95
#Settings.SlowMotionDelay = 0.1
#Settings.Highlight = True

#Settings.UserLogs = True
#Settings.UserLogPrefix = os.environ['COMPUTERNAME'] + '_' + socket.gethostbyname(socket.gethostname()) #PCname and IPaddress
#Settings.UserLogTime = True
#Debug.setUserLogFile(buildsDir + "\\userLog.txt")

Debug.on(3) 
#Settings.ActionLogs = True
#Settings.InfoLogs = True
#Settings.DebugLogs = True
#Settings.LogTime = True
#Debug.setLogFile(buildsDir + "\\actionLog.txt")

###################START-SIKULI-JOB###################
try:
    #App.close("maya.exe")
    builds_exe = func.getBuilds(buildsDir,".exe") #get a list of builds 

    #LOOP THROUGH ALL THE BUILDS IN THE INPUT FOLDER (buildsDir)           
    for build in builds_exe:
        
        maya_version = build[build.find('_maya')+5:build.find('_maya')+9] #get maya version       
        build_type = func.buildType(build) #get build type version  adv/nfr/edu/trial 
        func_maya.installVRayMayaGui(build)
        #func.closeBrowser()
        func_maya.startMaya(maya_version)
        ##func_maya.resetScene()
        func_maya.loadVray()
        func_maya.createScene()
        func_maya.renderVrayCPU(build)     
        func_maya.renderVrayIPRwindow(build, 'ipr_vfb_cpu')
        func_maya.renderVrayIPRviewport(build, 'ipr_viewport_cpu')

        ##Here the engine is switched to cuda with renderVrayGPU function and then same IPR fuctions are used as above
        ##In order to ensure Building Kernels procedure is completed I could run Standalone GPU rendering with wait command first!!!
        func_maya.renderVrayGPU(build)
        func_maya.renderVrayIPRwindow(build, 'ipr_vfb_cuda')
        func_maya.renderVrayIPRviewport(build, 'ipr_viewport_cuda')
        
        func_maya.exportVrscene(build)
        
        func_maya.renderStd(maya_version, build, '-rtengine=0')
        func_maya.renderStd(maya_version,build,'-rtengine=1')
        func_maya.renderStd(maya_version,build,'-rtengine=5')      

        #App.close("maya.exe")
        
    Do.popup( "Test completed sucessfully" ,"Completed ...", 2)
        
except:
    Do.popup( "Something went wrong" ,"ERROR ...", 2)

#func.sendEmail(send_mail_script,buildsDir)

