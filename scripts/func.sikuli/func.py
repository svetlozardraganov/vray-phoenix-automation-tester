from sikuli import * 
import os #needed of OS-operations like getting parrent dir etc.
import org.sikuli.basics.FileManager as FM #needed for downloading JSON file from the license server.
import json #needed for parsing JSON file from the License server
import img #import images
import subprocess #needed for calling installer/uninstaller
from subprocess import Popen, PIPE #needed to get output from external python scripts
import ast #needed to convert output from external scripts to dictionary
import operator #needed to sort bulds by two criteria, max version and build type
#import __builtin__ as __builtin__ # python native type() command usage: print(__builtin__.type(stdout))
import func_max

###################GET-LICENSE###################
def getLicense():
    license_status = FM.downloadURLtoString("http://localhost:30304/sessions/online")
    license_json = json.loads(license_status)
    licenses = [] #store license from the following loop command. Note that first item will be empty and will be remove from the filter cmd bellow.
    try:
        for product in license_json:
            interface_lic = product['product']['1']
            render_node_lic = product['product']['2']
            product_name = product['product']['productLabel']
            lic = ''
            if interface_lic and render_node_lic:
                lic = ("LICENSE: %s, Interface: %s, Render: %s" % (product_name, interface_lic, render_node_lic))
            elif interface_lic:
                lic = ("LICENSE: %s, Interface: %s" % (product_name, interface_lic))
            elif render_node_lic:
                lic = ("LICENSE: %s, Render: %s" % (product_name, render_node_lic))
            licenses.append(lic)

        licenses = filter(None, licenses) #remove empty item from the list
        for licence in licenses:
            Debug.user(licence)
            print licence
        Do.popup( "\n".join(licenses) ,"Licence Check...", 2)
    except:
        lic = ('-------------NO-LICENSE-BEING-USED-------------')
        Debug.user(lic)
        print(lic)
        Do.popup( lic ,"Licence Check...", 3)



###################GET-BIULDS###################
def getBuilds(dir,ext):
    Debug.user("getBuilds Started")
    builds = []
    result = []
    for file in os.listdir(dir):
        if file.endswith(ext):
            x = []
            x.append(dir + "\\" + file)
            max_ver = file.split('_')[3]
            x.append(max_ver)
            build_type = file.split('_')[4]
            x.append(build_type)
            builds.append(x)
    builds.sort(key = operator.itemgetter(1, 2), reverse=True) #sort builds by two criterias, max_version and vray_version
    for build in builds:
        result.append(build[0])
    Do.popup("\n".join(result),'Found builds', 2)
    return result


###################DETERMINE BUILD TYPE: ADV/EDU/NFR/TRIAL###################
def buildType(build):
    build_type=''
    if build.find('_adv_') !=-1:
        build_type='adv'
        print("Build Type: %s" %build_type)
    elif build.find('_edu_') !=-1:
        build_type='edu'
        print("Build Type: %s" %build_type)
    elif build.find('_nfr_') !=-1:
        build_type='nfr'
        print("Build Type: %s" %build_type)
    elif build.find('_trial_') !=-1:
        build_type='trial'
        print("Build Type: %s" %build_type)
    return build_type

###################-GET-JOKE-###################
def getJoke():
    vicove = FM.downloadURLtoString("https://vicove.com/sluchaini-vicove")
    strip_left = vicove.find("joke_text") +11
    strip_right = vicove.find("</p>" ,strip_left)
    vic = vicove[strip_left:strip_right]
    vic = vic.strip()
    vic = vic.replace('<br />','')
    return vic

###################PHOENIX-INSTALLATION###################
def installPhoenix(build):
    Debug.user("Installing %s" %(build.split("\\")[2]))
    #App.open('CMD /C ' + build)
    App.open(build)  
    wait(img.phoenixFD_install_win,15)
    click(img.cg_install_I_accept)
    click(img.cg_install_next)
    wait(img.phoenixFD_finish,2000)
    wait(1)
    click(img.phoenixFD_finish)
    wait(3)
    App.close('vrlservice_installer.exe')
    #wait(2)
    #click(img.phoenixFD_I_accept)
    #wait(2)
    #click(img.phoenixFD_next)
    #wait(2)
    #click(img.phoenixFD_install_now)
    #wait(img.phoenixFD_finish,30)
    #if exists(img.phoenixFD_checkbox_enabled,5):
    #    checkboxes = findAll(img.phoenixFD_checkbox_enabled)
    #    for checkbox in checkboxes:
    #        checkbox.click()
    #click(img.phoenixFD_finish)
    wait(3)

###################CLOSE-BROWSER###################
def closeBrowser():
    type(Key.F4, Key.CTRL)
    wait(0.3)
    type(Key.SPACE, KeyModifier.ALT)
    wait(0.3)
    type('n')
    wait(2)


###################CREATE-VRAY-SCENE###################
def createVrayScene(version):
    click(img.max_domelight)
    wait(1)
    click(img.screen_center)
    wait(1)
    rightClick()


###################CREATE-SIMULATION###################
def createSim(version,sim):
    Debug.user("createSim started")
    #resetMaxFile()
    #click(img.max_standard_primitives[version])
    #click(img.max_box)
    #click(img.max_box_keyboard_entry_rollout[version])
    #doubleClick(img.max_box_keyboard_entry[version])
    #type("25")
    #type(Key.TAB)
    #type("25")
    #type(Key.TAB)
    #type("25")
    #click(img.max_box_create)
    func_max.maxScript("resetMaxFile(#noPrompt)")
    func_max.maxScript("Box lengthsegs:1 widthsegs:1 heightsegs:1 length:25 width:25 height:25 mapcoords:on pos:[0,0,0] isSelected:on")
    Debug.user("Simulation started")
    if sim=='beer':
        click(img.phoenix_beer)
        paste(img.max_script_mini, "$.mat = StandardMaterial()")
        wait(0.3)
        type(Key.ENTER)
        wait(0.3)       
    elif sim=='fire':
        click(img.phoenix_fire)
    wait(2)
    click(img.phoenix_start_sim)
    wait(10)
    #getLicense()    
    click(img.phoenix_stop_sim)
    wait(3)
    Debug.user("Simulation completed")
    
###################RENDER-SCENE###################
def renderVray(build, version, sim_preset):
    Debug.user("V-Ray Rendering started")
    if sim_preset == 'beer':
        paste(img.max_script_mini, 'VRayLight invisible:1 type:1 intensityAt:39.3701 webfile:"{00000000-0000-0000-0000-000000000000}" on:on castShadows:on rgb:(color 255 255 255) rgbFilter:(color 255 255 255) intensity:3483.86 kelvin:6500 useKelvin:on intensityType:0 originalintensity:1500 useMultiplier:off multiplier:1 shiftColorWhenDimming:off useFarAttenuation:off displayFarAttenuationGizmo:off startFarAttenuation:80 endFarAttenuation:200 contrast:0 softenDiffuseEdge:0 projector:off affectDiffuse:on affectSpecular:on ambientOnly:off targetDistance:240 light_length:48 light_Width:24 light_Radius:5.5 atmosShadows:off atmosOpacity:100 atmosColorAmt:100 shadowMultiplier:1 shadowColorMapEnable:off shadowColor:(color 0 0 0) lightAffectsShadow:off useGlobalShadowSettings:off hotspot:30 falloff:60 showCone:off xRotation:0 yRotation:0 zRotation:0')
        wait(0.3)
        type(Key.ENTER)
    paste(img.max_script_mini, "renderers.current=Vray()")
    wait(0.3)
    type(Key.ENTER)
    paste(img.max_script_mini, "renderers.current.progressive_max_render_time=0.1")
    wait(0.3)
    type(Key.ENTER)
    #click(img.max_render_btn[version])
    func_max.maxScript("max quick render")
    wait(1)
    #getLicense()
    wait(10)
    output_name = 'vfbControl #saveimage '+ "\"" + build.split(".")[0] + '_' + sim_preset + ".jpg\""
    paste(img.max_script_mini, output_name)
    wait(1)
    type(Key.ENTER)
    wait(5)
    Debug.user("V-Ray Rendering completed")

def renderVrayIPR(build, version, sim_preset):
    Debug.user("V-Ray IPR Rendering started")
    if sim_preset == 'beer':
        paste(img.max_script_mini, 'VRayLight invisible:1 type:1 intensityAt:39.3701 webfile:"{00000000-0000-0000-0000-000000000000}" on:on castShadows:on rgb:(color 255 255 255) rgbFilter:(color 255 255 255) intensity:3483.86 kelvin:6500 useKelvin:on intensityType:0 originalintensity:1500 useMultiplier:off multiplier:1 shiftColorWhenDimming:off useFarAttenuation:off displayFarAttenuationGizmo:off startFarAttenuation:80 endFarAttenuation:200 contrast:0 softenDiffuseEdge:0 projector:off affectDiffuse:on affectSpecular:on ambientOnly:off targetDistance:240 light_length:48 light_Width:24 light_Radius:5.5 atmosShadows:off atmosOpacity:100 atmosColorAmt:100 shadowMultiplier:1 shadowColorMapEnable:off shadowColor:(color 0 0 0) lightAffectsShadow:off useGlobalShadowSettings:off hotspot:30 falloff:60 showCone:off xRotation:0 yRotation:0 zRotation:0')
        wait(0.3)
        type(Key.ENTER)
    paste(img.max_script_mini, "renderers.current=VrayRT()")
    wait(0.3)
    type(Key.ENTER)
    paste(img.max_script_mini, "vrayStartIPR()")
    wait(0.3)
    type(Key.ENTER)
    wait(1)
    #getLicense()
    wait(10)
    paste(img.max_script_mini, "vrayStopIPR()")
    wait(0.3)
    type(Key.ENTER)
    wait(1)
    output_name = 'vfbControl #saveimage '+ "\"" + build.split(".")[0] + '_' + sim_preset + "_IPR.jpg\""
    paste(img.max_script_mini, output_name)
    wait(1)
    type(Key.ENTER)
    wait(5)
    Debug.user("V-Ray IPR Rendering completed")

def renderScanline(build, version , sim_preset):
    Debug.user("Scanline Rendering started")
    paste(img.max_script_mini, "renderers.current=Default_Scanline_Renderer()")
    wait(0.3)
    type(Key.ENTER)
    click(img.max_render_btn[version])
    wait(1)
    getLicense()
    wait(5)
    output_name = 'vfbControl #saveimage '+ "\"" + build.split(".")[0] + ".jpg\""
    paste(img.max_script_mini, "img = getlastrenderedimage()")
    #print("img = getlastrenderedimage()")
    #print("img.filename = " + "\"" + build.split(".")[0] + ".jpg\"")
    wait(0.3)
    type(Key.ENTER)
    paste(img.max_script_mini, "img.filename = " + "\"" + build.split(".")[0] + "_" + sim_preset + ".jpg\"" )
    wait(0.3)
    type(Key.ENTER)
    paste(img.max_script_mini, "save img" )
    wait(0.3)
    type(Key.ENTER)
    Debug.user("Scanline Rendering completed")

###################INSTALL-VRAY-NO-GUI###################
def installVray(version,buildsDir,vray_version): 
    for file in os.listdir(buildsDir + '\\vray'):
        if (file.endswith('.exe') and (version in file) and (vray_version in file)):
            Do.popup("Installing " + file,"Working on...", 2)
            Debug.user("Installing %s" %(file))
            arg1 = buildsDir + '\\vray\\' + file
            arg2 = '-configFile=' + buildsDir + '\\vray\\config.xml'
            arg3 = '-gui=0'
            arg4 = '-quiet=0'
            subprocess.call([arg1, arg2, arg3, arg4])
            
            #p = Popen([arg1, arg2, arg3, arg4], stdout=PIPE)
            #stdout = p.communicate()[0]
            #print stdout
            #exit()
                            


###################GET-VRAY-VERSION###################
def getVrayMaxInstallPath(version, output):
    #version = 3dsMax version, output determines if vray-version or vray-installation-path will be outputted
    #sample usage getVrayMaxInstallPath(version, 'ver') / getVrayMaxInstallPath(version, 'path')
    
    cmd = 'python ' + '"' + getParentFolder() + 'get_vray_max_registry.py' + '" ' + version 
    p = Popen(cmd, stdout=PIPE)
    stdout = p.communicate()[0]
    stdout = ast.literal_eval(stdout)
    vray_current_version = stdout['ver']
    vray_install_path = stdout['path']

    if output == 'ver':
        if stdout['ver']:
            return stdout['ver']
    elif output == 'path':
        if stdout['path']:
            return stdout['path']

###################UNINSTALL-VRAY###################
def uninstallVray(version): 
    
    Do.popup("Unstalling V-Ray " + getVrayMaxInstallPath(version, 'ver') ,"Working on...", 2)
    Debug.user("Unstalling V-Ray %s" %(getVrayMaxInstallPath(version, 'ver')))
    arg1 = getVrayMaxInstallPath(version, 'path')[1:-1]
    arg2 = '-uninstall=' + getVrayMaxInstallPath(version, 'path')[:-14] + 'install.log"'
    arg3 = '-uninstallApp="V-Ray for 3dsmax ' + version + ' for x64"'
    arg4 = '-gui=0'
    subprocess.call([arg1,arg2,arg3,arg4])
    
    #remove leftover files
    wait(1)
    cmd = 'python ' + '"' + getParentFolder() + 'get_3dsmax_registry.py' + '" ' + version 
    p = Popen(cmd, stdout=PIPE)
    vray_leftover_scripts_path = p.communicate()[0].strip('\n')[:-1] + 'scripts\Startup'
    for file in os.listdir(vray_leftover_scripts_path):
       if file.startswith("vray"):
            os.remove(vray_leftover_scripts_path + '\\' +file)
    

            
###################SEND-EMAIL###################
def sendEmail(send_mail_script,buildsDir):
    Debug.user("Sending email")
    wait(2)
    run('py "' + getParentFolder() + send_mail_script + '" "' + buildsDir + '"')

###############################