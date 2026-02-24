#!/bin/bash

echo "Starting uninstallation of Linux Screen OCR..."

# Define the directories where the app was installed
INSTALL_DIR="$HOME/.local/share/linux_ocr"
BIN_FILE="$HOME/.local/bin/linux-ocr"

# Remove the isolated application folder and its virtual environment
if [ -d "$INSTALL_DIR" ]; then
    echo "Removing application directory: $INSTALL_DIR"
    rm -rf "$INSTALL_DIR"
fi

# Remove the executable command link
if [ -f "$BIN_FILE" ]; then
    echo "Removing executable command: $BIN_FILE"
    rm -f "$BIN_FILE"
fi

echo "Uninstallation Complete."
echo "The application and its virtual environment have been successfully removed."
echo "Note: Core system packages (tesseract-ocr, python3-pyqt5) were left intact to avoid breaking other applications."
