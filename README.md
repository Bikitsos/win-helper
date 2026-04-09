# Windows Helper

An administrative utility for system setup and workstation configuration, built with Python and PySide6.

## Overview

This tool provides a graphical user interface to run predefined Windows administration scripts (PowerShell and Batch). It is designed to be packaged into a single standalone executable, which enables easy deployment across multiple workstations.

## Available Actions

- **Install VC Redistributables**: Installs required Visual C++ dependencies.
- **Install Winget**: Installs the Windows Package Manager.
- **Set Cyprus Regional Settings**: Configures the system region for Cyprus.
- **Install NetBird**: Installs the NetBird VPN client.
- **Activate Windows**: Runs the activation script.
- **Set Power to Ultimate**: Enables the Ultimate Performance power plan and disables sleep/screen timeouts.
- **Set Windows Light Theme**: Forces the Windows Aero Light theme.
- **Set Time Zone (Athens)**: Sets the system time zone to GTB Standard Time.
- **Disable Windows Update**: Definitively disables the Windows Update service.

## Development setup

1. Ensure [uv](https://github.com/astral-sh/uv) is installed.
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Run the application from source:
   ```bash
   uv run main.py
   ```

## Packaging

The application can be compiled into a single standalone executable using PyInstaller.

```bash
uv run pyinstaller --noconfirm --noconsole --onefile --add-data "scripts;scripts" --name "win-helper" main.py
```

The resulting executable will be available at `dist/win-helper.exe`.