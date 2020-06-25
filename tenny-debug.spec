# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None


a = Analysis(['src\\main.py'],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[('qss/style.qss', 'qss'),
                    ('images/stopwatch.ico', 'images')],
             hiddenimports=[],
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
          name='tenny-0.6-win64-rc1',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='images\stopwatch.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='tenny-0.6-win64-rc1')
