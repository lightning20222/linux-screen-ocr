#!/bin/bash

echo "Starting Linux Screen OCR Installation..."

echo "Administrator privileges are required to install system packages."
sudo -v || { echo "Error: Sudo authentication failed or canceled."; exit 1; }

echo "Installing system dependencies..."
sudo apt-get update || { echo "Error updating packages."; exit 1; }
sudo apt-get install -y tesseract-ocr python3-venv curl || { echo "Error installing packages."; exit 1; }

INSTALL_DIR="$HOME/.local/share/linux_ocr"
BIN_DIR="$HOME/.local/bin"

echo "Creating installation directories..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

echo "Downloading application files..."
curl -sL -o "$INSTALL_DIR/linux_ocr.py" \
https://raw.githubusercontent.com/lightning20222/linux-screen-ocr/main/linux_ocr.py

if [ ! -f "$INSTALL_DIR/linux_ocr.py" ]; then
    echo "Error: Failed to download application."
    exit 1
fi

echo "Setting up Python virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"

echo "Upgrading pip..."
"$INSTALL_DIR/venv/bin/python" -m pip install --upgrade pip --quiet

echo "Installing Python dependencies..."
"$INSTALL_DIR/venv/bin/pip" install pytesseract Pillow PyQt5 --quiet

echo "Creating executable command..."

cat << EOF > "$BIN_DIR/linux-ocr"
#!/bin/bash
"$INSTALL_DIR/venv/bin/python" "$INSTALL_DIR/linux_ocr.py"
EOF

chmod +x "$BIN_DIR/linux-ocr"

echo "Ensuring ~/.local/bin is in PATH..."

if ! grep -q '.local/bin' "$HOME/.bashrc"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

echo ""
echo "✅ Installation Complete."
echo ""
echo "Run the app using:"
echo "linux-ocr"
echo ""
echo "If command not found, restart terminal or run:"
echo "source ~/.bashrc"
echo ""
echo "or by mapping 'linux-ocr' to a custom keyboard shortcut."
