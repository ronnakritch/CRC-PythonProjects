import pyautogui
import time
while True:
        x, y = pyautogui.position()  # Get the current mouse coordinates
        print(f"Mouse position: ({x}, {y})")
        time.sleep(1)  # Delay to avoid overwhelming output
