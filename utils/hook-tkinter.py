"""
PyInstaller hook for tkinter package.

This hook ensures that tkinter and its native dependencies (_tkinter.so, libtk, libtcl)
are properly included in the PyInstaller bundle when building on Linux.
"""
from PyInstaller.utils.hooks import collect_submodules, get_module_file_attribute
import os
import sys

# Collect all tkinter submodules
hiddenimports = collect_submodules('tkinter')

# On Linux, we need to explicitly handle _tkinter shared library
if sys.platform.startswith('linux'):
    try:
        import _tkinter
        # Get the path to _tkinter module
        tkinter_path = get_module_file_attribute('_tkinter')
        if tkinter_path:
            print(f"Found _tkinter at: {tkinter_path}")
    except ImportError as e:
        print(f"Warning: Could not import _tkinter: {e}")
