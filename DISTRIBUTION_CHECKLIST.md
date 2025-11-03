# PC Utilities Manager - Distribution Checklist

Use this checklist when preparing to distribute PC Utilities Manager to ensure LGPL compliance and quality.

## Pre-Distribution Tasks

### License & Compliance (CRITICAL)
- [ ] ✅ LICENSE.txt file exists and is accessible
- [ ] ✅ LICENSES/ folder contains all required license files
- [ ] ✅ PYSIDE6-LGPLV3.txt is included
- [ ] ✅ THIRD-PARTY-LICENSES.txt is included
- [ ] ✅ DISTRIBUTION_COMPLIANCE.md is included in package
- [ ] ✅ About dialog mentions PySide6 and LGPL (DONE)
- [ ] ✅ README.md has license section (DONE)
- [ ] ✅ setup.py has proper metadata (DONE)

### Documentation
- [ ] README.md is current and accurate
- [ ] requirements.txt lists all dependencies
- [ ] Installation instructions are clear
- [ ] Troubleshooting section is complete
- [ ] Version number is correct

### Code Quality
- [ ] No hardcoded paths (except user home directory)
- [ ] No debug print statements or debug code
- [ ] Error handling is proper
- [ ] Comments are clear and helpful
- [ ] Code follows Python conventions (PEP 8)

### Testing
- [ ] Application starts without errors
- [ ] All buttons work correctly
- [ ] Office converter works (if Office installed)
- [ ] Image to PDF converter works
- [ ] About dialog displays correctly
- [ ] No console errors on exit

### Dependencies
- [ ] PySide6 is listed in requirements.txt
- [ ] pywin32 is listed in requirements.txt
- [ ] Pillow is listed in requirements.txt
- [ ] Python version requirement is specified (>=3.8)
- [ ] No missing optional dependencies

## Packaging for Free Distribution

### Source Code Distribution
Use this for simplest distribution:

- [ ] download_manager.py
- [ ] setup.py
- [ ] requirements.txt
- [ ] README.md
- [ ] LICENSE.txt
- [ ] LICENSES/ (entire folder)
- [ ] DISTRIBUTION_COMPLIANCE.md
- [ ] DISTRIBUTION_CHECKLIST.md
- [ ] run.bat (launcher script)
- [ ] auto_setup.bat (installer script)
- [ ] install.bat (if separate)

**File naming:** `pc_utilities_v1.0_source.zip`

### PyInstaller Distribution

#### Step 1: Create Executable
```bash
pip install pyinstaller
pyinstaller --onedir --windowed --add-data "LICENSE.txt:." download_manager.py
```

#### Step 2: Verify Files
- [ ] dist/download_manager/ folder created
- [ ] dist/download_manager/download_manager.exe exists
- [ ] dist/download_manager/PySide6/ folder with DLLs exists
- [ ] dist/download_manager/_internal/ folder exists

#### Step 3: Add License Files
```bash
cd dist/download_manager
copy ..\..\LICENSE.txt .
xcopy ..\..\LICENSES .\LICENSES /E /I
copy ..\..\README.md .
```

#### Step 4: Create Distribution Package
- [ ] Create folder: `PC_Utilities_v1.0_Windows`
- [ ] Copy: `dist/download_manager/` contents to it
- [ ] Copy: LICENSE.txt to root
- [ ] Copy: LICENSES/ folder to root
- [ ] Copy: README.md to root
- [ ] Copy: DISTRIBUTION_COMPLIANCE.md to root
- [ ] Create README_FIRST.txt with quick start
- [ ] Zip entire folder

**File naming:** `pc_utilities_v1.0_windows.zip`

## Packaging for Commercial Distribution

### Installer Creation (NSIS Example)
- [ ] Use Windows installer tool (NSIS, Advanced Installer, etc.)
- [ ] Include all application files
- [ ] Include all license files
- [ ] Set default installation path to Program Files
- [ ] Create Start Menu shortcuts
- [ ] Create uninstaller

### Installer Package Contents
- [ ] Application executable
- [ ] All required DLLs (PySide6, pywin32, Pillow)
- [ ] LICENSE.txt file
- [ ] LICENSES/ folder
- [ ] README.md or help file
- [ ] Optional: changelog or version history

### Code Signing (Recommended)
- [ ] Purchase or obtain code signing certificate
- [ ] Sign the executable to avoid Windows SmartScreen warnings
- [ ] Sign the installer executable

**File naming:** `PC_Utilities_Setup_v1.0.exe`

## Distribution Channel Checklist

### GitHub/GitLab Release
- [ ] Commit all changes
- [ ] Tag release (v1.0.0)
- [ ] Create release notes
- [ ] Attach built executable/zip
- [ ] Include all license files in repo
- [ ] Repository README mentions LGPL

### Website Download
- [ ] Download page has version number
- [ ] License terms are visible on page
- [ ] File integrity (checksums) available
- [ ] System requirements listed
- [ ] Support contact provided
- [ ] Download mirrors tested

### PyPI Package (Optional)
- [ ] Ensure setup.py is complete
- [ ] Test with: `python setup.py sdist bdist_wheel`
- [ ] Upload to PyPI: `twine upload dist/*`
- [ ] Verify listing on pypi.org

## Final Verification Before Release

### Compliance Check
- [ ] LGPL license text present and accurate
- [ ] Attribution to PySide6 visible in app
- [ ] No modifications to PySide6 in distribution
- [ ] Source code or build provided

### Functionality Check
- [ ] Application launches without errors
- [ ] All features work as expected
- [ ] Error messages are helpful
- [ ] Exit is clean (no hanging processes)

### Package Check
- [ ] All files are included
- [ ] No unnecessary files included
- [ ] File permissions are correct
- [ ] ZIP/installer can be extracted properly
- [ ] File sizes are reasonable

### Documentation Check
- [ ] README is clear and complete
- [ ] Installation instructions work
- [ ] License information is easy to find
- [ ] Support/contact information provided

## Post-Distribution

### After Release
- [ ] Monitor for error reports
- [ ] Respond to user feedback
- [ ] Track download/installation metrics
- [ ] Plan next version improvements

### Version Updates
- [ ] Update version number in code
- [ ] Update version number in setup.py
- [ ] Update README with changes
- [ ] Create new release package
- [ ] Test thoroughly before distribution

## Distribution Scenarios

### For Free USB Distribution
Required files:
```
✓ download_manager.py
✓ requirements.txt
✓ auto_setup.bat
✓ run.bat
✓ README.md
✓ LICENSE.txt
✓ LICENSES/folder
```

**Checklist:**
- [ ] All above files present
- [ ] Files organized cleanly
- [ ] USB formatted properly
- [ ] Test on clean Windows machine

### For Commercial Product
Required files:
```
✓ Application executable (signed)
✓ Installer program
✓ All DLLs (separate)
✓ LICENSE.txt
✓ LICENSES/ folder
✓ README/Help documentation
```

**Checklist:**
- [ ] Installer tested
- [ ] Executable signed
- [ ] Legal review done
- [ ] EULA appropriate
- [ ] Support contact clear

## Signing Off

Before distribution, verify:

- [ ] **Legal**: LGPL terms understood and followed
- [ ] **Technical**: All features tested and working
- [ ] **Quality**: Code is clean and documented
- [ ] **Complete**: All required files included
- [ ] **Compliant**: All licenses included and attributed

## Approved for Distribution

Once all checkboxes are complete:

**Application:** PC Utilities Manager
**Version:** 1.0
**Date Approved:** _______________
**Distributor:** _______________
**Release Type:** ☐ Free  ☐ Commercial  ☐ Freeware

---

**Note:** This checklist ensures legal compliance with LGPL v3.0 and quality standards.
Always refer to DISTRIBUTION_COMPLIANCE.md for detailed guidance.

**Last Updated:** 2025-11-03
