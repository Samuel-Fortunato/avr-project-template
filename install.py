#!/usr/bin/env python3
import os
import sys
import shutil
import platform
from pathlib import Path

COMMAND_NAME = "avr-new-project"    # command run by user
SCRIPT_NAME = "create-project.py"
INSTALL_NAME = "avr-project-template"

# Source folder (where installer is run from)
source_dir = Path(__file__).parent

# Detect OS
is_windows = platform.system().lower() == "windows"
is_linux = platform.system().lower() == "linux"

# Install location (where the project will live permanently)
if is_windows:
    install_dir = Path(os.environ["USERPROFILE"]) / "Scripts" / INSTALL_NAME
    wrapper_dir = Path(os.environ["USERPROFILE"]) / "Scripts"
elif is_linux:
    install_dir = Path.home() / ".local" / "share" / INSTALL_NAME
    wrapper_dir = Path.home() / ".local" / "bin"
else:
    print("ERROR: Failed to detect OS")
    if is_windows:
        input("Press Enter to exit...")
    sys.exit(1)

# Ensure wrapper dir exists
wrapper_dir.mkdir(parents=True, exist_ok=True)

# Copy project folder
if install_dir.exists():
    shutil.rmtree(install_dir)
shutil.copytree(source_dir, install_dir, ignore=shutil.ignore_patterns('.git'))

# Create wrapper
if is_windows:
    wrapper_path = wrapper_dir / f"{COMMAND_NAME}.bat"
    with open(wrapper_path, "w", encoding="utf-8") as f:
        f.write(f'@echo off\npython "{install_dir / SCRIPT_NAME}" %*\n')
elif is_linux:
    wrapper_path = wrapper_dir / COMMAND_NAME
    with open(wrapper_path, "w", encoding="utf-8") as f:
        f.write(f'#!/bin/bash\npython3 "{install_dir / SCRIPT_NAME}" "$@"\n')
    wrapper_path.chmod(0o755)

print(f"✅ Installed {SCRIPT_NAME} to {install_dir}")
print(f"✅ Wrapper created at {wrapper_path}")
print("ℹ️ Make sure the wrapper directory is in your PATH:")
print(f"   {wrapper_dir}")

if is_windows:
    print("   (Add it in System Properties → Environment Variables if not already there.)")
elif is_linux:
    print("   On most systems ~/.local/bin is already in PATH.")

# Pause if run from GUI so user can read output
if is_windows:
    input("Press Enter to exit...")
