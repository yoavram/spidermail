# -*- mode: python -*-
a = Analysis(['spidermail.py'],
             pathex=['D:\\workspace\\spidermail'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='spidermail.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               [('cacert.pem', 'cacert.pem', 'DATA')],
               [('urls.txt', 'urls.txt', 'DATA')],
               strip=None,
               upx=True,
               name='spidermail')
