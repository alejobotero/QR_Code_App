# QR Studio — Flask App

A polished QR code generator with an interactive web UI.

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Features

- **Generate QR codes** from any text, URL, email, phone, Wi-Fi config, or vCard
- **Custom colors** — pick any foreground/background color
- **Error correction levels** — L / M / Q / H
- **PNG or SVG output**
- **One-click download** and copy-to-clipboard
- **Quick presets** for common QR types (URL, email, Wi-Fi, vCard)
- **Recent history** thumbnails in the preview panel
- **Ctrl+Enter** keyboard shortcut to generate

## Project Structure

```
qr_app/
├── app.py              ← Flask backend
├── requirements.txt
└── templates/
    └── index.html      ← Single-page UI
```

## Deploying Online (e.g. Railway, Render, Fly.io)

1. Add a `Procfile`:
   ```
   web: gunicorn app:app
   ```
2. Add `gunicorn` to `requirements.txt`
3. Push to your platform of choice — all three support free tiers.
