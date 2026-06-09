<div align="center">

```
██████╗  ██████╗ ███████╗     █████╗  ██████╗████████╗    ██████╗ ██╗   ██╗███████╗██╗  ██╗
██╔══██╗██╔═══██╗██╔════╝    ██╔══██╗██╔════╝╚══██╔══╝    ██╔══██╗██║   ██║██╔════╝██║  ██║
██████╔╝██║   ██║█████╗      ███████║██║        ██║        ██████╔╝██║   ██║███████╗███████║
██╔═══╝ ██║   ██║██╔══╝      ██╔══██║██║        ██║        ██╔══██╗██║   ██║╚════██║██╔══██║
██║     ╚██████╔╝███████╗    ██║  ██║╚██████╗   ██║        ██║  ██║╚██████╔╝███████║██║  ██║
╚═╝      ╚═════╝ ╚══════╝    ╚═╝  ╚═╝ ╚═════╝   ╚═╝        ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                          ⚔  O V E R L A Y
```

**The only overlay your party leader will ever need.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078d7?style=flat-square&logo=windows&logoColor=white)](https://github.com)
[![Game](https://img.shields.io/badge/Game-Path%20of%20Exile%201-orange?style=flat-square)](https://www.pathofexile.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Vibes](https://img.shields.io/badge/Vibes-Immaculate-gold?style=flat-square)](https://github.com)

</div>

---

## 🗡️ What is this?

You're in a **party rush**. Someone is screaming "GO GO GO" in Discord. You just died in Merveil for the third time. You have no idea what the next zone is. Your party leader is already in Act 4.

**This overlay fixes that.**

`poe-act-rush-overlay` is a **transparent, always-on-top desktop overlay** for Path of Exile 1 that **automatically detects your current zone** by reading `Client.txt` and instantly tells you:

- 📍 **Where you are** — current zone name & act
- ✅ **What to do** — exact task list for this zone (kill X, pick up Y, use WP Z)
- 🧭 **Where to go next** — the precise next location from the ACT RUSH route
- 🟩 **Quest item alerts** — screams at you when there's something to pick up
- ⏱️ **A built-in speedrun timer** — start, pause, stop, auto-finish

Zero clicks. Zero alt-tabbing. Zero "wait where do I go" in party chat.

---

## 🎬 Demo

```
┌─────────────────────────────────────┐
│ ⚔ PoE Act Rush          F5=lock F6=reset  ✕ │
├─────────────────────────────────────┤
│  00:14:32                           │
│  [▶ RUNNING]  [■ STOP]  [⏸ PAUSE]  │
├─────────────────────────────────────┤
│  Weaver's Chambers                  │
│  Act 2                              │
│                                     │
│  ▸ Kill The Weaver                  │
│    Pick up Maligaro's Spike         │
│    TP → open blocked path           │
│                                     │
│  NEXT → Northern Forest             │
├─────────────────────────────────────┤
│  🟩 Pick up Maligaro's Spike!       │
├─────────────────────────────────────┤
│  Browse…  Reading: Client.txt       │
└─────────────────────────────────────┘
```

> *The overlay lives in the corner of your screen. PoE runs. You never touch it.*

---

## ⚡ Features

| Feature | Description |
|---|---|
| 🔍 **Auto zone detection** | Tails `Client.txt` live — no manual input ever |
| 🧭 **Next zone guidance** | Shows exactly where to go next per ACT RUSH route |
| 🟩 **Pickup alerts** | Highlights critical quest items the moment you enter a zone |
| ⏱️ **Speedrun timer** | Tracks your full 10-act run time with pause/resume support |
| 🏆 **Auto-finish detection** | Stops the clock when the run ends |
| 🔒 **Drag & lock** | `F5` locks the window in place — drag it anywhere first |
| 🔄 **Reset** | `F6` wipes the timer, ready for the next runner |
| 👻 **Transparent overlay** | Semi-transparent dark UI — never covers your game |
| 🎯 **10 acts, 85+ zones** | Full route from Act 1 Coast to Act 10 Kitava |
| 🚀 **Single `.exe`** | No Python, no installs — just run it |

---

## 🚀 Quick Start

### Option A — Just download and run (recommended)

1. Grab the latest `poe_overlay.exe` from [**Releases**](../../releases)
2. Double-click it
3. Done. Seriously.

> The overlay auto-detects `Client.txt` on startup for standard Steam and standalone PoE installs. If yours is somewhere unusual, click **Browse…** and point it at your `Client.txt`.

### Option B — Run from source

```bash
git clone https://github.com/yourname/poe-act-rush-overlay
cd poe-act-rush-overlay
pip install -r requirements.txt
python poe_overlay.py
```

**Requirements:** Python 3.10+, tkinter (bundled with Python on Windows), nothing else.

### Option C — Build it yourself

```bash
pip install pyinstaller
pyinstaller poe_overlay.spec
# → dist/poe_overlay.exe
```

---

## 🗺️ The Route

This overlay follows the **ACT RUSH** party leveling route — a highly optimized path through all 10 acts designed for fast, efficient progression. Every zone entry in the overlay corresponds 1:1 with the route.

<details>
<summary><b>📋 Full route overview (click to expand)</b></summary>

```
🟩 ACT 1  Coast → Mud Flats (3 Glyphs) → Submerged Passage → Flooded Depths (Dweller)
          → Lower/Upper Prison (Brutus) → Ship Graveyard Cave (Allflame, Fairgraves)
          → Cavern of Wrath → Cavern of Anger → Kill Merveil

⬜ ACT 2  Chamber of Sins 1→2 (Fidelitas) → Crypt 1→2 (Golden Hand)
          → Broken Bridge (Kraityn) → Wetlands (Oak) → Western Forest (Alira)
          → Weaver's Chambers (Weaver + Maligaro's Spike) → Northern Forest
          → Vaal Ruins (Apex) → Caverns → Ancient Pyramid (Vaal Oversoul)

✅ ACT 3  Crematorium (Piety) → Slums → Sewers (3 Busts) → Battlefront (Ribbon Spool)
          → Docks (Thaumetic Sulphate) → Solaris 2 (Dialla) → Ebony Barracks (Gravicius)
          → Lunaris 1→2 (Piety PP) → Imperial Gardens → Sceptre of God (Dominus)
          → Aqueduct → Highgate

🟪 ACT 4  Dried Lake (Voll) → Mines 1→2 (Deshret's Spirit) → Daresso's Dream (Daresso)
          → Kaom's Stronghold (Kaom) → Crystal Veins → Belly 1→2 → Bowels → Harvest (Malachai)

🟦 ACT 5  Ascent → Control Blocks → Oriath Square → Chamber of Innocence (Avarius)
          → Ruined Square → Reliquary (Torments PP) → Ossuary (Sign of Purity)
          → Cathedral Rooftop → Cathedral Apex → Kill Kitava

🟧 ACT 6  Coast → Mud Flats (Tukohama) → Lower Prison → Shavronne's Tower
          → Prisoner's Gate → Valley of Fire Drinker (Abberath) → Riverways (Puppet Mistress)
          → Southern Forest → Beacon → Brine King's Reef

🟥 ACT 7  Crypt (Maligaro's Map) → Chamber of Sins 1 (Map Device) → Ashen Fields (Greust)
          → Northern Forest → Dread Thicket (Fireflies, Gruthkul) → Causeway (Kishara's Star)
          → Vaal City → Temple of Decay 1→2 → Arakaali's Web → Kill Arakaali

🟪 ACT 8  Toxic Conduits → Doedre's Cesspool (Loose Crate, Doedre) → Sewer Outlet
          → Grain Gate (Maramoa) → Solaris 1→2 (Dawn) → Lunaris 1→2 (Dusk)
          → Bath House → High Gardens (Yugul) → Lunaris Concourse → Blood Aqueduct

🟦 ACT 9  Descent → Vastiri Desert (Shakari) → Foothills (Basilisk Acid)
          → Quarry (Shrine of Winds, Kira & Gurukhan, Refinery, Trarthan Powder)
          → Sin portal → Belly of the Beast → Rotting Core → Oriath

🟨 ACT 10 Cathedral Rooftop (Cultists) → Ravaged Square (Torched Courts)
          → Desecrated Chambers (Avarius) → Control Blocks (Vilenta)
          → Canals → Feeding Trough → Kill Kitava → /passives (24/24) ✅
```

</details>

---

## 🎮 Controls

| Key / Button | Action |
|---|---|
| `▶ START` | Begin the speedrun timer |
| `⏸ PAUSE` / `▶ RESUME` | Pause and resume mid-run |
| `■ STOP` | Manually stop the timer |
| `F5` | Toggle window lock/unlock (drag when unlocked) |
| `F6` | Reset timer — ready for next runner |
| `Browse…` | Manually select your `Client.txt` |
| `✕` | Close the overlay |

---

## 🧠 How it works

```
Client.txt  ──►  Background thread tails new lines
                        │
                        ▼
              Regex: "You have entered <Zone>."
                        │
                        ▼
              Zone matched against 85+ route entries
                        │
                        ▼
              Overlay updates: zone name, act, task list,
                               next location, pickup alert
```

No game memory reading. No injection. No hooks. Just a log file — the same way every legitimate PoE tool has worked for a decade.

---

## 🏗️ Project Structure

```
poe-act-rush-overlay/
├── poe_overlay.py      ← everything. one file. beautiful chaos.
├── poe_overlay.spec    ← PyInstaller build config
├── ACT_RUSH.txt        ← the sacred route document
└── README.md           ← you are here
```

---

## 🤝 Contributing

Found a zone that's missing? Route step that's wrong? Boss name that's off?

1. Fork it
2. Fix it
3. PR it

The route data lives in the `ROUTE` list at the top of `poe_overlay.py` — every entry has `zones`, `act`, `steps`, `next`, and `pickups`. Adding or editing zones takes about 30 seconds.

---

## 💬 FAQ

**Q: Does this work with PoE 2?**
No. This is built for Path of Exile 1 only. The acts, zones, and quest structure are completely different.

**Q: Will I get banned for using this?**
No. This only reads a log file. GGG explicitly allows tools that read `Client.txt`. No memory reading, no injection, no automation.

**Q: The overlay didn't detect my zone — why?**
Make sure the overlay is pointed at the right `Client.txt`. Also note it only reads *new* lines from when it starts — it won't catch zones you entered before launching the overlay.

**Q: Can I use this solo (not in a party rush)?**
Absolutely. It works for any run following this route, party or solo.

**Q: The "next zone" shown is wrong for my run.**
The next zone is hardcoded from the ACT RUSH route. If you're doing a different route, open a PR or fork it.

---

## ❤️ Credits

Route by the **ACT RUSH** community. Built for the runners, the followers, the people who type `+` in chat and have no idea what that means yet.

Special thanks to **@Nawied** — for providing hes rush route

---

<div align="center">

**⚔ May your maps be juiced and your deaths be few. ⚔**

*Made with spite, caffeine, and an intense desire to stop dying in Merveil.*

</div>
