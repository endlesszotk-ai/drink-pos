# วิธี Build Poopee Desktop Pet สำหรับ Windows

## ต้องการ

- Windows 10 / 11
- Python 3.11+  →  https://www.python.org/downloads/
- (ตัวเลือก) Inno Setup 6  →  https://jrsoftware.org/isinfo.php

---

## วิธีที่ 1 — รันสคริปต์เดียว (แนะนำ)

```bat
build_windows.bat
```

สคริปต์จะ:
1. ติดตั้ง dependencies ทั้งหมด
2. Build ด้วย PyInstaller
3. เปิดแอปให้ทดสอบเลย

ผลลัพธ์อยู่ที่ `dist\PoopeePet\PoopeePet.exe`

---

## วิธีที่ 2 — Build ด้วยมือ

```bat
pip install -r requirements.txt pyinstaller
pyinstaller poopee_pet.spec --noconfirm
```

---

## วิธีที่ 3 — สร้าง Installer (.exe)

หลังจาก build เสร็จแล้ว:

1. ติดตั้ง [Inno Setup 6](https://jrsoftware.org/isinfo.php)
2. เปิดไฟล์ `installer.iss` ใน Inno Setup IDE
3. กด Compile (Ctrl+F9)
4. ไฟล์ installer จะอยู่ที่ `installer_output\PoopeePet_Setup_v1.0.0.exe`

---

## ใช้งาน Gemini AI

สร้างไฟล์ `.env` ใน `dist\PoopeePet\` (หรือโฟลเดอร์เดียวกับ .exe):

```
GEMINI_API_KEY=your_api_key_here
```

รับ API key ได้ฟรีที่ https://aistudio.google.com/

---

## โครงสร้างโปรเจกต์

```
poopee_pet/
├── main.py              ← entry point
├── requirements.txt
├── poopee_pet.spec      ← PyInstaller config
├── build_windows.bat    ← build script
├── installer.iss        ← Inno Setup installer script
├── .env.example
├── assets/
│   └── sprites/         ← รูปแมว 11 ท่า
└── app/
    ├── config.py
    ├── pet_widget.py
    ├── bubble_widget.py
    ├── chat_dialog.py
    └── ai/
        ├── dummy_provider.py
        └── gemini_provider.py
```
