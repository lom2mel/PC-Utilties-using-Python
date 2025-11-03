# PC Utilities Manager - Distribution Compliance Guide

## Overview

This document explains how to safely package and distribute PC Utilities Manager while remaining compliant with the GNU Lesser General Public License v3.0 (LGPL v3.0) requirements from PySide6.

## Quick Answer: CAN YOU DISTRIBUTE?

**YES** - You can distribute PC Utilities Manager as:
- ✅ Free software
- ✅ Commercial/paid software
- ✅ Freeware
- ✅ Shareware
- ✅ As part of a larger application

**WITHOUT:**
- ❌ Making your code open source
- ❌ Sharing your proprietary code
- ❌ Paying licensing fees

## What You Must Do

### 1. Include License Files

Always include these files with your distribution:
```
your_distribution/
├── LICENSE.txt                          (Main compliance file)
├── LICENSES/
│   ├── PYSIDE6-LGPLV3.txt              (PySide6 LGPL v3.0 license)
│   └── THIRD-PARTY-LICENSES.txt        (All dependencies)
├── download_manager.py
├── requirements.txt
└── README.md
```

### 2. Provide Attribution

Include clear attribution to PySide6 in:
- **About dialog** - ✓ Already updated in your app
- **README.md** - ✓ Already updated
- **Setup/Installation instructions** - Include mention of PySide6

### 3. Allow Library Replacement

When distributing with PyInstaller or cx_Freeze:
- Include PySide6 DLLs as separate files (don't use `--onefile` exclusively)
- Document that users may replace PySide6 libraries with compatible versions
- Example note: "Advanced users may replace PySide6 with compatible versions from https://code.qt.io/cgit/pyside/pyside-setup.git/"

### 4. Document Dependencies

Your `requirements.txt` should list all dependencies:
```
PySide6>=6.5.0
pywin32>=305
Pillow>=9.0.0
```

## Packaging Options

### Option 1: Distribute Source Code (Simplest)

Just distribute the source files + requirements.txt:
- Users install Python and dependencies themselves
- Completely compliant with LGPL
- Easiest to maintain

**Files to include:**
- `download_manager.py`
- `requirements.txt`
- `setup.py`
- `README.md`
- `LICENSE.txt`
- `LICENSES/` folder
- `run.bat` or equivalent launcher
- `auto_setup.bat` (your existing installer script)

### Option 2: PyInstaller Standalone Executable

Create a Windows executable using PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onedir --windowed --add-data "LICENSE.txt:." download_manager.py
```

**Important for LGPL compliance:**
- Use `--onedir` (not `--onefile`) so PySide6 DLLs remain separate
- Include LICENSE.txt and LICENSES/ folder in the distribution
- Create an installer that includes these files

**Files to include in distribution:**
```
PC_Utilities_Installer/
├── dist/
│   └── download_manager/
│       ├── download_manager.exe
│       ├── PySide6/          (DLLs - separate files)
│       ├── LICENSE.txt
│       └── LICENSES/
├── LICENSE.txt
├── LICENSES/
├── README.md
└── install_instructions.txt
```

### Option 3: Windows Installer (.MSI or .EXE)

Use tools like NSIS or Advanced Installer:

```
Installer should include:
- Application executable
- All required DLLs (PySide6, etc.)
- LICENSE.txt file
- LICENSES/ folder
- README.md
- Any batch files (run.bat, etc.)
```

## What NOT To Do

❌ **Don't:**
- Statically compile PySide6 into your executable using `--onefile`
- Remove license files from distribution
- Claim PySide6 is your own work
- Modify PySide6 source code without sharing modifications
- Hide or obscure the LGPL license requirement

## Example Distribution Scenarios

### Scenario 1: Free USB Distribution
```
pc_utilities_usb/
├── download_manager.py
├── requirements.txt
├── auto_setup.bat
├── run.bat
├── README.md
├── LICENSE.txt          ← LGPL attribution
├── DISTRIBUTION_COMPLIANCE.md
└── LICENSES/
    ├── PYSIDE6-LGPLV3.txt
    └── THIRD-PARTY-LICENSES.txt
```
✅ **Fully compliant** - Users understand LGPL, can replace libraries

### Scenario 2: Commercial Paid Software
```
PC_Utilities_Professional_Installer.exe
- Installs all files including licenses
- About dialog shows PySide6 attribution
- Installer includes LICENSE.txt
- Help menu links to: https://code.qt.io/cgit/pyside/pyside-setup.git/
```
✅ **Fully compliant** - LGPL allows commercial use

### Scenario 3: Website Download (Standalone)
```
pc_utilities_v1.0.zip
├── dist/
│   └── download_manager/ (PyInstaller output)
│       ├── download_manager.exe
│       ├── PySide6/ (DLL files)
│       └── LICENSE.txt
├── LICENSE.txt
├── LICENSES/
├── README.md
└── INSTALL_INSTRUCTIONS.txt
```
✅ **Fully compliant** - Separate DLLs, licenses included

## Frequently Asked Questions

### Q: Can I sell this application?
**A:** Yes! LGPL allows commercial distribution. Just include the license files.

### Q: Do I need to pay anything?
**A:** No. PySide6 and all dependencies are free. No licensing fees required.

### Q: Must I open-source my code?
**A:** No! LGPL only requires the PySide6 library to remain modifiable, not your application.

### Q: Can I modify PySide6?
**A:** You can, but if you distribute modified PySide6, you must share the modifications.

### Q: What if I don't include license files?
**A:** It violates LGPL terms. Always include them. It's a legal requirement.

### Q: Can users replace PySide6?
**A:** Yes, and they have the legal right to do so. This is an LGPL requirement.

### Q: What about static linking?
**A:** Avoid static compilation of PySide6. Python uses dynamic imports, which is fine.

### Q: Can I use --onefile with PyInstaller?
**A:** Technically yes, but document that PySide6 can be replaced by extracting the exe.

## Testing Your Compliance

Checklist before distribution:

- [ ] LICENSE.txt is in the root directory
- [ ] LICENSES/ folder contains PySide6-LGPLV3.txt
- [ ] LICENSES/ folder contains THIRD-PARTY-LICENSES.txt
- [ ] README.md mentions PySide6 and LGPL
- [ ] About dialog shows PySide6 attribution (✓ Done)
- [ ] setup.py includes proper metadata (✓ Done)
- [ ] PySide6 DLLs are separate files (if using PyInstaller)
- [ ] requirements.txt lists all dependencies
- [ ] No modifications made to PySide6 source
- [ ] Installation instructions are clear

## Resources

- **PySide6 Official**: https://wiki.qt.io/Qt_for_Python
- **PySide6 Repository**: https://code.qt.io/cgit/pyside/pyside-setup.git/
- **LGPL v3.0 License**: https://www.gnu.org/licenses/lgpl-3.0.html
- **LGPL Compliance Guide**: https://www.gnu.org/licenses/lgpl-3.0.en.html

## Summary

Your PC Utilities Manager is **fully compliant** with LGPL v3.0 for:
- ✅ Free distribution
- ✅ Commercial sales
- ✅ Proprietary code (your code remains yours)
- ✅ Modifications (just attribute and follow LGPL terms)

The compliance files are already in place. Just ensure they're included whenever you distribute the application!

---

**Last Updated:** 2025-11-03
**Application:** PC Utilities Manager v1.0
**License:** Your proprietary license (application) + LGPL v3.0 (PySide6)
