# Linux Screen OCR

Linux Screen OCR is a lightweight, open-source utility for extracting text from any visual element on your screen. Designed for speed and privacy, it captures screen regions directly into system memory, processes the image using the Tesseract OCR engine locally, and provides immediate access to the extracted text without saving temporary files to your hard drive.

## Project Background

This project was developed to solve a common workflow interruption in Linux environments: the inability to quickly copy text from protected documents, embedded videos, or system error dialogs. 

Existing solutions often require a multi-step process: taking a screenshot, saving it to disk, opening a secondary application, and manually extracting the text. This tool was built to condense that process into a single action. By leveraging PyQt5 for an invisible screen overlay and PyTesseract for text extraction, the application handles the entire pipeline in-memory. This ensures zero disk-write degradation, zero leftover clutter, and strict data privacy since no information is ever sent to a cloud API.

## Core Features

* **In-Memory Processing:** Bypasses disk storage entirely by handling screenshot image buffers directly in RAM.
* **Absolute Privacy:** 100% offline text extraction using your machine's local installation of Tesseract OCR.
* **Frictionless Interface:** A seamless, semi-transparent screen overlay allows for precise cursor selection.
* **Review and Export:** A minimalist dialog window allows users to review the extracted text, manually correct any OCR artifacts, copy it to the system clipboard, or export it as a `.txt` file.

## Installation

This application provides an automated installation script that safely handles system dependencies and configures a localized Python virtual environment, ensuring strict compliance with PEP 668 system package management standards.

Run the following command in your terminal to install the application:

```bash
bash <(curl -sL [https://raw.githubusercontent.com/lightning20222/linux-screen-ocr/refs/heads/main/install.sh])
```

**What this script does:**
1. Installs necessary system packages (`tesseract-ocr`, `python3-pyqt5`, `python3-venv`) via `apt`.
2. Creates an isolated application directory at `~/.local/share/linux_ocr`.
3. Downloads the latest Python source code directly from this repository.
4. Generates an isolated Python virtual environment to install the `pytesseract` and `Pillow` wrappers.
5. Creates a globally accessible executable at `~/.local/bin/linux-ocr`.

## Usage Instructions

Once installed, the application can be launched directly from the terminal by typing:

```bash
linux-ocr
```

### Recommended Workflow (Keyboard Shortcut)
For the intended user experience, map the executable to a custom keyboard shortcut in your Desktop Environment (e.g., GNOME, KDE, XFCE).

1. Open your system's **Keyboard Settings**.
2. Navigate to **Custom Shortcuts**.
3. Create a new shortcut named `Screen OCR`.
4. Set the command to `linux-ocr`.
5. Bind it to a key combination (e.g., `Ctrl + Shift + O`).

Now, simply press your assigned shortcut, click and drag to highlight the target text on your screen, and copy the output.

## System Requirements
* A Debian/Ubuntu-based Linux distribution (support for `apt` package manager).
* `sudo` privileges for the initial installation of Tesseract and PyQt5.

## Uninstallation

To completely remove the application and its isolated virtual environment from your system, you can run the provided uninstall script:

```bash
bash <(curl -sL [https://raw.githubusercontent.com/lightning20222/linux-screen-ocr/refs/heads/main/uninstall.sh])
```
*(Note: This safely removes the application files but leaves system-level packages like Tesseract installed, as other programs may depend on them).*
