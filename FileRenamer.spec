# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['file_renamer_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt6.QtCore', 
        'PyQt6.QtWidgets', 
        'PyQt6.QtGui',
        'pytesseract', 
        'pypdf', 
        'docx', 
        'chardet', 
        'PIL', 
        'PIL.Image'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'numpy', 'pandas', 'scipy', 'sklearn',
        'tensorflow', 'torch', 'jax', 'onnxruntime',
        'cv2', 'opencv', 'rapidocr',
        'tkinter', 'wx', 'kivy',
        'IPython', 'jupyter', 'notebook',
        'sphinx', 'docutils', 'pytest', 'unittest',
        'email', 'http', 'urllib3', 'requests',
        'sqlite3', 'xml', 'html', 'xmlrpc',
        'multiprocessing', 'concurrent', 'asyncio',
        'logging', 'argparse', 'getopt',
        'doctest', 'pdb', 'profile', 'cProfile'
    ],
    noarchive=False,
    optimize=2,  # 启用Python优化
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FileRenamer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # 启用strip减少二进制大小
    upx=True,    # 启用UPX压缩
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='FileRenamer.app',
    icon=None,
    bundle_identifier=None,
)
