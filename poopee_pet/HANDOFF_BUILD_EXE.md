# Prompt สำหรับ Claude: Build Poopee Desktop Pet → Windows .exe

## ไฟล์ที่แนบมาด้วย

| ไฟล์ | คำอธิบาย |
|---|---|
| `poopee_pet_project.zip` | โค้ดและ assets ทั้งหมด |
| `.env` | มี `GEMINI_API_KEY` สำหรับ Gemini AI |
| รูปแมว (ถ้าแนบมา) | sprite sheet ตัวใหม่ |

---

## บริบทโปรเจกต์

**Poopee Desktop Pet** คือ Windows Desktop Pet แมว tuxedo ที่:
- ลอยบนหน้าจอแบบโปร่งใส frameless always-on-top
- ลากแมวได้ / คลิกขวาเปลี่ยนท่า-ขนาด / ดับเบิลคลิกคุย
- ต่อ Gemini API ตอบภาษาไทย (fallback ถ้าไม่มี key)
- Save config ใน `config.json`

---

## โครงสร้างโปรเจกต์ (ใน zip)

```
poopee_pet/
├── main.py                  ← entry point: python main.py
├── requirements.txt         ← PyQt6, python-dotenv
├── .gitignore
├── build_windows.bat        ← build script (PyInstaller)
├── poopee_pet.spec          ← PyInstaller spec
├── installer.iss            ← Inno Setup installer script
├── BUILD_GUIDE.md
├── preview_lite.html        ← HTML preview (ไม่ต้องรัน server)
├── app/
│   ├── __init__.py
│   ├── config.py            ← load/save config.json
│   ├── pet_widget.py        ← หน้าต่างแมว + drag + menu (23 poses)
│   ├── bubble_widget.py     ← speech bubble
│   ├── chat_dialog.py       ← input dialog
│   └── ai/
│       ├── __init__.py      ← get_provider() auto-detect key
│       ├── base.py          ← AIProvider interface
│       ├── dummy_provider.py← fallback ไม่มี key
│       └── gemini_provider.py ← Gemini REST API (ไม่ต้องมี SDK)
├── assets/
│   ├── poopee_sprite_sheet.png
│   └── sprites/             ← 23 ท่า .png
│       walk.png, walk2.png, walk3.png, stand.png,
│       idle_front.png, idle_sleepy.png, sit_yawn.png,
│       peek.png, sit_alert.png, sit_side.png,
│       crouch_yawn.png, curl_sleep.png, crouch.png,
│       sleep_side.png, sleep_stretch.png, sleep_long_left.png,
│       sleep_low_left.png, sleep_low_right.png,
│       surprised.png, sleep_flat.png, sleep_roll.png,
│       sleep_back.png, sleep_curl2.png
└── tools/
    └── slice_sprites.py     ← pure-Python sprite sheet slicer
```

---

## Tech Stack

- **Python 3.11+**
- **PyQt6 ≥ 6.6** — UI framework
- **python-dotenv** — โหลด `.env`
- **Gemini API** ผ่าน `urllib` (stdlib, ไม่ต้อง SDK)
- **PyInstaller** — build .exe
- **Inno Setup 6** (optional) — สร้าง installer .exe

---

## Task: Build Windows .exe

### ขั้นตอนที่ต้องทำ

1. **แตก zip** และวาง `.env` ไว้ใน `poopee_pet/`

2. **ติดตั้ง dependencies**
   ```cmd
   pip install PyQt6 python-dotenv pyinstaller
   ```

3. **Build ด้วย PyInstaller**
   ```cmd
   cd poopee_pet
   pyinstaller poopee_pet.spec --noconfirm
   ```
   หรือรัน `build_windows.bat` ตรงๆ

4. **ผลลัพธ์** อยู่ที่ `dist\PoopeePet\PoopeePet.exe`

5. **(ตัวเลือก) สร้าง Installer**
   - ติดตั้ง [Inno Setup 6](https://jrsoftware.org/isinfo.php)
   - Compile `installer.iss`
   - ได้ไฟล์ `installer_output\PoopeePet_Setup_v1.0.0.exe`

---

## สิ่งสำคัญที่ต้องระวัง

### PyInstaller spec (`poopee_pet.spec`)
```python
datas=[('assets', 'assets')]   # ต้อง include assets folder
console=False                   # ไม่แสดง console window
```

### .env ต้องอยู่ข้างๆ .exe
วาง `.env` ใน `dist\PoopeePet\` เดียวกับ `PoopeePet.exe`

### Path ใน code ใช้ `Path(__file__).resolve().parent`
ทุกไฟล์ใช้ path แบบนี้ ไม่ใช้ `os.getcwd()` — PyInstaller รองรับได้

### Gemini Provider ใช้ urllib (ไม่ต้องมี google-genai)
`app/ai/gemini_provider.py` เรียก REST API โดยตรง:
```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=KEY
```

---

## ถ้าต้องการเพิ่ม App Icon

1. แปลง `assets/sprites/idle_sleepy.png` → `assets/poopee_icon.ico`
   ```python
   # ใช้ Pillow:
   from PIL import Image
   img = Image.open('assets/sprites/idle_sleepy.png')
   img.save('assets/poopee_icon.ico', sizes=[(256,256),(128,128),(64,64),(32,32),(16,16)])
   ```

2. แก้ `poopee_pet.spec` บรรทัด:
   ```python
   # icon='assets/poopee_icon.ico',   ← uncomment บรรทัดนี้
   ```

---

## ถ้าต้องการเปลี่ยน Sprite

1. วางรูป sprite sheet ใหม่ใน `assets/`
2. รัน `python tools/slice_sprites.py` (pure Python ไม่ต้องมี Pillow)
3. แก้ `POSE_NAMES` ใน `slice_sprites.py` ให้ตรงกับ layout ของรูป
4. อัปเดต `SPRITES` dict ใน `app/pet_widget.py`

---

## Acceptance Checklist

- [ ] `python main.py` รันได้ เห็นแมวลอยบน desktop
- [ ] ไม่มี console window โผล่มา
- [ ] ลากแมวได้
- [ ] คลิกขวา → เปลี่ยนท่า / ขนาด / quit
- [ ] ดับเบิลคลิก → กล่องแชท → ตอบเป็นภาษาไทย
- [ ] `dist\PoopeePet\PoopeePet.exe` รันได้โดยไม่ต้องติดตั้ง Python
- [ ] วาง `.env` ข้างๆ .exe แล้วตอบด้วย Gemini AI จริง

---

## หมายเหตุ

- `.env` **ไม่ถูก commit ขึ้น git** (อยู่ใน `.gitignore`)
- ถ้าไม่มี `.env` แอปทำงานปกติ ใช้ DummyProvider ตอบภาษาไทย
- รองรับ Windows 10 / 11 x64
