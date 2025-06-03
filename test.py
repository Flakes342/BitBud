import pyautogui
import subprocess
import time
screenWidth, screenHeight = pyautogui.size()

search_url = f"https://www.youtube.com/results?search_query=Haule+Haule"
cmd = f"firefox {search_url}"

subprocess.Popen(cmd.split())
print(pyautogui.position())
time.sleep(5)  # Wait for a moment before opening the browser

print(pyautogui.position())

pyautogui.click(613,297)  # Click in the center of the screen

print(f"Screen width: {screenWidth}, Screen height: {screenHeight}")