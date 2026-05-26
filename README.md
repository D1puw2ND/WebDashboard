# ProcWatch — Process Monitoring Dashboard

Monitor dan kontrol main.py secara real-time dari browser.

## Struktur Folder

```
project/
├── app.py              ← Flask server
├── main.py             ← Tool kamu (taruh di sini)
├── install.sh          ← Installer (taruh di sini)
├── requirements.txt    ← Dependency dashboard
└── templates/
    └── index.html      ← UI dashboard
```

## Cara Pakai

### 1. Install dependency dashboard
```bash
pip install -r requirements.txt
```

### 2. Jalankan server
```bash
python app.py
```

### 3. Buka browser
```
http://localhost:5000
```

### 4. Kontrol dari dashboard
- Klik **START** → jalankan main.py
- Klik **FORCE STOP** → hentikan paksa
- Klik **EXPORT** → download log sebagai .txt
- Klik **CLEAR** → bersihkan tampilan log

## Keyboard Shortcut
| Key | Aksi |
|-----|------|
| F5  | START |
| ESC | FORCE STOP |

## Akses dari HP / device lain (satu jaringan WiFi)
Cari IP lokal kamu:
```bash
# Linux/Termux
ip addr show | grep inet
```
Lalu buka di browser HP: `http://192.168.x.x:5000`
