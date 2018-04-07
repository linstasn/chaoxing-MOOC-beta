# coding:utf-8
import sys
import os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r'C:\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python36\tcl\tk8.6'
build_exe_options = {
    'packages': ['asyncio', 'idna', 'numpy'],
    'excludes': []
}

setup(
    name='erya',
    version='0.1',
    description='尔雅刷课',
    options={'build_exe': build_exe_options},
    executables=[Executable('rest_console.py')], requires=['wxpy', 'logzero']
)