# CooPad — Remote Gamepad

CooPad is a cross-platform remote gamepad application that allows you to use a gamepad over the network. A client captures gamepad inputs and sends them to a host, which creates a virtual gamepad that games can use.

## ✅ Cross-Platform Support

CooPad works on both **Linux** and **Windows** as host and client:
- ✅ Linux Host + Linux Client
- ✅ Linux Host + Windows Client
- ✅ Windows Host + Linux Client  
- ✅ Windows Host + Windows Client

**📖 See [CROSS_PLATFORM_COMPATIBILITY.md](CROSS_PLATFORM_COMPATIBILITY.md) for detailed setup instructions, troubleshooting, and known issues.**

## Quick Start

### Test Your Platform

Run the compatibility checker to verify your setup:
```bash
python3 platform_test.py
```

### Installation

#### Linux
```bash
# Install system packages
sudo apt update
sudo apt install python3-tk python3-dev build-essential

# Install Python packages
pip install -r requirements.txt

# Setup uinput permissions (for host)
chmod +x scripts/setup_uinput.sh
./scripts/setup_uinput.sh
# Then log out and back in
```

#### Windows
```bash
# Install ViGEm Bus Driver (for host)
# Download from: https://github.com/ViGEm/ViGEmBus/releases

# Install Python packages
pip install -r requirements.txt
pip install vgamepad
```

### Run the Application

```bash
# Start the GUI
python3 main.py  # Linux
python main.py   # Windows
```

## Testing

```bash
# Platform compatibility check
python3 platform_test.py

# Full integration test (host + client)
python3 integration_test.py
```

## Documentation

- **[CROSS_PLATFORM_COMPATIBILITY.md](CROSS_PLATFORM_COMPATIBILITY.md)** - Complete cross-platform guide
  - Platform-specific requirements
  - Setup instructions for Linux and Windows
  - Known issues and troubleshooting
  - Performance expectations
  - Network configuration

## Features

- Remote gamepad over local network or VPN
- Full Xbox 360 gamepad emulation
- Low latency (1-10ms on local network)
- Cross-platform: Linux ↔ Windows
- No special drivers needed on client
- Supports physical gamepad input via pygame

## Requirements

### Common (Both Platforms)
- Python 3.8+
- Pillow
- pygame

### Linux Host
- evdev (virtual gamepad via uinput)
- uinput kernel module
- Permissions for /dev/uinput

### Windows Host
- vgamepad (virtual gamepad via ViGEm)
- ViGEm Bus Driver

### Client (Both Platforms)
- pygame (for joystick input)
- Network access to host

## License

See LICENSE file for details.