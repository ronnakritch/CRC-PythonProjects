import pyautogui
import time
import subprocess


app_path = r"C:\Program Files\Stock Tops Care\SmartDrugstoreHybridHO.exe"
user = "Stock01"
pwd = "Stock01new@2024"

subprocess.Popen(app_path, shell=True)
time.sleep(10)
pyautogui.hotkey('alt','tab')
pyautogui.hotkey('alt','tab')
time.sleep(1)
pyautogui.click(906, 523)
time.sleep(1)
pyautogui.typewrite(user)

pyautogui.press('tab')
pyautogui.write(pwd)
pyautogui.press('enter')
time.sleep(10)
pyautogui.click(206, 73)
time.sleep(1)
pyautogui.click(406, 99)
time.sleep(1)
pyautogui.click(490, 1020)
time.sleep(1)
pyautogui.click(900, 799)

for _ in range(36):
    time.sleep(1)
    pyautogui.press('down')
    pyautogui.hotkey('ctrl','c')
    pyautogui.click(583, 800) #export
    time.sleep(3)
    pyautogui.hotkey('ctrl','v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    time.sleep(1)

pyautogui.click(1411, 817) #close 
time.sleep(1)
pyautogui.click(513, 54) #close 
time.sleep(1)
pyautogui.press('enter')

print("\nLoad SOH all Topcare success, Program exited.")



