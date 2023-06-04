import tkinter as tk
import threading
import urllib.request
import zipfile
import os
from tkinter import messagebox
import shutil
import subprocess

class Update:
    def __init__(self, version, docdir):
        self.version = version
        self.docdir = docdir

        self.root = tk.Tk()
        self.root.geometry('300x40')
        self.root.title("NSBot Update")

        self.update_Label = tk.Label(self.root, text="กำลังติดตั้งอัพเดท กรุณารอสักครู่", font=("Segoe UI",  12))
        self.update_Label.pack()

        self.root.update()
        self.start_download_and_extract()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        x_cordinate = int((self.root.winfo_screenwidth() / 2) - (self.root.winfo_width() / 2))
        y_cordinate = int((self.root.winfo_screenheight() / 2) - (self.root.winfo_height() / 2))
        self.root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def cleanup_files(self):
        # ระบุโฟลเดอร์ของโปรแกรม
        program_dir = self.docdir

        # ลบไฟล์ในโฟลเดอร์ของโปรแกรม (ยกเว้นโฟลเดอร์ .git และ extract_temporary)
        for file_name in os.listdir(program_dir):
            file_path = os.path.join(program_dir, file_name)
            if os.path.isfile(file_path) and file_name != ".git" and file_name not in ["update.py", "update2.py", "update2.exe", "main.py", "gui.py", "gui.exe"]:
                os.remove(file_path)
            elif os.path.isdir(file_path) and file_name != ".git" and file_name != "extract_temporary":
                shutil.rmtree(file_path)

        # ย้ายไฟล์และโฟลเดอร์จาก extract_temporary ไปยังโฟลเดอร์ของโปรแกรม
        extract_temp_dir = os.path.join(program_dir, "extract_temporary")
        for file_name in os.listdir(extract_temp_dir):
            file_path = os.path.join(extract_temp_dir, file_name)
            if os.path.isfile(file_path) or os.path.isdir(file_path):
                if file_name not in ["update.py", "update2.exe"]:
                    destination_path = os.path.join(program_dir, file_name)
                    if os.path.exists(destination_path):
                        os.remove(destination_path)  # ลบไฟล์ที่มีอยู่ในที่ปลายทาง
                    shutil.move(file_path, program_dir)

        # ลบโฟลเดอร์ extract_temporary
        shutil.rmtree(extract_temp_dir)

    def download_and_extract(self):
        # URL ของไฟล์ .zip ที่ต้องการดาวน์โหลด
        zip_url = f"https://github.com/nsblollipop/NSBotUpdate/releases/download/{self.version}/NSBot.zip"

        # ชื่อไฟล์ .zip ที่ต้องการบันทึก
        zip_file_name = "NSBot.zip"

        # ตำแหน่งที่ต้องการแตกไฟล์
        extract_dir = "extract_temporary"

        # ดาวน์โหลดไฟล์ .zip
        urllib.request.urlretrieve(zip_url, zip_file_name)

        # แตกไฟล์ .zip
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # ลบไฟล์ .zip หลังจากแตกไฟล์แล้ว (ถ้าต้องการ)
        os.remove(zip_file_name)

        # ลบไฟล์ในโฟลเดอร์ของโปรแกรมและย้ายไฟล์จาก extract_temporary ไปยังโฟลเดอร์ของโปรแกรม (ยกเว้น .git)
        self.cleanup_files()

        subprocess.Popen(['NSBot.exe'])
        self.root.destroy()

    def start_download_and_extract(self):
        # สร้างเธรดสำหรับดาวน์โหลดและแตกไฟล์
        thread = threading.Thread(target=self.download_and_extract)

        # กำหนดให้เธรดทำงานเป็นแบบ Daemon เพื่อปิดโปรแกรมได้หากผู้ใช้ปิดหน้าต่าง
        thread.daemon = True

        # เริ่มเธรด
        thread.start()

    def on_closing(self):
        if messagebox.askokcancel("ออก", "คุณต้องการออกจากโปรแกรมหรือไม่?"):
            self.root.destroy()
