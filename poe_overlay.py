"""
Path of Exile 1 - Act Rush Overlay
====================================
Reads PoE Client.txt, tracks zone progress and shows a timer.
Timer stops automatically on entering the Epilogue (after Kitava Act 10).

Controls:
  - Click START  → begin the stopwatch
  - F5           → lock / unlock window drag
  - F6           → reset timer
"""

import tkinter as tk
from tkinter import filedialog
import threading
import time
import os
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# ROUTE DATA  — based on ACT_RUSH.txt
# "steps"   = what to do next (shown in overlay)
# "pickups" = quest item reminders (shown as alert, no confirmation needed)
# ---------------------------------------------------------------------------

ROUTE: list[dict] = [
    # ── ACT 1 ──────────────────────────────────────────────────────────────
    {
        "zones": ["The Coast", "Coast"],
        "act": "Act 1",
        "steps": ["Mud Flats → collect 3 Glyphs"],
        "pickups": [],
    },
    {
        "zones": ["The Mud Flats", "Mud Flats"],
        "act": "Act 1",
        "steps": ["Collect 3 Glyphs", "→ Submerged Passage"],
        "pickups": ["🟩 Pick up Glyph!"],
    },
    {
        "zones": ["The Submerged Passage", "Submerged Passage"],
        "act": "Act 1",
        "steps": ["→ Flooded Depths", "Kill Dweller", "TP → Bestel"],
        "pickups": [],
    },
    {
        "zones": ["The Flooded Depths", "Flooded Depths"],
        "act": "Act 1",
        "steps": ["Kill The Dweller of the Deep", "TP → Lioneye's Watch → Bestel"],
        "pickups": [],
    },
    {
        "zones": ["The Lower Prison", "Lower Prison"],
        "act": "Act 1",
        "steps": ["→ Upper Prison", "Kill Brutus", "TP"],
        "pickups": [],
    },
    {
        "zones": ["The Upper Prison", "Upper Prison"],
        "act": "Act 1",
        "steps": ["Kill Brutus", "TP to town"],
        "pickups": [],
    },
    {
        "zones": ["Ship Graveyard"],
        "act": "Act 1",
        "steps": ["WP → Cave", "Allflame", "Kill Fairgraves", "→ Bestel"],
        "pickups": ["🟩 Pick up Allflame!"],
    },
    {
        "zones": ["Ship Graveyard Cave"],
        "act": "Act 1",
        "steps": ["Pick up Allflame", "Kill Fairgraves", "TP"],
        "pickups": ["🟩 Pick up Allflame!"],
    },
    {
        "zones": ["Cavern of Wrath"],
        "act": "Act 1",
        "steps": ["→ Cavern of Anger", "Kill Merveil"],
        "pickups": [],
    },
    {
        "zones": ["Cavern of Anger"],
        "act": "Act 1",
        "steps": ["Kill Merveil", "→ Southern Forest WP"],
        "pickups": [],
    },
    # ── ACT 2 ──────────────────────────────────────────────────────────────
    {
        "zones": ["The Southern Forest", "Southern Forest"],
        "act": "Act 2",
        "steps": ["→ Chamber of Sins 1 WP"],
        "pickups": [],
    },
    {
        "zones": ["Chamber of Sins Level 1", "Chamber of Sins 1"],
        "act": "Act 2",
        "steps": ["WP → Chamber of Sins 2", "Kill Fidelitas"],
        "pickups": [],
    },
    {
        "zones": ["Chamber of Sins Level 2", "Chamber of Sins 2"],
        "act": "Act 2",
        "steps": ["Kill Fidelitas", "TP"],
        "pickups": [],
    },
    {
        "zones": ["The Crypt Level 1", "Crypt Level 1", "Crypt 1"],
        "act": "Act 2",
        "steps": ["WP → Crypt 2", "Golden Hand PP → Yeena"],
        "pickups": ["🟩 Pick up Golden Hand!"],
    },
    {
        "zones": ["The Crypt Level 2", "Crypt Level 2", "Crypt 2"],
        "act": "Act 2",
        "steps": ["Golden Hand PP → TP → Yeena"],
        "pickups": ["🟩 Pick up Golden Hand!"],
    },
    {
        "zones": ["The Broken Bridge", "Broken Bridge"],
        "act": "Act 2",
        "steps": ["Kill Kraityn"],
        "pickups": [],
    },
    {
        "zones": ["The Wetlands", "Wetlands"],
        "act": "Act 2",
        "steps": ["Kill Oak"],
        "pickups": [],
    },
    {
        "zones": ["The Western Forest", "Western Forest"],
        "act": "Act 2",
        "steps": [
            "Kill Alira",
            "→ Weaver's Chambers → Kill Weaver → Maligaro's Spike",
            "Open the blocked path",
        ],
        "pickups": ["🟩 Pick up Maligaro's Spike after killing Weaver!"],
    },
    {
        "zones": ["The Weaver's Chambers", "Weaver's Chambers"],
        "act": "Act 2",
        "steps": ["Kill The Weaver", "Pick up Maligaro's Spike", "TP"],
        "pickups": ["🟩 Pick up Maligaro's Spike!"],
    },
    {
        "zones": ["The Northern Forest", "Northern Forest"],
        "act": "Act 2",
        "steps": ["→ Vaal Ruins", "Activate Apex DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["The Vaal Ruins", "Vaal Ruins"],
        "act": "Act 2",
        "steps": ["Activate Apex", "DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["The Caverns", "Caverns"],
        "act": "Act 2",
        "steps": ["WP → Ancient Pyramid"],
        "pickups": [],
    },
    {
        "zones": ["The Ancient Pyramid", "Ancient Pyramid"],
        "act": "Act 2",
        "steps": ["Kill Vaal Oversoul", "→ Act 3"],
        "pickups": [],
    },
    # ── ACT 3 ──────────────────────────────────────────────────────────────
    {
        "zones": ["The Crematorium", "Crematorium"],
        "act": "Act 3",
        "steps": ["WP → Kill Piety", "TP → Clarissa w mieście"],
        "pickups": [],
    },
    {
        "zones": ["The Slums", "Slums"],
        "act": "Act 3",
        "steps": ["→ Sewers WP", "Collect 3 Busts", "DC/TP"],
        "pickups": ["🟩 Collect all 3 Busts!"],
    },
    {
        "zones": ["The Sewers", "Sewers"],
        "act": "Act 3",
        "steps": ["Collect 3 Busts", "DC/TP"],
        "pickups": ["🟩 Collect all 3 Busts!"],
    },
    {
        "zones": ["The Battlefront", "Battlefront"],
        "act": "Act 3",
        "steps": ["WP → Ribbon Spool", "→ Docks → Thaumetic Sulphate"],
        "pickups": ["🟩 Pick up Ribbon Spool!"],
    },
    {
        "zones": ["The Docks", "Docks"],
        "act": "Act 3",
        "steps": ["Find and pick up Thaumetic Sulphate", "TP"],
        "pickups": ["🟩 Pick up Thaumetic Sulphate!"],
    },
    {
        "zones": ["The Solaris Temple Level 2", "Solaris Temple Level 2", "Solaris 2"],
        "act": "Act 3",
        "steps": ["WP → Lady Dialla", "→ Sewers (znowu) → Ebony Barracks"],
        "pickups": [],
    },
    {
        "zones": ["The Ebony Barracks", "Ebony Barracks"],
        "act": "Act 3",
        "steps": ["WP → [N] Kill Gravicius", "DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["The Lunaris Temple Level 1", "Lunaris Temple Level 1", "Lunaris 1"],
        "act": "Act 3",
        "steps": ["WP → Lunaris 2", "Kill Piety PP", "DC/TP → Grigor"],
        "pickups": [],
    },
    {
        "zones": ["The Lunaris Temple Level 2", "Lunaris Temple Level 2", "Lunaris 2"],
        "act": "Act 3",
        "steps": ["Kill Piety PP", "DC/TP → Grigor"],
        "pickups": [],
    },
    {
        "zones": ["The Imperial Gardens", "Imperial Gardens"],
        "act": "Act 3",
        "steps": ["WP → Lower Sceptre → Upper Sceptre WP", "Kill Dominus"],
        "pickups": [],
    },
    {
        "zones": ["The Lower Sceptre of God", "Lower Sceptre of God"],
        "act": "Act 3",
        "steps": ["→ Upper Sceptre of God"],
        "pickups": [],
    },
    {
        "zones": ["The Upper Sceptre of God", "Upper Sceptre of God"],
        "act": "Act 3",
        "steps": ["Kill High Templar Dominus", "→ Aqueduct WP → Highgate"],
        "pickups": [],
    },
    {
        "zones": ["The Aqueduct", "Aqueduct"],
        "act": "Act 3",
        "steps": ["WP → Highgate"],
        "pickups": [],
    },
    # ── ACT 4 ──────────────────────────────────────────────────────────────
    {
        "zones": ["The Dried Lake", "Dried Lake"],
        "act": "Act 4",
        "steps": ["Kill Voll", "DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["The Mines Level 1", "Mines Level 1", "Mines 1"],
        "act": "Act 4",
        "steps": ["→ Mines 2", "Deshret's Spirit PP", "DC/TP"],
        "pickups": ["🟩 Pick up Deshret's Spirit PP!"],
    },
    {
        "zones": ["The Mines Level 2", "Mines Level 2", "Mines 2"],
        "act": "Act 4",
        "steps": ["Deshret's Spirit PP", "DC/TP"],
        "pickups": ["🟩 Pick up Deshret's Spirit PP!"],
    },
    {
        "zones": ["Daresso's Dream"],
        "act": "Act 4",
        "steps": ["→ Grand Arena", "Kill Daresso"],
        "pickups": [],
    },
    {
        "zones": ["The Grand Arena", "Grand Arena"],
        "act": "Act 4",
        "steps": ["Kill King Daresso"],
        "pickups": [],
    },
    {
        "zones": ["Kaom's Stronghold"],
        "act": "Act 4",
        "steps": ["Kill King Kaom", "DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["Crystal Veins"],
        "act": "Act 4",
        "steps": ["Dialla → Belly 1 → Belly 2 → Bowels → Piety → Harvest"],
        "pickups": [],
    },
    {
        "zones": ["The Belly of the Beast Level 1", "Belly of the Beast Level 1", "Belly of the Beast"],
        "act": "Act 4",
        "steps": ["→ Belly 2 → Bowels → Kill Piety → Harvest"],
        "pickups": [],
    },
    {
        "zones": ["The Belly of the Beast Level 2", "Belly of the Beast Level 2"],
        "act": "Act 4",
        "steps": ["→ Bowels of the Beast → Kill Piety → Harvest"],
        "pickups": [],
    },
    {
        "zones": ["The Bowels of the Beast", "Bowels of the Beast"],
        "act": "Act 4",
        "steps": ["Kill Piety → Harvest"],
        "pickups": [],
    },
    {
        "zones": ["The Harvest"],
        "act": "Act 4",
        "steps": ["Kill 3 Guardians", "Black Core", "Kill Malachai", "DC/TP"],
        "pickups": [],
    },
    # ── ACT 5 ──────────────────────────────────────────────────────────────
    {
        "zones": ["The Ascent", "Ascent"],
        "act": "Act 5",
        "steps": ["Oriath Portal WP → Kill Overseer Crow → Overseer's Tower"],
        "pickups": [],
    },
    {
        "zones": ["The Control Blocks", "Control Blocks"],
        "act": "Act 5",
        "steps": ["Supplies PP → Kill Justicar Casticus"],
        "pickups": ["🟩 Pick up Supplies PP!"],
    },
    {
        "zones": ["Oriath Square"],
        "act": "Act 5",
        "steps": ["WP → Chamber of Innocence"],
        "pickups": [],
    },
    {
        "zones": ["The Chamber of Innocence", "Chamber of Innocence"],
        "act": "Act 5",
        "steps": ["WP → Kill High Templar Avarius", "DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["The Ruined Square", "Ruined Square"],
        "act": "Act 5",
        "steps": [
            "WP → Reliquary → Kitava's Torments PP → DC/TP",
            "Ossuary → Sign of Purity → DC/TP",
            "Cathedral Rooftop → Apex → Kill Kitava",
        ],
        "pickups": ["🟩 Pick up Kitava's Torments PP!", "🟩 Sign of Purity"],
    },
    {
        "zones": ["The Reliquary", "Reliquary"],
        "act": "Act 5",
        "steps": ["WP → Kitava's Torments PP", "DC/TP"],
        "pickups": ["🟩 Pick up Kitava's Torments PP!"],
    },
    {
        "zones": ["The Ossuary", "Ossuary"],
        "act": "Act 5",
        "steps": ["Sign of Purity", "DC/TP"],
        "pickups": ["🟩 Pick up Sign of Purity!"],
    },
    {
        "zones": ["Cathedral Rooftop"],
        "act": "Act 5",
        "steps": ["→ Cathedral Apex", "Kill Kitava"],
        "pickups": [],
    },
    {
        "zones": ["Cathedral Apex"],
        "act": "Act 5",
        "steps": ["Kill Kitava", "→ Wraeclast"],
        "pickups": [],
    },
    # ── ACT 6 ──────────────────────────────────────────────────────────────
    {
        "zones": ["The Coast (Act 6)", "Coast (Act 6)"],
        "act": "Act 6",
        "steps": [
            "WP → Mud Flats → Forgotten Warrior",
            "Karui Fortress → Tukohama's Keep",
            "Kill Tukohama PP → DC/TP",
        ],
        "pickups": [],
    },
    {
        "zones": ["The Lower Prison (Act 6)", "Lower Prison (Act 6)"],
        "act": "Act 6",
        "steps": ["WP → Shavronne's Tower → Prison Rooftop"],
        "pickups": [],
    },
    {
        "zones": ["Shavronne's Tower"],
        "act": "Act 6",
        "steps": ["DC? → Warden's Chambers → Prisoner's Gate WP"],
        "pickups": [],
    },
    {
        "zones": ["Prisoner's Gate"],
        "act": "Act 6",
        "steps": ["WP → Valley of the Fire Drinker", "Kill Abberath PP → DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["The Riverways", "Riverways"],
        "act": "Act 6",
        "steps": ["WP → Wetlands → Spawning Grounds", "Kill Puppet Mistress PP → DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["The Southern Forest (Act 6)", "Southern Forest (Act 6)"],
        "act": "Act 6",
        "steps": ["WP → Cavern of Anger [Flag] → Beacon WP → Brine King's Reef"],
        "pickups": [],
    },
    # ── ACT 7 ──────────────────────────────────────────────────────────────
    {
        "zones": ["The Crypt (Act 7)", "Crypt (Act 7)"],
        "act": "Act 7",
        "steps": ["WP → Maligaro's Map → DC/TP"],
        "pickups": ["🟩 Pick up Maligaro's Map!"],
    },
    {
        "zones": ["Chamber of Sins Level 1 (Act 7)", "Chamber of Sins 1 (Act 7)"],
        "act": "Act 7",
        "steps": ["WP → Map Device (Maligaro's Map)", "→ Chamber of Sins 2 → Den"],
        "pickups": [],
    },
    {
        "zones": ["The Ashen Fields", "Ashen Fields"],
        "act": "Act 7",
        "steps": ["WP → Fortress Encampment", "Kill Greust PP → DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["The Northern Forest (Act 7)", "Northern Forest (Act 7)"],
        "act": "Act 7",
        "steps": ["→ Dread Thicket → Fireflies", "Den of Despair → Kill Gruthkul PP → DC/TP"],
        "pickups": ["🟩 Collect Fireflies!"],
    },
    {
        "zones": ["The Causeway", "Causeway"],
        "act": "Act 7",
        "steps": ["Kishara's Star PP → DC/TP"],
        "pickups": ["🟩 Pick up Kishara's Star PP!"],
    },
    {
        "zones": ["The Vaal City", "Vaal City"],
        "act": "Act 7",
        "steps": ["WP → Temple of Decay 1 → 2 → Arakaali's Web", "Kill Arakaali → Sarn Ramparts WP"],
        "pickups": [],
    },
    # ── ACT 8 ──────────────────────────────────────────────────────────────
    {
        "zones": ["The Toxic Conduits", "Toxic Conduits"],
        "act": "Act 8",
        "steps": ["Doedre's Cesspool → Loose Crate", "Kill Doedre the Vile → Sewer Outlet WP"],
        "pickups": ["🟩 Find the Loose Crate!"],
    },
    {
        "zones": ["The Sewer Outlet", "Sewer Outlet"],
        "act": "Act 8",
        "steps": ["WP → Quay → Ankh of Eternity → Resurrection Site → Tolman"],
        "pickups": [],
    },
    {
        "zones": ["The Grain Gate", "Grain Gate"],
        "act": "Act 8",
        "steps": ["WP → Gemling Legionnaires (Maramoa) → DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["The Solaris Temple Level 1 (Act 8)", "Solaris Temple 1 (Act 8)"],
        "act": "Act 8",
        "steps": ["WP → Solaris Temple 2 → Dawn → DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["The Lunaris Temple Level 1 (Act 8)", "Lunaris Temple 1 (Act 8)"],
        "act": "Act 8",
        "steps": ["WP → Lunaris Temple 2 → Dusk → DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["The Bath House", "Bath House"],
        "act": "Act 8",
        "steps": ["WP → High Gardens → Pool of Terror", "Kill Yugul PP (Hargan) → DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["The Lunaris Concourse", "Lunaris Concourse"],
        "act": "Act 8",
        "steps": ["WP → Harbour Bridge → Sky Shrine → Solaris & Lunar", "Blood Aqueduct → Highgate"],
        "pickups": [],
    },
    # ── ACT 9 ──────────────────────────────────────────────────────────────
    {
        "zones": ["The Descent", "Descent"],
        "act": "Act 9",
        "steps": ["→ Supply Hoists"],
        "pickups": [],
    },
    {
        "zones": ["The Vastiri Desert", "Vastiri Desert"],
        "act": "Act 9",
        "steps": ["WP → PP1 Storm Chest → Oasis (Portal outside TP)", "Sin, Irasha, Petrus → Shakari"],
        "pickups": ["🟩 Pick up PP1 Storm Chest!"],
    },
    {
        "zones": ["The Foothills", "Foothills"],
        "act": "Act 9",
        "steps": ["WP → Boiling Lake → Basilisk Acid → DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["The Quarry", "Quarry"],
        "act": "Act 9",
        "steps": [
            "WP → Shrine of the Winds [L] → Kira & Gurukhan",
            "Refinery [R] → Trarthan Powder → DC/TP",
            "Sin → Belly of the Beast → Rotting Core → Oriath",
        ],
        "pickups": ["🟩 Pick up Trarthan Powder!"],
    },
    # ── ACT 10 ─────────────────────────────────────────────────────────────
    {
        "zones": ["Cathedral Rooftop (Act 10)"],
        "act": "Act 10",
        "steps": ["Kill Kitava's Cultists"],
        "pickups": [],
    },
    {
        "zones": ["The Ravaged Square", "Ravaged Square"],
        "act": "Act 10",
        "steps": ["WP [N] → Torched Courts"],
        "pickups": [],
    },
    {
        "zones": ["The Desecrated Chambers", "Desecrated Chambers"],
        "act": "Act 10",
        "steps": ["WP → Sanctum of Innocence → Kill Avarius → DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["The Control Blocks (Act 10)", "Control Blocks (Act 10)"],
        "act": "Act 10",
        "steps": ["WP → Kill Vilenta → DC/TP"],
        "pickups": [],
    },
    {
        "zones": ["The Canals", "Canals"],
        "act": "Act 10",
        "steps": ["Ravaged Square → Innocence → Canals → Feeding Through → Kill Kitava → KONIEC!"],
        "pickups": [],
    },
    {
        "zones": ["The Feeding Trough", "Feeding Trough", "Feeding Through"],
        "act": "Act 10",
        "steps": ["Kill Kitava — OSTATNI BOSS!", "KONIEC!"],
        "pickups": [],
    },
]

# ---------------------------------------------------------------------------
# Flatten ROUTE into lookup dict
# ---------------------------------------------------------------------------

ZONE_MAP: dict[str, dict] = {}
for _entry in ROUTE:
    for _zone in _entry["zones"]:
        ZONE_MAP[_zone.lower()] = _entry


def match_zone(zone_name: str) -> dict | None:
    """Return route entry for a zone name (exact then fuzzy substring match)."""
    zl = zone_name.lower()
    if zl in ZONE_MAP:
        return ZONE_MAP[zl]
    for key, entry in ZONE_MAP.items():
        if key in zl or zl in key:
            return entry
    return None


# ---------------------------------------------------------------------------
# Finish-line detection
# ---------------------------------------------------------------------------
FINISH_ZONES = {"oriath", "karui shores"}

# ---------------------------------------------------------------------------
# Default Client.txt locations — PoE 1 only
# ---------------------------------------------------------------------------
DEFAULT_LOG_PATHS = [
    r"C:\Program Files (x86)\Grinding Gear Games\Path of Exile\logs\Client.txt",
    r"C:\Program Files\Grinding Gear Games\Path of Exile\logs\Client.txt",
    r"C:\Program Files (x86)\Steam\steamapps\common\Path of Exile\logs\Client.txt",
    r"C:\Program Files\Steam\steamapps\common\Path of Exile\logs\Client.txt",
    str(Path.home() / "Games" / "Path of Exile" / "logs" / "Client.txt"),
]

ZONE_PATTERN = re.compile(r": You have entered (.+)\.")

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
BG_COLOR     = "#0d0d0f"
BG_ALPHA     = 0.72
ACCENT_COLOR = "#c8a96e"
TEXT_COLOR   = "#e8e0d0"
DIM_COLOR    = "#7a7265"
GREEN_COLOR  = "#5ec45e"
GOLD_COLOR   = "#ffd700"
BORDER_COLOR = "#2a2520"

ACT_COLORS = {
    "Act 1":  "#9ab8d8",
    "Act 2":  "#a8d89a",
    "Act 3":  "#d8b89a",
    "Act 4":  "#b89ad8",
    "Act 5":  "#d89ab8",
    "Act 6":  "#9ab8d8",
    "Act 7":  "#a8d89a",
    "Act 8":  "#d8b89a",
    "Act 9":  "#b89ad8",
    "Act 10": "#d8c85e",
}

TIMER_IDLE    = "idle"
TIMER_RUNNING = "running"
TIMER_PAUSED  = "paused"
TIMER_STOPPED = "stopped"


# ===========================================================================
# OVERLAY APPLICATION
# ===========================================================================

class PoEOverlay:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PoE Act Rush")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", BG_ALPHA)
        self.root.configure(bg=BG_COLOR)

        self.log_path: str = ""
        self.locked: bool = False
        self.current_zone: str = ""
        self.current_entry: dict | None = None

        self.timer_state: str = TIMER_IDLE
        self.start_time: float = 0.0
        self.elapsed_frozen: float = 0.0

        self._drag_x = 0
        self._drag_y = 0

        self._build_ui()

        # Auto-detect log
        for p in DEFAULT_LOG_PATHS:
            if os.path.isfile(p):
                self.log_path = p
                self._set_status(f"Log: …{p[-45:]}")
                break

        self._stop_event = threading.Event()
        threading.Thread(target=self._tail_log, daemon=True).start()

        self._tick()

        self.root.bind("<F5>", self._toggle_lock)
        self.root.bind("<F6>", self._reset_timer)

        self.root.geometry("+20+20")

    # ── UI construction ───────────────────────────────────────────────────

    def _build_ui(self):
        W = 340

        outer = tk.Frame(self.root, bg=BORDER_COLOR)
        outer.pack(fill="both", expand=True, padx=1, pady=1)

        self.inner = tk.Frame(outer, bg=BG_COLOR)
        self.inner.pack(fill="both", expand=True, padx=1, pady=1)
        inner = self.inner

        # Header bar
        header = tk.Frame(inner, bg="#161412", height=28)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="⚔ PoE Act Rush",
            fg=ACCENT_COLOR, bg="#161412",
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left", padx=8, pady=4)

        tk.Button(
            header, text="✕",
            command=self.root.destroy,
            fg="#c45e5e", bg="#161412",
            activeforeground="#ff4444", activebackground="#161412",
            font=("Segoe UI", 9, "bold"),
            relief="flat", cursor="hand2", bd=0,
        ).pack(side="right", padx=6, pady=2)

        tk.Label(
            header, text="F5=lock  F6=reset",
            fg=DIM_COLOR, bg="#161412",
            font=("Segoe UI", 7),
        ).pack(side="right", padx=4, pady=4)

        header.bind("<ButtonPress-1>",   self._drag_start)
        header.bind("<B1-Motion>",       self._drag_motion)

        # Timer
        timer_frame = tk.Frame(inner, bg=BG_COLOR)
        timer_frame.pack(fill="x", padx=8, pady=(6, 2))

        self.timer_lbl = tk.Label(
            timer_frame, text="00:00",
            fg=ACCENT_COLOR, bg=BG_COLOR,
            font=("Consolas", 26, "bold"),
        )
        self.timer_lbl.pack(side="left")

        # Start / Stop buttons
        self.start_frame = tk.Frame(inner, bg=BG_COLOR)
        self.start_frame.pack(fill="x", padx=8, pady=2)

        self.start_btn = tk.Button(
            self.start_frame,
            text="▶  START",
            command=self._start_timer,
            bg="#1e3a1e", fg="#5ec45e",
            activebackground="#2a4a2a",
            font=("Segoe UI", 9, "bold"),
            relief="flat", cursor="hand2",
        )
        self.start_btn.pack(side="left", fill="x", expand=True)

        self.stop_btn = tk.Button(
            self.start_frame,
            text="■  STOP",
            command=self._stop_timer,
            bg="#3a1e1e", fg="#c45e5e",
            activebackground="#4a2a2a",
            font=("Segoe UI", 9, "bold"),
            relief="flat", cursor="hand2",
            state="disabled",
        )
        self.stop_btn.pack(side="left", fill="x", expand=True, padx=(4, 0))

        self.pause_btn = tk.Button(
            self.start_frame,
            text="⏸  PAUSE",
            command=self._pause_timer,
            bg="#2a2a1e", fg="#c4b45e",
            activebackground="#3a3a2a",
            font=("Segoe UI", 9, "bold"),
            relief="flat", cursor="hand2",
            state="disabled",
        )
        self.pause_btn.pack(side="left", fill="x", expand=True, padx=(4, 0))

        # Separator
        tk.Frame(inner, bg=BORDER_COLOR, height=1).pack(fill="x", padx=8, pady=4)

        # Zone label
        self.zone_lbl = tk.Label(
            inner, text="— waiting for zone —",
            fg=TEXT_COLOR, bg=BG_COLOR,
            font=("Segoe UI", 10, "bold"), anchor="w", wraplength=320,
        )
        self.zone_lbl.pack(fill="x", padx=8)

        self.act_lbl = tk.Label(
            inner, text="",
            fg=DIM_COLOR, bg=BG_COLOR,
            font=("Segoe UI", 8), anchor="w",
        )
        self.act_lbl.pack(fill="x", padx=8)

        # Steps area
        self.steps_frame = tk.Frame(inner, bg=BG_COLOR)
        self.steps_frame.pack(fill="x", padx=8, pady=(4, 2))
        self.step_labels: list[tk.Label] = []

        # Alert (pickup) — simple display only, no confirm
        self.alert_divider = tk.Frame(inner, bg="#1e3a1e", height=1)
        self.alert_lbl = tk.Label(
            inner, text="",
            fg=GREEN_COLOR, bg=BG_COLOR,
            font=("Segoe UI", 9, "bold"), anchor="w", wraplength=320,
        )
        self.alert_lbl.pack(fill="x", padx=8, pady=(0, 4))

        # Finish banner (hidden initially)
        self.finish_frame = tk.Frame(inner, bg="#1a1400")
        self.finish_lbl = tk.Label(
            self.finish_frame, text="",
            fg=GOLD_COLOR, bg="#1a1400",
            font=("Segoe UI", 10, "bold"), wraplength=320,
        )
        self.finish_lbl.pack(fill="x", padx=8, pady=4)

        # Browse + status
        bottom = tk.Frame(inner, bg=BG_COLOR)
        bottom.pack(fill="x", padx=8, pady=(2, 6))

        tk.Button(
            bottom, text="Browse…",
            command=self._browse_log,
            bg="#1a1a22", fg=DIM_COLOR,
            activebackground="#2a2a32",
            font=("Segoe UI", 8), relief="flat", cursor="hand2",
        ).pack(side="left")

        self.status_lbl = tk.Label(
            bottom, text="Looking for Client.txt…",
            fg=DIM_COLOR, bg=BG_COLOR,
            font=("Segoe UI", 7), anchor="w",
        )
        self.status_lbl.pack(side="left", padx=6, fill="x", expand=True)

        self.root.minsize(W, 10)

    # ── Drag ─────────────────────────────────────────────────────────────

    def _drag_start(self, event):
        if not self.locked:
            self._drag_x = event.x_root - self.root.winfo_x()
            self._drag_y = event.y_root - self.root.winfo_y()

    def _drag_motion(self, event):
        if not self.locked:
            x = event.x_root - self._drag_x
            y = event.y_root - self._drag_y
            self.root.geometry(f"+{x}+{y}")

    # ── Hotkeys ──────────────────────────────────────────────────────────

    def _toggle_lock(self, event=None):
        self.locked = not self.locked
        self._set_status("Window LOCKED" if self.locked else "Unlocked — drag the header")

    def _reset_timer(self, event=None):
        self.timer_state = TIMER_IDLE
        self.start_time = 0.0
        self.elapsed_frozen = 0.0
        self.timer_lbl.config(text="00:00", fg=ACCENT_COLOR)
        self.start_btn.config(text="▶  START", state="normal",
                              bg="#1e3a1e", fg="#5ec45e")
        self.stop_btn.config(state="disabled")
        self.pause_btn.config(state="disabled", text="⏸  PAUSE", bg="#2a2a1e", fg="#c4b45e")
        self.finish_frame.pack_forget()

    # ── Status bar ───────────────────────────────────────────────────────

    def _set_status(self, msg: str):
        self.status_lbl.config(text=msg)

    # ── Browse ───────────────────────────────────────────────────────────

    def _browse_log(self, event=None):
        path = filedialog.askopenfilename(
            title="Select Client.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if path:
            self.log_path = path
            self._set_status(f"Log: …{path[-45:]}")

    # ── Timer ─────────────────────────────────────────────────────────────

    def _start_timer(self):
        if self.timer_state != TIMER_IDLE:
            return
        self.start_time = time.time()
        self.timer_state = TIMER_RUNNING
        self.start_btn.config(
            text="● RUNNING",
            state="disabled",
            bg="#0d0d0f",
            fg=DIM_COLOR,
        )
        self.stop_btn.config(state="normal")
        self.pause_btn.config(state="normal", text="⏸  PAUSE", bg="#2a2a1e", fg="#c4b45e")

    def _stop_timer(self):
        """Manual STOP button — freezes timer without finishing the run."""
        if self.timer_state != TIMER_RUNNING:
            return
        self.elapsed_frozen = time.time() - self.start_time
        self.timer_state = TIMER_STOPPED
        final_str = self._format_elapsed(self.elapsed_frozen)
        self.timer_lbl.config(text=final_str, fg=ACCENT_COLOR)
        self.start_btn.config(
            text=f"⏸ STOPPED — {final_str}",
            state="disabled",
            bg="#0d0d0f",
            fg=DIM_COLOR,
        )
        self.stop_btn.config(state="disabled")
        self._set_status(f"Timer stopped at {final_str} — press F6 to reset")

    def _pause_timer(self):
        if self.timer_state == TIMER_RUNNING:
            # Pause — freeze elapsed
            self.elapsed_frozen = time.time() - self.start_time
            self.timer_state = TIMER_PAUSED
            self.pause_btn.config(text="▶  RESUME", bg="#1e3a1e", fg="#5ec45e")
            self.stop_btn.config(state="disabled")
            self._set_status("Timer paused — click RESUME to continue")
        elif self.timer_state == TIMER_PAUSED:
            # Resume — adjust start_time so elapsed continues from frozen point
            self.start_time = time.time() - self.elapsed_frozen
            self.timer_state = TIMER_RUNNING
            self.pause_btn.config(text="⏸  PAUSE", bg="#2a2a1e", fg="#c4b45e")
            self.stop_btn.config(state="normal")
            self._set_status(f"Reading: {os.path.basename(self.log_path)}" if self.log_path else "Running…")

    def _format_elapsed(self, seconds: float) -> str:
        s = int(seconds)
        mm, ss = divmod(s, 60)
        hh, mm = divmod(mm, 60)
        if hh:
            return f"{hh:02d}:{mm:02d}:{ss:02d}"
        return f"{mm:02d}:{ss:02d}"

    def _tick(self):
        if self.timer_state == TIMER_RUNNING:
            elapsed = time.time() - self.start_time
            self.timer_lbl.config(text=self._format_elapsed(elapsed))
        elif self.timer_state == TIMER_PAUSED:
            self.timer_lbl.config(text=self._format_elapsed(self.elapsed_frozen))
        self.root.after(500, self._tick)

    def _on_run_finished(self, zone_name: str):
        if self.timer_state != TIMER_RUNNING:
            return
        self.elapsed_frozen = time.time() - self.start_time
        self.timer_state = TIMER_STOPPED

        final_str = self._format_elapsed(self.elapsed_frozen)
        self.timer_lbl.config(text=final_str, fg=GOLD_COLOR)

        self.start_btn.config(
            text=f"🏁  DONE — {final_str}",
            state="disabled",
            bg="#1a1400",
            fg=GOLD_COLOR,
        )
        self.stop_btn.config(state="disabled")
        self.pause_btn.config(state="disabled")

        self.finish_lbl.config(text=f"🏆 Run complete! Final time: {final_str}")
        self.finish_frame.pack(fill="x", padx=8, pady=(0, 4))

        self._set_status(f"Entered {zone_name} — run finished!")

    # ── Zone update ──────────────────────────────────────────────────────

    def _update_zone(self, zone_name: str):
        if zone_name == self.current_zone:
            return
        self.current_zone = zone_name

        # Auto-finish disabled — use STOP button manually
        zone_lower = zone_name.lower()

        self.current_entry = match_zone(zone_name)
        self.zone_lbl.config(text=zone_name)

        if self.current_entry:
            act = self.current_entry.get("act", "")
            self.act_lbl.config(text=act, fg=ACT_COLORS.get(act, TEXT_COLOR))

            for lbl in self.step_labels:
                lbl.destroy()
            self.step_labels.clear()

            for i, step in enumerate(self.current_entry.get("steps", [])):
                prefix = "▸ " if i == 0 else "  "
                color  = TEXT_COLOR if i == 0 else DIM_COLOR
                lbl = tk.Label(
                    self.steps_frame, text=f"{prefix}{step}",
                    fg=color, bg=BG_COLOR,
                    font=("Segoe UI", 9), anchor="w", wraplength=310, justify="left",
                )
                lbl.pack(fill="x")
                self.step_labels.append(lbl)

            pickups = self.current_entry.get("pickups", [])
            if pickups:
                # Show all pickups for this zone joined in one label
                self.alert_lbl.config(text="  ".join(pickups), fg=GREEN_COLOR)
                self.alert_divider.pack(fill="x", padx=8, pady=2)
            else:
                self.alert_lbl.config(text="")
                self.alert_divider.pack_forget()
        else:
            self.act_lbl.config(text="", fg=DIM_COLOR)
            for lbl in self.step_labels:
                lbl.destroy()
            self.step_labels.clear()
            u = tk.Label(
                self.steps_frame, text="Zone not in route — free roam",
                fg=DIM_COLOR, bg=BG_COLOR, font=("Segoe UI", 9, "italic"), anchor="w",
            )
            u.pack(fill="x")
            self.step_labels.append(u)
            self.alert_lbl.config(text="")
            self.alert_divider.pack_forget()

    # ── Log tailing ──────────────────────────────────────────────────────

    def _tail_log(self):
        wait_logged = False
        while not self._stop_event.is_set():
            if not self.log_path or not os.path.isfile(self.log_path):
                if not wait_logged:
                    self.root.after(0, self._set_status, "Waiting for Client.txt…")
                    wait_logged = True
                time.sleep(1)
                continue

            wait_logged = False
            try:
                with open(self.log_path, "r", encoding="utf-8", errors="replace") as f:
                    # Seek to the very end — only watch NEW lines from here
                    f.seek(0, 2)

                    self.root.after(
                        0, self._set_status,
                        f"Reading: {os.path.basename(self.log_path)}",
                    )

                    prev_path = self.log_path
                    while not self._stop_event.is_set():
                        # Restart tail if user picked a new file via Browse
                        if self.log_path != prev_path:
                            break
                        line = f.readline()
                        if not line:
                            time.sleep(0.3)
                            continue
                        m = ZONE_PATTERN.search(line)
                        if m:
                            zone = m.group(1).strip()
                            self.root.after(0, self._update_zone, zone)
            except Exception as exc:
                self.root.after(0, self._set_status, f"Log error: {exc}")
                time.sleep(3)


# ===========================================================================
# ENTRY POINT
# ===========================================================================

def main():
    root = tk.Tk()
    PoEOverlay(root)
    root.mainloop()


if __name__ == "__main__":
    main()