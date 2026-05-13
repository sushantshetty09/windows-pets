import os
import sys
import platform
import winreg

def add_to_startup(app_name, exe_path):
    if platform.system() == "Windows":
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        print(f"Successfully added {app_name} to Windows Startup!")
    else:
        print("This script is only intended for Windows.")

if __name__ == "__main__":
    # Path to the pythonw.exe to run without a console window
    python_exe = sys.executable.replace("python.exe", "pythonw.exe")
    script_path = os.path.abspath("main.py")
    
    # We want to run it without a console window
    command = f'"{python_exe}" "{script_path}"'
    
    add_to_startup("WindowsPet", command)
