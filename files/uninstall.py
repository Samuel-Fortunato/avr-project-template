#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path
import platform
import shutil as shutils

# Detect OS
is_windows = platform.system().lower() == "windows"
is_linux = platform.system().lower() == "linux"

# Root directory of the uninstall script (assumes same root as create_project.py and template/)
root_dir = Path(__file__).parent

# Paths to remove in project directory
script_path = root_dir / "create-project.py"
template_dir = root_dir / "template"
uninstaller_path = root_dir / "uninstall.py"

# Determine wrapper location dynamically using shutil.which
wrapper_name = "avr-new-project" + (".bat" if is_windows else "")
wrapper_path_str = shutils.which(wrapper_name)
wrapper_path = Path(wrapper_path_str) if wrapper_path_str else None

# Remove files/folders in root_dir except uninstall script
for path in [script_path, template_dir]:
    if path.exists():
        try:
            if path.is_dir():
                shutil.rmtree(path)
                print(f"✅ Removed directory: {path}")
            else:
                path.unlink()
                print(f"✅ Removed file: {path}")
        except Exception as e:
            print(f"❌ Failed to remove {path}: {e}")
    else:
        print(f"ℹ️ Not found (skipped): {path}")

# Remove wrapper if found
if wrapper_path and wrapper_path.exists():
    try:
        wrapper_path.unlink()
        print(f"✅ Removed wrapper: {wrapper_path}")
    except Exception as e:
        print(f"❌ Failed to remove wrapper: {e}")
else:
    print(f"ℹ️ Wrapper not found in PATH")

# Finally, remove the uninstall script and root folder.
try:
    uninstaller_path.unlink()
    print(f"✅ Removed uninstall script: {uninstaller_path}")
except Exception as e:
    print(f"❌ Failed to remove uninstall script: {e}")
  
try: 
    os.rmdir(root_dir) 
    print(f"✅ Removed root folder: {root_dir}") 
except Exception as e: 
    print(e) 
    print(f"❌ Failed to remove root folder: {e}")

# Pause if on Windows GUI
if is_windows:
    input("\nPress Enter to exit...")
