import pyautogui
import time
import subprocess

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
        time.sleep(5)  # Add a small delay to reduce CPU usage

def perform_actions(sequence):

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('tab')
    pyautogui.write(str(sequence).zfill(3))
    pyautogui.press('enter')
    pyautogui.hotkey('alt', 'e')
    time.sleep(1)
    pyautogui.write(str(sequence).zfill(3))
    
    pyautogui.press('enter')
    time.sleep(1)

upfront_path = r"C:\Program Files (x86)\Upfront\USSWDS\USSWDS.exe"
subprocess.Popen(upfront_path, shell=True)
time.sleep(10)
#login
pyautogui.press('enter')
pyautogui.press('enter')
pyautogui.press('enter')
#outlet menu select
time.sleep(5)
pyautogui.hotkey('alt', '5')
pyautogui.press('5')

time.sleep(10)
pyautogui.press('down')
pyautogui.press('down')
pyautogui.press('enter')
pyautogui.press('tab')
pyautogui.press('tab')
pyautogui.press('tab')
pyautogui.press('tab')
pyautogui.press('tab')
pyautogui.press('tab')
pyautogui.press('tab')
pyautogui.press('down')
pyautogui.press('down')
pyautogui.press('down')
pyautogui.press('down')
pyautogui.press('enter')
pyautogui.hotkey('alt', 'e')
time.sleep(2)
pyautogui.write('001') #1st sequence
pyautogui.press('enter')
time.sleep(2)

# Define the initial color, desired color, and position
initial_color = (255, 0, 0) #red
desired_color = (171, 171, 171) #gray
position = (800, 200) #position color load tab

# Loop over sequences from 2 to 36
for i in range(2, 37):
    wait_for_color_change(initial_color, desired_color, position, sequence=i)

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
    "raw_file": r"D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\06_RAW_FILE\SOH\SSPWDS",
    "old_file": r"D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\06_RAW_FILE\SOH\SSPWDS\backup"
}

copy_all_files(params)

    