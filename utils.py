import colorsys
import numpy as np


def get_smart_hsv(img):
    """Analyzes the album cover to find a vibrant dominant color for the neon effect."""
    img_small = img.resize((10, 10)).convert("RGB")
    pix_array = np.array(img_small)
    avg_r = np.mean(pix_array[:, :, 0])
    avg_g = np.mean(pix_array[:, :, 1])
    avg_b = np.mean(pix_array[:, :, 2])
    h, s, v = colorsys.rgb_to_hsv(avg_r / 255.0, avg_g / 255.0, avg_b / 255.0)

    # Force high saturation for the neon look, unless it's grayscale
    if s < 0.12: return [h, 0.0, 0.75]
    return [h, max(s, 0.88), 0.75]
