application_title = "Firefly" #what you want to application to be called
main_python_file = "firefly.py" #the name of the python file you use to run the program

import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

includes = ["sys", "math", "random", "time", "socket"]

setup(
        name = "firefly",
        version = "0.1",
        description = "Sample cx_Freeze PyQt4 script",
        options = {"build_exe" : {"includes" : includes }},
        executables = [Executable(main_python_file, base = base)])
