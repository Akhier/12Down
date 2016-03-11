from distutils.core import setup
import py2exe

Data_Files = ['terminal12x12_gs_ro.png', 'libtcod-mingw.dll', 'SDL.dll']
setup(console=['12Down.py'],
      data_files=Data_Files,
      options={'py2exe': {'bundle_files': 1, 'compressed': True}})
