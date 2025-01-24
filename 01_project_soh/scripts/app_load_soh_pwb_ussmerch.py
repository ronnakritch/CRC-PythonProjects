import pyautogui
import time
import subprocess
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(project_root)

from configs.parameter_soh_pwb_ussmerch import PWB
def wait_for_color_change(initial_color, desired_color, position, sequence):
    while True:
        current_color = pyautogui.pixel(position[0], position[1])
        
        if current_color == desired_color:
            time.sleep(10)
            perform_actions(sequence)
            print(f"Color changed to {desired_color}. Sequence {sequence} executed.")
            break
        elif current_color != initial_color:
            print(f"Color has changed from {initial_color}, but not to {desired_color}. Current color: {current_color}")
        else:
            print(f"Waiting... Current color: {current_color}")
        time.sleep(5)  

def perform_actions():
    time.sleep(1) 
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('tab') #step1
    pyautogui.press('tab') #step2
    pyautogui.press('tab') #step3
    pyautogui.press('tab') #step4
    pyautogui.press('tab') #step5
    pyautogui.press('tab') #step6
    pyautogui.press('tab') #step7
    pyautogui.press('tab') #step8
    pyautogui.press('tab') #step9
    pyautogui.press('tab') #step10
    pyautogui.press('down') #select down to dropdown
    pyautogui.press('down') #select 1st outlet
    pyautogui.press('enter')
    pyautogui.press('tab') #step1
    pyautogui.press('tab') #step2
    pyautogui.press('tab') #step3
    pyautogui.press('tab') #step4
    pyautogui.press('tab') #step5
    pyautogui.press('tab') #step6
    pyautogui.press('tab') #step7
    pyautogui.press('tab') #step8
    pyautogui.press('tab') #step9
    pyautogui.hotkey('ctrl', 'c') #copy branch name
    pyautogui.hotkey('alt', 'e') #export
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'v') #paste branch name to save as file
    pyautogui.press('enter')
    time.sleep(1)                               


upfront_path = r"C:\Program Files (x86)\Upfront\USSMerchPWB\USSMerchPWB.exe"
subprocess.Popen(upfront_path, shell=True)
time.sleep(10)
#login
pyautogui.write(PWB['pass']) 
pyautogui.press('tab')
pyautogui.press('enter')

#outlet menu select
time.sleep(30)
pyautogui.hotkey('alt', 'B') #รายงาน
time.sleep(1)
pyautogui.press('B') 
time.sleep(1)
pyautogui.press('6') #รายงาน Inventory
time.sleep(1)
pyautogui.press('A') #Inventory Value Daily Report
time.sleep(30)

pyautogui.press('down') #select down to dropdown
pyautogui.press('down') #select 1st outlet
pyautogui.press('enter')
pyautogui.press('tab') #step1
pyautogui.press('tab') #step2
pyautogui.press('tab') #step3
pyautogui.press('tab') #step4
pyautogui.press('tab') #step5
pyautogui.press('tab') #step6
pyautogui.press('tab') #step7
pyautogui.press('tab') #step8
pyautogui.press('tab') #step9
pyautogui.hotkey('ctrl', 'c') #copy branch name
pyautogui.hotkey('alt', 'e') #export
time.sleep(2)
pyautogui.hotkey('ctrl', 'v') #paste branch name to save as file
pyautogui.press('enter')
time.sleep(2)

# Define the initial color, desired color, and position
initial_color = (255, 0, 0) #red
desired_color = (244, 244, 244) #gray
position = (900, 200) #position color load tab

# Loop over sequences from 2 to 36
for i in range(2, 410):
    wait_for_color_change(initial_color, desired_color, position)

#close upfront
pyautogui.hotkey('alt', 'f4')
pyautogui.hotkey('alt', 'f4')
pyautogui.hotkey('alt', 'f4')
pyautogui.press('left')
pyautogui.press('enter')

import shutil
import os

def copy_all_files(params):
    raw_folder = params["raw_file"]
    old_folder = params["old_file"]
    
    if not os.path.exists(old_folder):
        os.makedirs(old_folder)

    for filename in os.listdir(raw_folder):
        source_file = os.path.join(raw_folder, filename)
        destination_file = os.path.join(old_folder, filename)

        # Copy each file
        if os.path.isfile(source_file):
            shutil.copy(source_file, destination_file)
            print(f"Copied: {source_file} to {destination_file}")

params = {
    "raw_file": r"C:\11_Python\01_project_soh\data\input\SSPWDS",
    "old_file": r"C:\11_Python\01_project_soh\data\input\SSPWDS\backup"
}

copy_all_files(params)