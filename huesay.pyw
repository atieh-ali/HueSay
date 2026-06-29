"""
HueSay - a color identifier for red-green colorblindness (Windows)
-------------------------------------------------------------------
A small label follows your mouse and tells you, in plain English, what color
is under your cursor - plus the HEX and RGB code. It can also say it out loud.

Controls (global hotkeys - work from anywhere):
  * Ctrl + Alt + S   -> say the current color out loud
  * Ctrl + Alt + Q   -> quit HueSay

No installation needed beyond Python itself. Uses only built-in modules.
Free to use and share.
"""

import ctypes
import subprocess
import tkinter as tk
from math import sqrt

# --- Make the app DPI-aware so cursor + pixel coordinates line up on any monitor ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
user32.GetAsyncKeyState.restype = ctypes.c_short

CREATE_NO_WINDOW = 0x08000000  # keeps the speech helper from flashing a console

# Virtual key codes for global hotkeys
VK_CONTROL, VK_ALT, VK_S, VK_Q = 0x11, 0x12, 0x53, 0x51


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def get_cursor_pos():
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


def get_pixel_color(x, y):
    """Return (r, g, b) of the pixel at screen coords (x, y), or None on failure."""
    hdc = user32.GetDC(0)
    if not hdc:
        return None
    color = gdi32.GetPixel(hdc, x, y)
    user32.ReleaseDC(0, hdc)
    if color == 0xFFFFFFFF or color < 0:  # CLR_INVALID
        return None
    r = color & 0xFF
    g = (color >> 8) & 0xFF
    b = (color >> 16) & 0xFF
    return r, g, b


def key_down(vk):
    return bool(user32.GetAsyncKeyState(vk) & 0x8000)


def speak(text):
    """Say `text` aloud using Windows' built-in speech engine (no install needed)."""
    safe = text.replace("'", "").replace('"', "")
    ps = (
        "Add-Type -AssemblyName System.Speech; "
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$s.Speak('" + safe + "')"
    )
    try:
        subprocess.Popen(
            ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps],
            creationflags=CREATE_NO_WINDOW,
        )
    except Exception:
        pass  # speech is a nice-to-have; never crash the app over it


# --- Named-color table. Heavier coverage in the reds/greens/browns/oranges that
#     trip up red-green colorblindness, so the spoken name is decisive. ---
NAMED_COLORS = [
    ("Black", (0, 0, 0)),
    ("Charcoal", (45, 45, 45)),
    ("Dark gray", (80, 80, 80)),
    ("Gray", (128, 128, 128)),
    ("Silver gray", (170, 170, 170)),
    ("Light gray", (205, 205, 205)),
    ("Off white", (240, 240, 235)),
    ("White", (255, 255, 255)),

    ("Red", (220, 20, 20)),
    ("Bright red", (255, 0, 0)),
    ("Dark red", (139, 0, 0)),
    ("Brick red", (170, 50, 40)),
    ("Crimson", (200, 30, 60)),
    ("Tomato red", (255, 80, 60)),
    ("Coral", (255, 110, 90)),
    ("Salmon pink", (250, 128, 114)),
    ("Pink", (255, 150, 180)),
    ("Light pink", (255, 195, 205)),
    ("Hot pink", (255, 60, 150)),
    ("Rose", (210, 70, 110)),
    ("Magenta", (220, 0, 200)),
    ("Maroon", (128, 0, 32)),

    ("Orange", (255, 140, 0)),
    ("Bright orange", (255, 165, 0)),
    ("Peach", (255, 200, 150)),
    ("Amber", (255, 191, 0)),
    ("Brown", (139, 69, 19)),
    ("Dark brown", (80, 45, 20)),
    ("Chocolate", (110, 65, 35)),
    ("Tan", (210, 180, 140)),
    ("Beige", (225, 210, 175)),
    ("Rust", (165, 70, 30)),
    ("Terracotta", (190, 95, 65)),

    ("Yellow", (240, 220, 20)),
    ("Bright yellow", (255, 240, 0)),
    ("Gold", (212, 175, 55)),
    ("Mustard", (200, 170, 45)),
    ("Khaki", (190, 180, 120)),
    ("Pale yellow", (245, 240, 150)),

    ("Green", (30, 160, 50)),
    ("Bright green", (0, 200, 0)),
    ("Dark green", (0, 100, 0)),
    ("Forest green", (34, 100, 34)),
    ("Emerald green", (0, 150, 90)),
    ("Lime green", (130, 210, 40)),
    ("Chartreuse", (175, 215, 60)),
    ("Olive green", (110, 110, 30)),
    ("Mint green", (150, 230, 170)),
    ("Sage green", (140, 165, 130)),
    ("Sea green", (46, 139, 87)),
    ("Teal", (0, 128, 128)),

    ("Blue", (30, 80, 220)),
    ("Bright blue", (0, 90, 255)),
    ("Dark blue", (0, 0, 139)),
    ("Navy", (20, 30, 80)),
    ("Royal blue", (65, 105, 225)),
    ("Steel blue", (70, 110, 150)),
    ("Sky blue", (120, 190, 235)),
    ("Light blue", (173, 216, 230)),
    ("Powder blue", (200, 225, 235)),
    ("Cyan", (0, 200, 220)),

    ("Purple", (128, 0, 128)),
    ("Violet", (148, 80, 211)),
    ("Plum", (140, 70, 130)),
    ("Lavender", (200, 180, 230)),
    ("Indigo", (75, 0, 130)),
    ("Mauve", (180, 150, 175)),
]


def color_distance(c1, c2):
    """Perceptual-ish distance (redmean) so names match how colors look."""
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    rmean = (r1 + r2) / 2.0
    dr, dg, db = r1 - r2, g1 - g2, b1 - b2
    return sqrt(
        (2 + rmean / 256.0) * dr * dr
        + 4 * dg * dg
        + (2 + (255 - rmean) / 256.0) * db * db
    )


def name_color(rgb):
    return min(NAMED_COLORS, key=lambda c: color_distance(rgb, c[1]))[0]


def luminance(rgb):
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


class HueSay:
    OFFSET_X, OFFSET_Y = 18, 20  # how far the label sits from the cursor tip

    def __init__(self, root):
        self.root = root
        self.last_name = ""
        self.s_was_down = False

        # Borderless, always-on-top floating label
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.configure(bg="#111111")

        self.swatch = tk.Label(root, width=2, bg="#000000")
        self.swatch.pack(side="left", fill="y", padx=(3, 4), pady=3)

        self.text = tk.Label(
            root, text="...", justify="left", anchor="w",
            font=("Segoe UI", 9, "bold"), fg="#ffffff", bg="#111111")
        self.text.pack(side="left", padx=(0, 6), pady=2)

        self.update_loop()

    def update_loop(self):
        # Global hotkeys
        if key_down(VK_CONTROL) and key_down(VK_ALT) and key_down(VK_Q):
            self.root.destroy()
            return
        s_now = key_down(VK_CONTROL) and key_down(VK_ALT) and key_down(VK_S)
        if s_now and not self.s_was_down and self.last_name:
            speak(self.last_name)
        self.s_was_down = s_now

        x, y = get_cursor_pos()
        rgb = get_pixel_color(x, y)
        if rgb:
            r, g, b = rgb
            hex_code = "#%02X%02X%02X" % (r, g, b)
            self.last_name = name_color(rgb)
            self.swatch.config(bg=hex_code)
            self.text.config(text="%s\n%s  (%d,%d,%d)" % (self.last_name, hex_code, r, g, b))

        # Follow the cursor (label sits to the lower-right so it never covers the tip)
        self.root.geometry("+%d+%d" % (x + self.OFFSET_X, y + self.OFFSET_Y))
        self.root.after(90, self.update_loop)


if __name__ == "__main__":
    root = tk.Tk()
    HueSay(root)
    root.mainloop()
