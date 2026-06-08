# ⚔️ PoE Act Rush Overlay

> A lightweight, always-on-top overlay for **Path of Exile 1** that tracks your Act Rush route in real time — so you never forget where to go next.

![Python](https://img.shields.io/badge/Python-3.10+-c8a96e?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-9ab8d8?style=flat-square&logo=windows&logoColor=white)
![Game](https://img.shields.io/badge/Game-Path%20of%20Exile%201-d8b89a?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-a8d89a?style=flat-square)

---

## ✨ What It Does

🗺️ **Live zone tracking** — reads your `Client.txt` log and detects every zone you enter, instantly  
📋 **Step-by-step guide** — shows exactly what to do next for every zone across all 10 Acts  
🟩 **Pickup reminders** — alerts you when there's a quest item to grab in the current zone  
⏱️ **Run timer** — start, pause, stop and reset your speedrun stopwatch at any time  
🔒 **Lockable window** — lock the overlay in place so you don't accidentally drag it mid-run  
🎮 **Always on top** — semi-transparent and stays above the game window  

---

## 🖼️ Preview

```
┌─────────────────────────────────────────┐
│ ⚔ PoE Act Rush          F5=lock F6=reset  ✕ │
├─────────────────────────────────────────┤
│  00:42                                  │
│  ▶ START   ■ STOP   ⏸ PAUSE            │
├─────────────────────────────────────────┤
│  The Mud Flats                          │
│  Act 1                                  │
│  ▸ Collect 3 Glyphs                     │
│    → Head to Submerged Passage          │
│                                         │
│  🟩 Pick up Glyph!                      │
├─────────────────────────────────────────┤
│  Browse…   Reading: Client.txt          │
└─────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Option A — Run from source

**Requirements:** Python 3.10 or newer (no extra libraries needed)

```bash
python poe_overlay.py
```

### Option B — Download the .exe

Grab the latest release from the [Releases](../../releases) page and run it directly — no Python installation required.

---

## 🗂️ Where is Client.txt?

The overlay auto-detects the log file from the most common install locations.
If it doesn't find it automatically, click **Browse…** and navigate to:

```
C:\Program Files (x86)\Grinding Gear Games\Path of Exile\logs\Client.txt
```

Or for Steam:

```
C:\Program Files (x86)\Steam\steamapps\common\Path of Exile\logs\Client.txt
```

---

## 🎮 Controls

| Control | Action |
|--------|--------|
| `▶ START` | Begin the run timer |
| `⏸ PAUSE` | Pause / resume the timer |
| `■ STOP` | Stop the timer (keeps the time shown) |
| `F5` | Lock / unlock window dragging |
| `F6` | Reset timer back to `00:00` |
| `✕` | Close the overlay |
| `Browse…` | Manually select your `Client.txt` |

---

## 🗺️ Route Coverage

The overlay follows the classic Act Rush route across all 10 Acts:

| Act | Key Objectives |
|-----|---------------|
| 🟩 **Act 1** | Coast → Mud Flats → Prison → Ship Graveyard → Merveil |
| **Act 2** | Chamber of Sins → Crypt → Bandit Lords → Weaver → Vaal Oversoul |
| ✅ **Act 3** | Crematorium → Sewers → Battlefront → Docks → Dominus |
| 🟪 **Act 4** | Dried Lake → Mines → Kaom → Malachai |
| 🟦 **Act 5** | Ascent → Chamber of Innocence → Kitava |
| 🟧 **Act 6** | Coast → Prison → Riverways → Brine King's Reef |
| 🟥 **Act 7** | Crypt → Ashen Fields → Vaal City → Arakaali |
| 🟪 **Act 8** | Toxic Conduits → Bath House → Harbour Bridge |
| 🟦 **Act 9** | Vastiri Desert → Quarry → Oriath |
| 🟨 **Act 10** | Ravaged Square → Desecrated Chambers → Kitava |

---

## 🔨 Build Your Own .exe

Want to share the overlay with friends without requiring Python? Use PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole poe_overlay.py
```

The `.exe` will appear in the `dist/` folder.

---

## 🛠️ Customising the Route

The full route is defined in the `ROUTE` list near the top of `poe_overlay.py`. Each entry looks like this:

```python
{
    "zones": ["The Mud Flats", "Mud Flats"],   # zone names to match (log exact or fuzzy)
    "act": "Act 1",
    "steps": ["Collect 3 Glyphs", "→ Submerged Passage"],
    "pickups": ["🟩 Pick up Glyph!"],           # shown as green alert
},
```

Edit, add or remove entries to match your preferred route — no other changes needed.

---

## 🤝 Contributing

Pull requests are welcome! If you have a better route, want to add split tracking, or improve the UI — go for it.

1. Fork the repo
2. Create a branch: `git checkout -b feature/my-improvement`
3. Commit your changes
4. Open a Pull Request

---

## 📜 License

MIT — do whatever you want with it. A star ⭐ is always appreciated!

---

> *Made for Wraeclast survivors who are tired of googling "where do I go in Act 7" mid-run.* 🗡️
