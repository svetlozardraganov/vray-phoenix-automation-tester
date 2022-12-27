from sikuli import * 
import os #needed of OS-operations like getting parrent dir etc.
import socket #needed to get PC-name and IP-address
import func #import fuctions
import func_max

buildsDir = r"C:\builds" #directory where builds are located
send_mail_script = 'send_email.py' #python 2 script that sends email after test completion


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
    Do.popup( "Start Testing Process!" ,"SikuliX", 2)
    #App.close("3dsmax.exe")
    func_max.close3dsMax()
    builds = func.getBuilds(buildsDir, ".exe") #get a list of builds 
    
    #LOOP THROUGH ALL THE BUILDS IN THE INPUT FOLDER (buildsDir)
    for build in builds:
        version = build.split("_")[3][3:] #get 3dsMax version
        print(version)
        build_type='' #determine if installer is for vray5/vray6

        
        #DETERMINE BUILD TYPE: VRAY5/VRAY6
        if build.find('vray5') !=-1:
            build_type='vray5'
            print("Phoenix Build Type: V-RAY 5")
        elif build.find('vray6') !=-1:
            build_type='vray6'
            print("Phoenix Build Type: V-RAY 6")

        
        
        #INSTALL PROPER VRAY BUILD OR REMOVE VRAY FOR SCANLINE TESTS
        if build_type == 'vray5':
            #CHECK IF CURRENT VERSION IS VRAY5 AND IF NOT INSTALL IT
            Debug.user("Build Type V-Ray 5")
            if func.getVRayFromReg(version, 'ver')==None:
                func.installVray(version,buildsDir,'vray_adv_5')
            elif (func.getVRayFromReg(version, 'ver')[0])!='3':
                func.uninstallVray(version)
                func.installVray(version,buildsDir,'vray_adv_5')
     
            func.installPhoenix(build)
            #func.closeBrowser()
            #func.start3dsMax(version)
            ###func.createVrayScene(version)
            func.createSim(version,'fire')
            func.renderVray(build, version, 'fire')
            func.createSim(version,'beer')
            func.renderVray(build, version, 'beer')
            
        elif build_type == 'vray6':
            #CHECK IF CURRENT VERSION IS VRAY6 AND IF NOT INSTALL IT
            Debug.user("Build Type V-Ray 6")

            vray_version = func.getVrayMaxInstallPath(version, 'ver')
            vray_version = vray_version[0] 
            
            if vray_version!='6':
                Debug.user("V-Ray 6 not installed")
                #func.uninstallVray(version)
                func.installVray(version,buildsDir,'vray_adv_6')
            else:
                Debug.user("V-Ray 6 already installed")
            
            func.installPhoenix(build)

            #func.closeBrowser()
            func_max.start3dsMax(version)
            #func.createVrayScene(version)
            func.createSim(version,'fire')
            func.renderVray(build, version, 'fire')
            func.renderVrayIPR(build, version, 'fire')
            
            func.createSim(version,'beer')
            func.renderVray(build, version, 'beer')
            func.renderVrayIPR(build, version, 'beer')
            
        #elif build_type == 'defscanline':
            ##CHECK IF VRAY IS INSTALLED AND IF IT IS UNINSTALL IT
            #if func.getVRayFromReg(version, 'ver')!=None:
            #    func.uninstallVray(version)
    
            #func.installPhoenix(build)
            #func.closeBrowser()
            #func.start3dsMax(version)
            #func.createSim(version,'fire')
            #func.renderScanline(build, version, 'fire')
            #func.createSim(version,'beer')
            #func.renderScanline(build, version, 'beer')
            
    func_max.close3dsMax()  
    Do.popup( "Test completed sucessfully" ,"Completed ...", 2)
    
except:
    Do.popup( "Something went wrong" ,"ERROR ...", 2)
    exit()

#func.sendEmail(send_mail_script,buildsDir)


###################TO-DO###################
# find a way to continue test if something fails.
# better way to check if 3dsmax is ready for using, right now it waits 30s after right-down toolbar is found
# better way to handle rendering time, right now it is hardcoded but it would be better to look for vanishing of progress win
# improove installation code, sometimes it doesnt work well for the click after I agree btn
# improove browser minimizing after phoenix installation - it doesnt work every time
# video recording
# run script on virtual machine