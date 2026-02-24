#!/bin/bash

echo "Starting Linux Screen OCR Installation..."

# Ask for the administrator password upfront. 
# If they fail or press Esc, print an error and exit immediately.
echo "Administrator privileges are required to install system packages."
sudo -v || { echo "Error: Sudo authentication failed or was canceled. Exiting installation."; exit 1; }

# 1. Install system dependencies
# The '|| exit 1' ensures that if apt fails for any reason, the script stops.
echo "Installing system dependencies (Tesseract and PyQt5)..."
sudo apt-get update || { echo "Error: Failed to update package list. Exiting."; exit 1; }
sudo apt-get install -y tesseract-ocr python3-pyqt5 python3-venv || { echo "Error: Failed to install system packages. Exiting."; exit 1; }

# 2. Define installation directories (safely in the user's home folder)
INSTALL_DIR="$HOME/.local/share/linux_ocr"
BIN_DIR="$HOME/.local/bin"

echo "Creating installation directories..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# 3. Download the Python script directly from your GitHub
echo "Downloading application files..."
curl -sL -o "$INSTALL_DIR/linux_ocr.py" https://raw.githubusercontent.com/lightning20222/linux-screen-ocr/refs/heads/main/linux_ocr.py

# 4. Set up the virtual environment so it doesn't break PEP 668 system packages
echo "Setting up Python virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"
"$INSTALL_DIR/venv/bin/pip" install pytesseract Pillow --quiet

# 5. Create a global command so the user can just type 'linux-ocr'
echo "Creating executable command..."
cat << EOF > "$BIN_DIR/linux-ocr"
#!/bin/bash
$INSTALL_DIR/venv/bin/python $INSTALL_DIR/linux_ocr.py
EOF

chmod +x "$BIN_DIR/linux-ocr"

echo "Installation Complete."
echo "You can now run the app anytime by typing 'linux-ocr' in your terminal,"
echo "or by mapping 'linux-ocr' to a custom keyboard shortcut."
