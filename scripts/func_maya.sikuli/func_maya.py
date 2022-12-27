from sikuli import * 
import img #import images
import func #import common functions
import subprocess #needed for calling installer/uninstaller
from subprocess import Popen, PIPE #needed to get output from external python scripts
import shutil
import zipfile # needed for extraction files for ZIP installation
import os #needed to set environment variables

####################-VRAY-GUI-INSTALL-###################

def installVRayMayaGui(build):
    Debug.user("Installing %s" %(build.split("\\")[2]))
    Do.popup( build ,"Installing ...", 1)
    App.open(build)
    wait(img.cg_maya_install_win,15)
    wait(2)
    click(img.cg_install_I_accept)
    wait(2)
    click(img.cg_install_next)
    wait(2)
    click(img.cg_share_analitisc_data)
    wait(img.cg_install_finish,120)
    click(img.cg_install_finish)
    wait(5)

####################-VRAY-ZIP-INSTALL-###################

def installVRayMayaZip(build,vray_zip_path):
    Do.popup("Might take a while", "Extracting Archive...", 2)
    print('Extracting archive')
    zip_ref = zipfile.ZipFile(build, 'r')
    zip_ref.extractall(vray_zip_path)
    zip_ref.close()
    print('Extract completed')
   
def setVrayMayaEnvVars(maya_version,vray_zip_path):
    my_env = os.environ.copy() 
    my_env['MAYA_RENDER_DESC_PATH'] = vray_zip_path + r'\maya_root\bin\rendererDesc'   
    my_env['VRAY_FOR_MAYA' + maya_version +'_MAIN'] = vray_zip_path + r'\maya_vray'
    my_env['VRAY_FOR_MAYA' + maya_version +'_PLUGINS'] = vray_zip_path + r'\maya_vray\vrayplugins'
    my_env['VRAY_AUTH_CLIENT_FILE_PATH'] = r'C:\Program Files\Common Files\ChaosGroup'
    my_env['VRAY_OSL_PATH_MAYA' + maya_version] = vray_zip_path + r'\vray\opensl'
    my_env['PATH'] = vray_zip_path + r'\maya_root\bin;' + my_env['PATH']
    
    ##Try Except is needed cause variables might or might not exist. If exists the new value is appended to varible if not new value is assigned to variable.
    try:
        my_env['MAYA_PLUG_IN_PATH'] = vray_zip_path + r'\maya_vray\plug-ins;' + my_env['MAYA_PLUG_IN_PATH']
    except:
        my_env['MAYA_PLUG_IN_PATH'] = vray_zip_path + r'\maya_vray\plug-ins'    
        
    try:
        my_env['MAYA_SCRIPT_PATH'] = vray_zip_path + r'\maya_vray\scripts;' + my_env['MAYA_SCRIPT_PATH']
    except:
        my_env['MAYA_SCRIPT_PATH'] = vray_zip_path + r'\maya_vray\scripts'
    
    try:
        my_env['PYTHONPATH'] = vray_zip_path + r'\maya_vray\scripts;' + my_env['PYTHONPATH']
    except:
        my_env['PYTHONPATH'] = vray_zip_path + r'\maya_vray\scripts'

    try:
        my_env['XBMLANGPATH'] = vray_zip_path + r'\maya_vray\icons;' + my_env['XBMLANGPATH']
    except:
        my_env['XBMLANGPATH'] = vray_zip_path + r'\maya_vray\icons'

    #this one is for V-Ray Standalone
    try:
        my_env['VRAY_PLUGINS'] = vray_zip_path + r'\maya_vray\vrayplugins;' + my_env['VRAY_PLUGINS']
    except:
        my_env['VRAY_PLUGINS'] = vray_zip_path + r'\maya_vray\vrayplugins'
    
    printVrayEnvVars(maya_version,my_env)
    return my_env


def printVrayEnvVars(maya_version,my_env):
    print ('MAYA_RENDER_DESC_PATH = '),
    print (my_env['MAYA_RENDER_DESC_PATH'])

    print ('VRAY_FOR_MAYA' + maya_version +'_MAIN = '),
    print my_env['VRAY_FOR_MAYA' + maya_version +'_MAIN']

    print ('VRAY_FOR_MAYA' + maya_version +'_PLUGINS = '),
    print my_env['VRAY_FOR_MAYA' + maya_version +'_PLUGINS']

    print ('VRAY_OSL_PATH_MAYA' + maya_version +' = '),
    print my_env['VRAY_OSL_PATH_MAYA' + maya_version]

    print ('PATH = '),
    print my_env['PATH']

    print ('MAYA_PLUG_IN_PATH = '),
    print my_env['MAYA_PLUG_IN_PATH'] 

    print ('MAYA_SCRIPT_PATH = '),
    print my_env['MAYA_SCRIPT_PATH']

    print ('PYTHONPATH = '),
    print my_env['PYTHONPATH']

    print ('XBMLANGPATH = '),
    print my_env['XBMLANGPATH']

    print ('VRAY_AUTH_CLIENT_FILE_PATH = '),
    print my_env['VRAY_AUTH_CLIENT_FILE_PATH']

    print ('VRAY_PLUGINS = '),
    print my_env['VRAY_PLUGINS']

    
####################-MAYA--###################

def melCommand(command):
    paste(img.maya_mel_script, command)
    wait(1)
    type(Key.ENTER)


def startMaya(maya_version, vray_zip_env_var = None):   
    cmd = 'python ' + '"' + getParentFolder() + 'get_maya_registry.py' + '" ' + maya_version 
    p = Popen(cmd, stdout=PIPE)
    mayaExecutable = p.communicate()[0].strip('\n')[:-1]
    
    if vray_zip_env_var == None:
        App.open(mayaExecutable)
    else:
        subprocess.Popen(mayaExecutable, env=vray_zip_env_var)
    wait(img.maya_timeline,300)
    
    #Do.popup(func.getJoke(),"Waiting 30s to load Maya modules...",30)
    print("startMaya end")
    
def resetScene():
    #reset Scene
    melCommand('file -f -new')
    #melCommand('vray hideVFB')
    
    
def loadVray():
    melCommand('loadPlugin "vrayformaya.mll"')
    Do.popup( "Loading V-Ray plugin..." ,"Waiting 10s ...",10)
    #set V-Ray as current renderer: https://around-the-corner.typepad.com/adn/2016/09/setting-up-maya-hardware-20-using-melpython.html
    melCommand("setCurrentRenderer vray")
    # displaying render settings window - needed to fully load vraySettings node.
    #melCommand('unifiedRenderGlobalsWindow') 
    wait(1)
    #melCommand('deleteUI unifiedRenderGlobalsWindow')
    #set render time
    wait(1)
    #melCommand('setAttr "vraySettings.progressiveThreshold" 0')
    #melCommand('setAttr "vraySettings.progressiveMaxTime" 0.1')


def createScene():
    #createbox
    melCommand("polyCube -w 5 -h 5 -d 5 -sx 1 -sy 1 -sz 1 -ax 0 1 0 -cuv 4 -ch 1")
    #create DomeLight
    melCommand("select -r `shadingNode -asLight VRayLightDomeShape`")


def saveImage(build,name):
    melCommand('vray vfbControl -saveimage "' + build.replace('\\','\\\\') + '_' + name + '.jpg"')
 
####################-VRAY-MAYA-RENDERING-###################
def renderVrayCPU(build):
    #render with V-Ray CPU: vrend -help
    Do.popup( "Rendering with V-Ray CPU engine" ,"Working on ...", 1)
    Debug.user("Rendering with V-Ray CPU engine")
    melCommand("vrend")
    #func.getLicense()
    wait(10)
    wait(img.vray_vfb_stopped,15)
    saveImage(build,"cpu")
    melCommand('vray hideVFB')
    wait(2)
    
def renderVrayGPU(build):
    #render with V-Ray CUDA engine
    Do.popup( "Rendering with V-Ray CUDA engine" ,"Working on ...", 1)
    Debug.user("Rendering with V-Ray CUDA engine")
    melCommand('setAttr "vraySettings.productionEngine" 2')
    melCommand("vrend")
    #func.getLicense()
    #wait VFB Stop button to appear and disappear to ensure rendering is completed
    wait(img.vray_vfb_stop,5)
    waitVanish(img.vray_vfb_stop,20)
    #wait(5)
    saveImage(build,'cuda')
    melCommand('vray hideVFB')
    wait(2)

def renderVrayIPRwindow(build, name): 
    #function is used for both CPU and CUDA rendering, the engine is switched by the renderVrayCPU and renderVRayGPU functions
    Do.popup( "Rendering with V-Ray IPR Window" ,"Working on ...", 1)
    Debug.user("Rendering with V-Ray IPR Window")
    melCommand('IPRRenderIntoNewWindow')
    #func.getLicense()
    wait(5)
    click(img.vray_vfb_stop)
    wait(1)
    saveImage(build,name)
    melCommand('vray hideVFB')
    wait(2)

def renderVrayIPRviewport(build, name):
    #function is used for both CPU and CUDA rendering, the engine is switched by the renderVrayCPU and renderVRayGPU functions
    Do.popup( "Rendering with V-Ray IPR Viewport" ,"Working on ...", 1)
    Debug.user("Rendering with V-Ray IPR Viewport")
    click(img.vray_maya_ipr_viewport)
    #func.getLicense()
    wait(3)
    screenshot = capture(SCREEN)
    shutil.move(screenshot, build + '_' + name +'.jpg')
    click()
    wait(2)

def exportVrscene(build):
    Do.popup( "Exporting .vrscene for Standalone rendering" ,"Working on ...", 1)
    Debug.user("Exporting .vrscene for Standalone rendering")
    #disable rendering
    melCommand('setAttr "vraySettings.vrscene_render_on" 0;')
    #enable vrscene exporter
    melCommand('setAttr "vraySettings.vrscene_on" 1')
    #set path
    #popup('setAttr -type "string" vraySettings.vrscene_filename "' + build.replace('\\','\\\\') + '.vrscene"')
    melCommand('setAttr -type "string" vraySettings.vrscene_filename "' + build.replace('\\','\\\\') + '.vrscene"')
    melCommand('vrend')
    wait(2)

####################-VRAY-STANDALONE-RENDERING-###################

def renderStd(maya_version, build, rtengine):
    #cmd = 'python ' + '"' + getParentFolder() + 'get_maya_registry.py' + '" ' + maya_version 
    #p = Popen(cmd, stdout=PIPE)
    #vrayStandalone = p.communicate()[0].strip('\n')[:-1] + r'vray\bin\vray.exe'
    #vrayStandalone = r"C:\Program Files\Chaos Group\V-Ray\Maya 2023 for x64\maya_vray\bin\vray.exe"
    vrayStandalone = r"C:\ProgramData\Autodesk\ApplicationPlugins\VRay3dsMax2023\bin\vray.exe"
    Debug.user(vrayStandalone)
    Do.popup("Rendering with V-Ray Standalone" + rtengine + '\n' + vrayStandalone ,"Working on ...", 2)
    Debug.user("Rendering with V-Ray Standalone")
    
    arg1=vrayStandalone
    arg2=r'-scenefile="' + build + '.vrscene"'
    arg3='-autoclose=1'
    arg4=rtengine
    arg5= '-imgFile="' + build + rtengine +'.jpg"'
    #print(arg1,arg2,arg3,arg4,arg5,arg6,arg7)
    print(arg1)
    print(arg2)
    print(arg3)
    print(arg4)
    print(arg5)
    renderProcess = subprocess.Popen([arg1,arg2,arg3,arg4,arg5]) #.popen command will just start rendering and will continue with the rest of the code 
    #wait(img.vray_vfb_stop,10)
    wait(10)
    #func.getLicense()
    renderProcess.wait()
    Debug.user("V-Ray Standalone Rendering completed")

def renderStdZip(maya_version, build, rtengine, vray_zip_env_var,vray_zip_path):
    vrayStandalone = vray_zip_path + r'\maya_vray\bin\vray.exe'
    Debug.user(vrayStandalone)
    print vrayStandalone
    Do.popup("Rendering with V-Ray Standalone" + rtengine + '\n' + vrayStandalone ,"Working on ...", 1)
    Debug.user("Rendering with V-Ray Standalone")
    
    arg1=vrayStandalone
    arg2=r'-scenefile="' + build + '.vrscene"'
    arg3='-autoclose=1'
    arg4=rtengine
    arg5= '-imgFile=' + build + rtengine +'.jpg'
    renderProcess = subprocess.Popen([arg1,arg2,arg3,arg4,arg5], env=vray_zip_env_var)
  
    wait(img.vray_vfb_stop,10)
    #func.getLicense()
    renderProcess.wait()
    Debug.user("V-Ray Standalone Rendering completed")
    
####################-ZIP-INSTALLATION-###################

    
#Debug.user("Maya %s started" %version)


    