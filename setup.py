from distutils.core import setup
import py2exe

Data_Files = ['terminal12x12_gs_ro.png', 'libtcod-mingw.dll',
              'SDL.dll', 'README.txt']
setup(console=['12Down.py'],
      data_files=Data_Files,
      options={'py2exe': {'bundle_files': 1, 'compressed': True}},
      author='Akhier Dragonheart',
      description='A 7drl with 12 dungeon levels to explore',
      version='1.0',
      name='12Down')
