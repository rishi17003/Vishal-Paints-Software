# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['src'],
    binaries=[],
    datas=[('product_rate.db', '.'), ('watermark.jpg', '.'),('C:/Users/Acer/Downloads/Vishal-Paints-Software-main_app/Vishal-Paints-Software-main/src/watermark.png', '.'),('product_rate_calculator.py', '.'),('HomeScreen.py', '.'),('InventoryDetailsScreen.py', '.'),('invoice_popup.py', '.'),('product_rate_calculator.py', '.'),('ProductHistoryScreen.py', '.'),('RawMaterialHistoryScreen.py', '.'),('RawMaterialManagementScreen.py', '.'), ('vishal_icon.ico', '.')],
    hiddenimports=['sqlite3', 'PyQt5','reportlab','reportlab.lib','reportlab.lib.pagesizes','reportlab.pdfgen','reportlab.lib.units','reportlab.platypus',],
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
    name='VishalPaints',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:/Users/Acer/Downloads/Vishal-Paints-Software-main_app/Vishal-Paints-Software-main/src/vishal_icon.ico'],
)
