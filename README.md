# 🎸 Spookify-Visualizer
A high-end, real-time Spotify music visualizer designed for **Raspberry Pi 4**. It features a 3D rotating album cover with a "glass edge" neon effect, dynamic typography, and a beat-responsive wave equalizer.

## ✨ Features
- **3D Glass Album**: Rotating 3D cover with multi-layered neon edges and dynamic glow.
- **Traveling Wave EQ**: A smooth, "Instagram-style" wave equalizer with horizontal fading.
- **Beat Reactivity**: Interface pulses and increases saturation based on the music's energy.
- **Smart Color Extraction**: Analyzes the entire album cover to find the perfect neon hue.
- **Directional Transitions**: Swipes left for next track and right for previous track.
- **RPi Optimized**: Uses local caching, texture downsampling, and efficient P3D rendering.

## 🚀 Installation

1. **Clone the repo:**
   ```bash
   git clone https://github.com/KMDEV99/spookify.git
   cd spookify
   
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   
   python main.py

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.