import pyautogui #click and keyboard
import time #time command(i.e. time delay)
import subprocess
from datetime import datetime, timezone, timedelta
from AppOpener import open
from jda_parameter import OFM_parameter, B2S_parameter, SSP_parameter  # importing parameters

# List of parameter sets
parameter_sets = [OFM_parameter] ##, B2S_parameter, SSP_parameter] 

# Define the file path
for params in parameter_sets:
    subprocess.Popen([r"C:\Program Files (x86)\IBM\Client Access\cwbtf.exe"], shell=True)
    time.sleep(10)
    #Setting receive window
    pyautogui.press('del') #delete old text
    pyautogui.write(params["server_name"])  # write server name
    pyautogui.press('tab') #scroll down     
    pyautogui.press('del') #delete old text
    pyautogui.write(params["file_name"])  # write file name
    pyautogui.press('tab') #scroll down step1
    pyautogui.press('tab') #scroll down step2
    pyautogui.press('tab') #scroll down step3
    pyautogui.press('down') #select file
    pyautogui.press('tab') #scroll down step4
    pyautogui.press('enter')  #enter to file detail

    #file details 
    pyautogui.press('tab') #scroll down 1
    pyautogui.press('tab') #scroll down 2
    pyautogui.press('tab') #scroll down 3
    pyautogui.press('tab') #scroll down 4
    pyautogui.press('tab') #scroll down 5
    pyautogui.press('tab') #scroll down 6
    pyautogui.press('down') #select 1
    pyautogui.press('down') #select 2
    pyautogui.press('tab') #scroll down 7
    pyautogui.write('c') #select csv format
    pyautogui.press('tab') #scroll down 1
    pyautogui.press('tab') #scroll down 2
    pyautogui.press('tab') #scroll down 3
    pyautogui.press('tab') #scroll down 4
    pyautogui.press('tab') #scroll down 5
    pyautogui.press('tab') #scroll down 6
    pyautogui.press('enter')  #enter to submit

    #Setting receive window
    pyautogui.press('tab')
    pyautogui.write(params["path_file"]) #write file name
    pyautogui.press('tab') #scroll down step5
    pyautogui.press('tab') #scroll down step6
    pyautogui.press('tab') #scroll down step7
    pyautogui.press('enter')  #enter submit 

    pyautogui.press('enter')  #yes alert box

    # Key write to log in to JDA
''' pyautogui.press('tab')  #tab for login1
    pyautogui.press('tab')  #tab for login2
    pyautogui.press('tab')  #tab for login3
    pyautogui.write(params["user"]) #write id
    pyautogui.press('tab')  #tab for login4
    pyautogui.write(params["pass"]) #write pass
    pyautogui.press('tab')  #tab for login5
    pyautogui.press('enter') # enter step1 ''' 