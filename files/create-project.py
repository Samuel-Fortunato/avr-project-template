#!/usr/bin/env python3
import os
import shutil
import sys
import re
from pathlib import Path

# --- CONFIG ---
TEMPLATE_DIR = Path(__file__).parent / "template"

# --- GET USER INPUT WITH VALIDATION ---
while True:
    project_name = input("Project name: ").strip()
    if project_name and re.match(r'^[A-Za-z0-9_-]+$', project_name):
        break
    print("Error: Project name can only contain alphanumeric characters, hyphens and underscores.")

while True:
    avr_mcu = input("MCU name (e.g., atmega328): ").strip().lower()
    if avr_mcu.startswith("at") and len(avr_mcu) > 2 and avr_mcu.isalnum():
        break
    print("Error: MCU name must be alphanumeric and start with \"at\"")

while True:
    ext_osc = input("External clock [true/false]: ").strip().lower()
    if ext_osc in ["true", "false"]:
        break
    print("Error: Please enter 'true' or 'false'.")

while True:
    clock_speed = input("Clock speed in Hz (e.g., 16000000): ").strip()
    if clock_speed.isdigit() and int(clock_speed) > 0:
        break
    print("Error: Please enter a positive integer value for clock speed.")

# --- COMPUTE DERIVED VALUES ---
simulide_mcu = avr_mcu[2:]
clock_speed_mhz = str(int(clock_speed) // 1_000_000)

# --- CREATE PROJECT DIR ---
if os.path.exists(project_name):
    print(f"Error: Directory '{project_name}' already exists.")
    sys.exit(1)

shutil.copytree(TEMPLATE_DIR, project_name)

# --- REPLACE PLACEHOLDERS ---
for root, _, files in os.walk(project_name):
    for file in files:
        path = os.path.join(root, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("{{PROJECT_NAME}}", project_name)
        content = content.replace("{{MCU}}", avr_mcu)
        content = content.replace("{{SIMULIDE_MCU}}", simulide_mcu)
        content = content.replace("{{CLOCK_SPEED}}", clock_speed)
        content = content.replace("{{CLOCK_SPEED_MHZ}}", clock_speed_mhz)
        content = content.replace("{{EXT_OSC}}", ext_osc)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

# --- RENAME SIM1 FILE ---
old_sim1 = os.path.join(project_name, "circuit.sim1")
new_sim1 = os.path.join(project_name, f"{project_name}.sim1")
os.rename(old_sim1, new_sim1)

# --- USAGE INSTRUCTIONS ---
print(f"\nProject '{project_name}' created successfully.\n")

print(f"""To configure with CMake CLI:
\t$ cd {project_name}
\t$ mkdir build
\t$ cd build
\t$ cmake .. -DCMAKE_TOOLCHAIN_FILE=../avr-toolchain.cmake\n""")

print(f"""To configure with CMake GUI:
\tOpen CMake GUI, set source to '{project_name}', build to '{project_name}/build',
\tand specify the toolchain file '../avr-toolchain.cmake' in the advanced options.\n""")
