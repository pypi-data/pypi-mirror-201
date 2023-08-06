# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata

datas = [
    ('..\\..\\..\\venv\\Lib\\site-packages\\fido2\\public_suffix_list.dat', 'fido2'),
    ('..\\..\\..\\pynitrokey\\VERSION', 'pynitrokey'),
    ('..\\..\\..\\LICENSE-APACHE', '.'),
    ('..\\..\\..\\LICENSE-MIT', '.')
]
datas += copy_metadata('pynitrokey')
datas += copy_metadata('ecdsa')
datas += copy_metadata('fido2')
datas += copy_metadata('pyusb')
datas += copy_metadata('spsdk')


block_cipher = None


a = Analysis(
    ['..\\..\\..\\nitropy.py'],
    pathex=[],
    binaries=[
        ('..\\..\\..\\venv\\Lib\\site-packages\\libusbsio\\bin\\x64\\libusbsio.dll', 'libusbsio'),
        ('..\\..\\..\\venv\\Lib\\site-packages\\usb1\\libusb-1.0.dll', '.')
    ],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='nitropy',
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
    icon=None,
    version='file_version_info.txt',
    uac_admin=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='nitropy',
)