#!/usr/bin/env bash
set -euo pipefail

# Build a single-file PyInstaller binary and package it into an AppImage
# Usage: ./scripts/build_appimage.sh [version]

VERSION=${1:-1.0.0}
APPNAME=CooPad
PKGNAME=coopad
BUILD_DIR=$(pwd)
DIST_DIR=${BUILD_DIR}/dist
APPDIR=${BUILD_DIR}/AppDir
RELEASES_DIR=${BUILD_DIR}/scripts/releases

echo "═══════════════════════════════════════════════════════"
echo "Building ${APPNAME} version ${VERSION} for Linux (AppImage)"
echo "═══════════════════════════════════════════════════════"
echo ""

# Ensure we're in project root
if [ ! -f "main.py" ]; then
  echo "Error: main.py not found. Please run from project root."
  exit 1
fi

# Ensure venv activated or use system python
if [ -z "${VIRTUAL_ENV:-}" ]; then
  echo "Warning: virtualenv not active. Using system Python."
fi

echo "Installing build dependencies and runtime dependencies..."
pip3 install --upgrade --quiet pyinstaller Pillow pygame-ce evdev 2>/dev/null || \
pip install --upgrade --quiet pyinstaller Pillow pygame-ce evdev

echo "Running PyInstaller with spec file..."
pyinstaller --noconfirm scripts/coopad.spec

echo "Preparing AppDir structure..."
rm -rf ${APPDIR}
mkdir -p ${APPDIR}/usr/bin
mkdir -p ${APPDIR}/usr/share/applications
mkdir -p ${APPDIR}/usr/share/icons/hicolor/256x256/apps
mkdir -p ${APPDIR}/usr/share/doc/${PKGNAME}

echo "Copying binary, icon, and docs..."
if [ -f "${DIST_DIR}/${PKGNAME}" ]; then
  cp ${DIST_DIR}/${PKGNAME} ${APPDIR}/usr/bin/${PKGNAME}
  chmod 0755 ${APPDIR}/usr/bin/${PKGNAME}
else
  echo "Error: Binary ${DIST_DIR}/${PKGNAME} not found!"
  exit 1
fi

# Copy icon if exists
if [ -f "img/src_CooPad.png" ]; then
  cp img/src_CooPad.png ${APPDIR}/usr/share/icons/hicolor/256x256/apps/${PKGNAME}.png
  cp img/src_CooPad.png ${APPDIR}/${PKGNAME}.png
  chmod 0644 ${APPDIR}/usr/share/icons/hicolor/256x256/apps/${PKGNAME}.png
  chmod 0644 ${APPDIR}/${PKGNAME}.png
fi

# Copy README if exists
if [ -f "README.md" ]; then
  cp README.md ${APPDIR}/usr/share/doc/${PKGNAME}/README.md
  chmod 0644 ${APPDIR}/usr/share/doc/${PKGNAME}/README.md
fi

# Create desktop entry
cat > ${APPDIR}/usr/share/applications/${PKGNAME}.desktop <<'DESKTOP'
[Desktop Entry]
Version=1.0
Type=Application
Name=CooPad
Comment=Remote Gamepad over Network
Exec=coopad
Icon=coopad
Terminal=false
Categories=Game;Utility;Network;
DESKTOP

# Create AppDir desktop file (required for AppImage)
cp ${APPDIR}/usr/share/applications/${PKGNAME}.desktop ${APPDIR}/${PKGNAME}.desktop

# Create AppRun script
cat > ${APPDIR}/AppRun <<'APPRUN'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"

# Load uinput module if not already loaded (requires sudo, so it may fail)
if ! lsmod | grep -q uinput 2>/dev/null; then
    modprobe uinput 2>/dev/null || true
fi

exec "${HERE}/usr/bin/coopad" "$@"
APPRUN

chmod 0755 ${APPDIR}/AppRun

# Download appimagetool if not present
APPIMAGETOOL="${BUILD_DIR}/appimagetool-x86_64.AppImage"
if [ ! -f "${APPIMAGETOOL}" ]; then
  echo "Downloading appimagetool..."
  wget -q -O "${APPIMAGETOOL}" "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
  chmod +x "${APPIMAGETOOL}"
fi

echo "Building AppImage..."
APPIMAGE="${DIST_DIR}/${APPNAME}-${VERSION}-x86_64.AppImage"
ARCH=x86_64 "${APPIMAGETOOL}" ${APPDIR} ${APPIMAGE}

# Create releases directory and copy the AppImage
echo "Creating releases directory..."
mkdir -p ${RELEASES_DIR}
cp ${APPIMAGE} ${RELEASES_DIR}/

echo ""
echo "═══════════════════════════════════════════════════════"
echo "✓ AppImage created successfully!"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "AppImage: ${APPIMAGE}"
echo "Release:  ${RELEASES_DIR}/$(basename ${APPIMAGE})"
echo ""
echo "To run:"
echo "  chmod +x ${APPIMAGE}"
echo "  ${APPIMAGE}"
echo ""
echo "Or copy to your PATH:"
echo "  sudo cp ${APPIMAGE} /usr/local/bin/${PKGNAME}"
echo ""
echo "Note: For Host mode (virtual gamepad), you may need to:"
echo "  1. Load uinput module: sudo modprobe uinput"
echo "  2. Add user to input group: sudo usermod -aG input \$USER"
echo "  3. Log out and back in for changes to take effect"
echo ""

exit 0
