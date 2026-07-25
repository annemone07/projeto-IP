# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mainCode.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('sons/musicas', 'sons/musicas'),
        ('sons/soundEffects', 'sons/soundEffects'),
        ('images/backgrounds', 'images/backgrounds'),
        ('images/enemy', 'images/enemy'),
        ('images/items', 'images/items'),
        ('images/playerSprites', 'images/playerSprites'),
        ('images/SoundSprite', 'images/SoundSprite'),
        ('ranking.json', '.')
    ],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='mainCode',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='mainCode',
)
