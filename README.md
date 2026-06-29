# HueSay 🎨🔊

**A color identifier for red-green colorblindness.** Hover your mouse anywhere on
your Windows screen and HueSay shows — in plain English — what color is under your
cursor, along with its HEX and RGB code. It can also say the color out loud.

Unlike browser color-picker extensions, HueSay reads **any pixel anywhere on your
screen** — photos, videos, other apps, games — not just web pages. The color names
are deliberately tuned toward the reds, pinks, oranges, browns, and greens that are
hardest to tell apart with red-green color vision deficiency, so the label is
decisive ("Olive green", "Brick red") rather than just a code you'd have to decode.

> Built by someone with red-green colorblindness, for anyone who wants to know what
> color they're actually looking at. Free to use and free to share.
<img width="400" height="339" alt="HueSay naming a color under the cursor" src="https://github.com/user-attachments/assets/3f8a193a-fbac-4d8f-a0b5-47d681680fa0" />

---

## ✨ Features

- **Follows your cursor** — a small label rides next to your mouse and updates live.
- **Plain-English color names** tuned for red-green colorblindness.
- **HEX + RGB codes** shown alongside the name.
- **Speaks the color out loud** using the built-in Windows voice (no extra install).
- **Works everywhere on screen**, not just in the browser.
- **Tiny and dependency-free** — pure Python standard library, no packages needed.

## 🎮 Controls

| Hotkey | Action |
| --- | --- |
| `Ctrl + Alt + S` | Say the current color out loud |
| `Ctrl + Alt + Q` | Quit HueSay |

## ⬇️ Download (no Python needed)

Grab the latest `HueSay.exe` from the [**Releases**](https://github.com/atieh-ali/HueSay/releases) page and
double-click it.

> The first time you run it, Windows SmartScreen may say "unknown publisher."
> That's only because the app isn't code-signed — click **More info → Run anyway**.

## 🛠️ Run from source (if you have Python)

```bash
python huesay.pyw
```

Requires Python 3.8+ on Windows. No `pip install` needed — it uses only the
standard library (`tkinter`, `ctypes`, `subprocess`).

## 🧩 Build your own .exe

```bash
pip install pyinstaller
python -m PyInstaller --onefile --noconsole --name HueSay huesay.pyw
```

The finished `HueSay.exe` will be in the `dist` folder.

## 🔍 How it works

HueSay reads the pixel under the cursor through the Windows GDI API (`GetPixel`)
via `ctypes`, then matches that RGB value to the nearest entry in a hand-tuned
color table using a perceptual ("redmean") distance formula so the chosen name
matches how the color actually looks. The label is a borderless, always-on-top
`tkinter` window that repositions itself next to the cursor each frame. Speech
uses the Windows built-in `System.Speech` engine via PowerShell.

## ♿ Accessibility note

HueSay is an assistive tool, not a medical device. It identifies on-screen pixel
colors; it can't correct color vision or guarantee a perfect name for every shade.
Suggestions and corrections are very welcome — open an issue.

## 📄 License

Released under the MIT License — free to use, modify, and share. See
[LICENSE](LICENSE).

## 👤 Author

**Ali Atieh** — [github.com/atieh-ali](https://github.com/atieh-ali)

Built in 2026 as a free accessibility tool for the colorblind community.
