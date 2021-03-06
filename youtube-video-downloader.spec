# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['youtube-video-downloader.py'],
             pathex=['YOUR_SCRIPT_FOLDER_PATH'],
             binaries=[],
             datas=[('YOUR_PYTHON_PATH\\lib\\site-packages\\eel\\eel.js', 'eel'), ('static', 'static')],
             hiddenimports=['bottle_websocket','pkg_resources.py2_warn'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Youtube Downloader',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False, icon='static\\src\\images\\downloader.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Youtube Video Downloader')
