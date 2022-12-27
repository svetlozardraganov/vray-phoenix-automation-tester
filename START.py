#START THIS FILE AS ADMIN (NEEDED FOR PROPER SIKULIX FUNTIONING)
import subprocess
import os
import ctypes

buildsDir = r"C:\builds" #directory where builds are located

#check if this process is started as Admin or not
run_as_admin = ctypes.windll.shell32.IsUserAnAdmin()
if run_as_admin != 1:
    print("SikuliX requires Admin priviligies to funtion properly!\nPlease start this process as Admin!")
    exit()

#get this script location
script_dir = os.path.dirname(os.path.realpath(__file__))

#start video recording process
ffmpeg_cmd = [script_dir+ r'\scripts\ffmpeg.exe', '-y', '-rtbufsize', '100M', '-f', 'gdigrab', '-framerate', '24', '-i', 'desktop', '-b', '3000k', '-vcodec', 'libx264', buildsDir + r'\recording.avi']
video_capture = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=None, stderr=None, close_fds=False)

#start sikulix script process
#VRAY-MAX
#proc = subprocess.Popen(["java", "-jar", script_dir + r"\sikuli\sikulixide-2.0.5.jar", "-r", script_dir + r"\scripts\vray_max.sikuli"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#VRAY-PHOENIX
#proc = subprocess.Popen(["java", "-jar", script_dir + r"\sikuli\sikulixide-2.0.5.jar", "-r", script_dir + r"\scripts\phoenix_max.sikuli"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#VRAY-MAYA
proc = subprocess.Popen(["java", "-jar", script_dir + r"\sikuli\sikulixide-2.0.5.jar", "-r", script_dir + r"\scripts\vray_maya.sikuli"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# # Wait sikulix process to complete
out, err = proc.communicate()

# Print sikulix output
print(out)
print(err)

#stop video recording process
video_capture.communicate(input='q'.encode()) #STOP RECORDING
