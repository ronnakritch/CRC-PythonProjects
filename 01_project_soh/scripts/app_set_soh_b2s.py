import pyautogui #click and keyboard
import time #time command(i.e. time delay)
import subprocess
from datetime import datetime, timezone, timedelta
from AppOpener import open

import sys
import os
# Dynamically add the project root to the module search path
script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
project_root = os.path.abspath(os.path.join(script_dir, ".."))  # One level up (project root)
sys.path.append(project_root)  # Add project root to sys.path

from configs.parameter_soh_jda import B2S_parameter  # importing parameters

user_name = B2S_parameter["user"]
pass_word = B2S_parameter["pass"]

# Define the file path
time.sleep(5)
subprocess.Popen([r"D:\TEMP TEMP\JDA AS400\CA_V7R1_SP49800 win10_win7\Icon JDA_Win10\CRC2.ws"], shell=True)
time.sleep(30)

# Key write to log in to JDA
pyautogui.write(user_name) #write id
pyautogui.press('tab')  #tab for login4
pyautogui.write(pass_word) #write pass
pyautogui.press('tab')  #tab for login5
pyautogui.press('enter')  # enter step1
time.sleep(5)

pyautogui.write(user_name) #write id
pyautogui.press('tab')  #tab for login4
pyautogui.write(pass_word) #write pass
pyautogui.press('enter')  # enter step1
time.sleep(1)
pyautogui.press('enter')  # enter step2
time.sleep(1)
pyautogui.press('enter')  # enter step3
time.sleep(1)
pyautogui.press('enter')  # enter step4
time.sleep(1)
pyautogui.press('enter')  # enter step5


#select data category
time.sleep(1)
pyautogui.write('18') 

#set parameter to import
time.sleep(1)
pyautogui.press('enter')  #select all store

utc_dt = datetime.now(timezone.utc) - timedelta(days=1) # Get the current datetime in UTC - 1day
format_utc_dt = utc_dt.strftime("%d%m%y") # Format the datetime in "ddmmyyyy"
pyautogui.write(format_utc_dt) #write date
pyautogui.press('delete') #del step1
pyautogui.press('delete') #del step2
pyautogui.press('enter')

pyautogui.write('3')  #select all sku type 
pyautogui.press('tab') #scroll down 1
pyautogui.press('tab') #scroll down 2
pyautogui.press('tab') #scroll down 3
pyautogui.write('N')  #select all sku type 

pyautogui.press('F7') #submit
time.sleep(1)
pyautogui.press('enter')
time.sleep(1)


#log out
pyautogui.press('F1') #return to menu
pyautogui.press('F7') #sign out

#close jda
pyautogui.hotkey('alt', 'F4') 

