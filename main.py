import threading
import time
import colorsys
import os
import py5

from spotify_handler import SpotifyHandler
from utils import get_smart_hsv
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
WIDTH, HEIGHT = 720, 720
SCALE_FACTOR = 0.8
CACHE_DIR = "album_cache"

# --- GLOBAL STATE ---
album_current, album_prev = None, None
track_name, artist_name = "", ""
next_track_name, next_artist_name = "", ""
last_track_id = None
track_history = []

anim_progress, anim_direction = 1.0, 1
target_hsv, current_hsv = [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]
beat_flash, wave_offset = 0.0, 0.0
lock = threading.Lock()


def setup():
    global spotify, font_title, font_artist
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.no_smooth()
    py5.no_stroke()

    if not os.path.exists(CACHE_DIR): os.makedirs(CACHE_DIR)

    try:
        font_title = py5.create_font("DejaVu Sans Bold", 44)
    except:
        font_title = py5.create_font("SansSerif", 44)

    try:
        font_artist = py5.create_font("DejaVu Sans Bold", 24)
    except:
        font_artist = py5.create_font("SansSerif", 24)

    spotify = SpotifyHandler(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, CACHE_DIR)
    threading.Thread(target=update_thread, daemon=True).start()


def update_thread():
    global album_current, album_prev, last_track_id, target_hsv, next_track_name, next_artist_name, anim_progress, anim_direction
    while True:
        try:
            track = spotify.get_current_track()
            if track and track['item']:
                t_id = track['item']['id']
                if t_id != last_track_id:
                    with lock:
                        if t_id in track_history:
                            anim_direction = -1
                            track_history.remove(t_id)
                        else:
                            anim_direction = 1
                        track_history.append(t_id)
                        if len(track_history) > 100: track_history.pop(0)

                    img_raw = spotify.get_album_art(t_id, track['item']['album']['images'][0]['url'])
                    hsv = get_smart_hsv(img_raw)
                    img_np = py5.create_image_from_numpy(py5.np.array(img_raw), "RGBA")

                    with lock:
                        if album_current: album_prev = album_current
                        next_track_name = track['item']['name'].upper()
                        next_artist_name = " ".join(list(track['item']['artists'][0]['name'].upper()))
                        album_current, target_hsv = img_np, hsv
                        anim_progress = 0.0
                    last_track_id = t_id
        except Exception as e:
            print(f"Update error: {e}")
        time.sleep(2)


def draw():
    global current_hsv, anim_progress, beat_flash, wave_offset, track_name, artist_name
    py5.background(0)

    py5.push_matrix()
    py5.translate(WIDTH / 2, HEIGHT / 2)
    py5.rotate_z(py5.PI)
    py5.scale(SCALE_FACTOR)
    py5.translate(-WIDTH / 2, -HEIGHT / 2)

    with lock:
        for i in range(3): current_hsv[i] = py5.lerp(current_hsv[i], target_hsv[i], 0.05)
        beat_flash *= 0.92
        wave_offset += 0.06
        if anim_progress < 0.5:
            ui_alpha = py5.remap(anim_progress, 0, 0.5, 255, 0)
        else:
            track_name, artist_name = next_track_name, next_artist_name
            ui_alpha = py5.remap(anim_progress, 0.5, 1.0, 0, 255)
        if anim_progress < 1.0: anim_progress += 0.025
        curr, prev, d = album_current, album_prev, anim_direction

    if curr:
        h, s, v = current_hsv
        r, g, b = [int(c * 255) for c in
                   colorsys.hsv_to_rgb(h, min(1.0, s + beat_flash * 0.4), min(1.0, v + beat_flash * 0.5))]

        # 1. UI TEXT
        py5.text_align(py5.CENTER)
        py5.push_matrix()
        py5.translate(WIDTH / 2, 80)
        py5.scale(1.0 + (beat_flash * 0.05))
        py5.fill(r, g, b, ui_alpha)
        py5.text_font(font_title)
        for off in [-1, 0, 1]: py5.text(track_name, off, 0)
        py5.translate(0, 35)
        py5.fill(r, g, b, ui_alpha * 0.8)
        py5.text_font(font_artist)
        py5.text(artist_name, 0, 0)
        py5.pop_matrix()

        # 2. WAVE EQUALIZER
        py5.push_matrix()
        py5.translate(WIDTH / 2 - (60 * 8) / 2, HEIGHT - 130)
        for i in range(60):
            edge = py5.sin(py5.remap(i, 0, 59, 0, py5.PI))
            n = py5.noise((i + wave_offset) * 0.04, py5.frame_count * 0.02)
            h_bar = n * (110 + beat_flash * 40)
            py5.begin_shape(py5.QUADS)
            py5.fill(r, g, b, ui_alpha * edge)
            py5.vertex(i * 8, 0)
            py5.vertex(i * 8 + 5, 0)
            py5.fill(r * 0.1, g * 0.1, b * 0.1, ui_alpha * edge)
            py5.vertex(i * 8 + 5, -h_bar)
            py5.vertex(i * 8, -h_bar)
            py5.end_shape()
            if n > 0.75: beat_flash = 0.4
        py5.pop_matrix()

        # 3. ALBUMS
        if prev and anim_progress < 1.0:
            draw_album(prev, (r, g, b), -d * anim_progress * WIDTH, 1.0 - anim_progress)
        draw_album(curr, (r, g, b), d * (1.0 - anim_progress) * WIDTH, anim_progress)

    py5.pop_matrix()


def draw_album(img, col, x, alpha):
    py5.push_matrix()
    py5.translate(WIDTH / 2 + x, HEIGHT / 2 - 5, 0)
    py5.rotate_x(0.42)
    py5.rotate_y(py5.frame_count * 0.0025)

    # Glow & Solid Side
    py5.hint(py5.DISABLE_DEPTH_MASK)
    for i in range(5):
        py5.fill(col[0], col[1], col[2], py5.remap(i, 0, 5, 10 + beat_flash * 20, 0) * alpha)
        py5.box(324 + i * 8, 324 + i * 8, 26 + i * 4)
    py5.hint(py5.ENABLE_DEPTH_MASK)

    py5.fill(col[0] * 0.2, col[1] * 0.2, col[2] * 0.2, 255 * alpha)
    py5.box(318, 318, 22)

    # Glass Edges
    py5.no_fill()
    py5.stroke_weight(2)
    for z in py5.np.linspace(-11, 11, 6):
        br = py5.lerp(0.6, 1.3, abs(z) / 11)
        py5.stroke(col[0] * br, col[1] * br, col[2] * br, 255 * alpha)
        py5.push_matrix()
        py5.translate(0, 0, z)
        py5.rect(-159, -159, 318, 318)
        py5.pop_matrix()
    py5.no_stroke()

    # Textured faces
    for z_pos in [11.2, -11.2]:
        py5.push_matrix()
        py5.translate(0, 0, z_pos)
        if z_pos < 0: py5.rotate_y(py5.PI)
        py5.tint(230 + beat_flash * 25, 255 * alpha)
        py5.begin_shape()
        py5.texture(img)
        py5.texture_mode(py5.NORMAL)
        py5.vertex(-160, -160, 0, 0, 0)
        py5.vertex(160, -160, 0, 1, 0)
        py5.vertex(160, 160, 0, 1, 1)
        py5.vertex(-160, 160, 0, 0, 1)
        py5.end_shape()
        py5.pop_matrix()
    py5.pop_matrix()


py5.run_sketch()