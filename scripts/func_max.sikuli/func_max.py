from sikuli import * 
import os #needed of OS-operations like getting parrent dir etc.
import img #import images
import func #import fuctions
import subprocess
from subprocess import Popen, PIPE #needed to get output from external python scripts

popuptime = 1

####################-FTP-###################

def ftp_download(buildsDir):
    print('Start ftp_download')
    cmd = 'python ' + '"' + getParentFolder() + 'ftp_download.py' + '" ' + buildsDir
    p = Popen(cmd, stdout=PIPE, bufsize=1)
    #the following block of code gets output from external script for downloading and extracting builds and print it
    with p.stdout:
        for line in iter(p.stdout.readline, b'',):
            print line,
    p.wait()

####################-3DSMAX-###################

    
def start3dsMax(version):   
    print("")
    Debug.user("Start start3dsMax")

    #maxExecutable = (os.getenv('ADSK_3DSMAX_x64_' + version)) + "3dsmax.exe"
    cmd = 'python ' + '"' + getParentFolder() + 'get_3dsmax_registry.py' + '" ' + version   
    p = Popen(cmd, stdout=PIPE)
    maxExecutable = p.communicate()[0].strip('\n')[:-1] + '3dsmax.exe'
    Do.popup( maxExecutable ,"Lauching ...", popuptime)
    App.open(maxExecutable)
    wait(img.max_viewport,300)

    #Do.popup(func.getJoke(),"Waiting 30s to load 3dsMax modules...",30)

    mouseMove(img.max_script_mini)
    while True:
        rightClick(getLastMatch())
        if exists(img.max_listener_menu,0):
            click(atMouse())
            break
        wait(1)
    
    changeMaxIniSettings()
    Debug.user("3ds Max %s started" %version)

def close3dsMax():
    #App.close("3dsmax.exe")
    os.system('taskkill /f /im 3dsmax.exe')
    Debug.user("3ds Max closed")

def maxScript(cmd):
    wait(0.4)
    paste(img.max_script_mini, cmd)
    wait(0.4)
    type(Key.ENTER)
    wait(0.4)


def changeMaxIniSettings():
    maxScript("iniFile = getMAXIniFile()")
    maxScript('setINISetting iniFile "MAXScript" "EnableMacroRecorder" "0"')
    maxScript('setINISetting iniFile "RenderProgressDialogPosition" "Dimension" "1297 131 387 244"')
    
def MaxCreateBasicScene(max_version):
    Debug.user("Start MaxCreateBasicScene")
    maxScript("resetMaxFile(#noPrompt)")
    wait(2)
    maxScript("VRayLight type:1 multiplier:1")   
    maxScript("Box lengthsegs:1 widthsegs:1 heightsegs:1 length:25 width:25 height:25 mapcoords:on pos:[0,0,0] isSelected:off")



###################-VRAY-###################

def installVrayGui(build):
        Debug.user("Installing %s" %build)
        Do.popup( build ,"Installing ...", popuptime)
        App.open(build)      
        wait(img.cg_max_install_win,60)
        click(img.cg_install_I_accept)
        click(img.cg_install_next)
        click(img.cg_share_analitisc_data)
        wait(img.cg_install_finish,200)
        click(img.cg_install_finish)
        wait(3)
        App.close('vrlservice_installer.exe')
        

def renderVrayCpu(build, max_version):
    Debug.user("V-Ray for 3dsMax CPU Rendering started")
    Do.popup( "V-Ray for 3dsMax CPU" ,"Rendering ...", popuptime)
    maxScript("renderers.current=Vray()")
    wait(4)
    maxScript('vfbControl #pos "reset"')
    maxScript("renderers.current.progressive_max_render_time=0.1")
    maxScript("renderers.current.progressive_noise_threshold=0")    
    maxScript("max quick render") 
    wait(1)
    #func.getLicense()
    waitVanish(img.vray_vfb_stop,60)
    maxScript('vfbControl #saveimage ' + "\"" + build + ".jpg\"")
    maxScript("vfbControl #show false")
    wait(5)
    Debug.user("V-Ray CPU Rendering completed")


def renderVrayIprCpu(build):
    Debug.user("V-Ray for 3dsMax IPR CPU Rendering started")
    Do.popup( "V-Ray for 3dsMax IPR CPU" ,"Rendering ...", popuptime)
    maxScript("renderers.current=Vray()")
    wait(4)
    maxScript("vrayStartIPR()")
    wait(img.vray_vfb_stop,10)
    #func.getLicense()   
    moveMouseWhileIpr()  
    maxScript("vrayStopIPR()")
    maxScript('vfbControl #saveimage ' + "\"" + build + "_IPR_CPU.jpg\"")
    maxScript("vfbControl #show false")
    Debug.user("V-Ray IPR Rendering completed")
    

def renderVrayCuda(build, max_version):
    Debug.user("V-Ray for 3dsMax CUDA Rendering started")
    Do.popup( "V-Ray for 3dsMax CUDA" ,"Rendering ...", popuptime)
    maxScript("renderers.current=VrayRT()")
    wait(4)
    maxScript("renderers.current.engine_type=2")
    maxScript("renderers.current.aa_threshold=0")
    maxScript("renderers.current.max_render_time=0.1")
    
    #click(img.max_render_btn[max_version])
    maxScript("max quick render") 
    wait(img.vray_vfb_stop,120)
    #func.getLicense()
    waitVanish(img.vray_vfb_stop,120)
    maxScript('vfbControl #saveimage ' + "\"" + build + "_CUDA.jpg\"")
    maxScript("vfbControl #show false")
    Debug.user("V-Ray CUDA Rendering completed")

def renderVrayIprCuda(build):
    Debug.user("V-Ray for 3dsMax IPR CUDA Rendering started")
    Do.popup( "V-Ray for 3dsMax IPR CUDA" ,"Rendering ...", popuptime)
    maxScript("renderers.current=VrayRT()")
    wait(4)
    maxScript("vrayStartIPR()")
    wait(img.vray_vfb_stop,10)
    #func.getLicense()
    moveMouseWhileIpr()    
    maxScript("vrayStopIPR()")
    maxScript('vfbControl #saveimage ' + "\"" + build + "_IPR_CUDA.jpg\"")
    maxScript("vfbControl #show false")
    Debug.user("V-Ray IPR Rendering completed")

def exportVrscene(build):
    maxScript("renderers.current=VrayRT()")
    wait(4)
    maxScript('vrayExportRTScene  '+ "\"" + build + ".vrscene\"")
    print('vrayExportRTScene  '+ "\"" + build + ".vrscene\"")
    wait(3)

def moveMouseWhileIpr():
    pos_middle_perspective = Location(1300, 700)
    mouseMove(pos_middle_perspective)
    Settings.MoveMouseDelay = 3
    mouseDown(Button.MIDDLE)
    mouseMove(pos_middle_perspective.offset(250,0))
    mouseMove(pos_middle_perspective.offset(-250,0))
    mouseMove(pos_middle_perspective)
    mouseUp()
    Settings.MoveMouseDelay = 0.5

def renderStd(max_version,build,rtengine):
    Debug.user("V-Ray Standalone Rendering started: %s"%rtengine)
    Do.popup( ("V-Ray Standalone %s"%rtengine) ,"Rendering ...", popuptime)
    #vrayUninstallPath = func.getVrayMaxInstallPath(max_version, 'path') #example: "C:\Program Files\Chaos Group\V-Ray\3ds Max 2019\uninstall\installer.exe"
    #vrayInstallPath = vrayUninstallPath[1:vrayUninstallPath.find(max_version)+4] #example: C:\Program Files\Chaos Group\V-Ray\3ds Max 2019
    #vrayStandalone = vrayInstallPath + r"\bin\vray.exe" #example C:\Program Files\Chaos Group\V-Ray\3ds Max 2019\bin\vray.exe
    vrayStandalone = r"C:\ProgramData\Autodesk\ApplicationPlugins\VRay3dsMax" + max_version + r"\bin\vray.exe" #C:\ProgramData\Autodesk\ApplicationPlugins\VRay3dsMax2023\bin
    arg1=vrayStandalone
    arg2=r'-scenefile="' + build + '.vrscene"'
    arg3='-autoclose=1'
    arg4=rtengine
    arg5= '-imgFile=' + build + rtengine +'.jpg'
    print[arg1,arg2,arg3,arg4,arg5]
    #subprocess.call([arg1,arg2,arg3,arg4,arg5]) #.call command will wait process to finish   
    renderProcess = subprocess.Popen([arg1,arg2,arg3,arg4,arg5]) #.popen command will just start it and will continue with the rest of the code  
    wait(img.vray_vfb_stop,10)
    #func.getLicense()
    #wait(1)
    renderProcess.wait()
    Debug.user("V-Ray Standalone Rendering completed")