# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\jwgle\\PycharmProjects\\Sorteerhoed'],
             binaries=[],
             datas=[('questions/*.txt', 'questions'), ('magichat.ico', '.')],
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
          name='Sorteerhoed INF1J',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          icon='magichat.ico',
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Sorteerhoed INF1J')
app = BUNDLE(exe,
         name='Sorteerhoed INF1J.app',
         icon='magichat.ico',
         bundle_identifier='inf1j.sorteerhoed')
