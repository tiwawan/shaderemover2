import sys
from cx_Freeze import setup, Executable
 
# ----------------------------------------------------------------
# セットアップ
# ----------------------------------------------------------------
base = None

if sys.platform == 'win32' : base = 'Win32GUI'
 
# exe にしたい python ファイルを指定
exe = Executable(script = 'shaderemover.py',
                 base = base)
 
# セットアップ
setup(name = 'sample',
      version = '0.1',
      description = 'converter',
      executables = [exe])
