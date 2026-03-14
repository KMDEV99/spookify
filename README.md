# 🎸 Spookify Visualizer

A dynamic, 3D music visualizer for Spotify, optimized for Raspberry Pi. It displays rotating album art, smooth typography, and a reactive frequency-style equalizer, all synced with your current playback.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![Platform](https://img.shields.io/badge/platform-RPi%20%7C%20Windows%20%7C%20macOS-lightgrey)

---

## ✨ Features
* **3D Album Rotation:** Dynamic, glass-effect album art synced with your music.
* **Smart Color Extraction:** The UI palette adapts to the current album's colors using HSV analysis.
* **Real-time Equalizer:** A frequency-wave effect that pulses with the energy of the track.
* **RPi Optimized:** Custom settings to ensure smooth performance on Raspberry Pi 4/5.

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone [https://github.com/KMDEV99/spookify.git](https://github.com/KMDEV99/spookify.git)
cd spookify
```
### 2. Set up the Environment
```bash
python -m venv .venv
# On Linux/macOS:
source .venv/bin/activate  
# On Windows:
.venv\Scripts\activate

pip install -r requirements.txt
```
### 3. Configure Spotify Credentials
Go to the Spotify Developer Dashboard.

Create a new App and set the Redirect URI to http://127.0.0.1:8888/callback.

Copy .env.example to a new file named .env:
```bash
cp .env.example .env
```

### Usage
Simply run the main script:
```bash
python main.py
```
