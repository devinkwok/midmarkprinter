from distutils.core import setup
import py2exe

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    data_files = [('', ['printer-sound.wav'])],
    zipfile = None,
    console=["sterilizer-printer.py"]
    )