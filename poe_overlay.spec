# -*- mode: python ; coding: utf-8 -*-
# Cross-platform spec — works on both Windows and Linux.
# Windows:  pyinstaller poe_overlay.spec   →  dist/poe_overlay.exe
# Linux:    pyinstaller poe_overlay.spec   →  dist/poe_overlay

import sys

a = Analysis(
    ['poe_overlay.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter', 'tkinter.filedialog'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='poe_overlay',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    # Windows: hide the console window; Linux: no effect
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
