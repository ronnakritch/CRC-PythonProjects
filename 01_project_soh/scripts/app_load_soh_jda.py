import pyautogui
import time
import subprocess
import sys
import os
# Dynamically add the project root to the module search path
script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
project_root = os.path.abspath(os.path.join(script_dir, ".."))  # One level up (project root)
sys.path.append(project_root)  # Add project root to sys.path
from configs.parameter_soh_jda import OFM_parameter, B2S_parameter, SSP_parameter

# List of parameter sets
parameter_sets = [ OFM_parameter, B2S_parameter, SSP_parameter] 

# Define the file path
for params in parameter_sets:
    subprocess.Popen(params["ibm_path"], shell=True)
    time.sleep(5)
    pyautogui.press('enter') #transfer data
    pyautogui.write(params["user"]) #write id
    pyautogui.press('tab')  #tab for login4
    pyautogui.write(params["pass"]) #write pass
    pyautogui.press('enter') # enter step1 