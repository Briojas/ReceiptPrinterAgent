# Receipt Printer Task Manager

A Python-based task management system that prints tasks to a thermal receipt printer and integrates with various services.

## Features

- Print tasks to thermal receipt printers
- Extract tasks from Gmail automatically
- AI-powered task parsing and prioritization
- Duplicate detection using vector embeddings
- Integration with multiple services (Gmail, Slack, Calendar, Notion) via Arcade.dev

## Installation

**⚠️ Linux Required:** This project requires a Linux environment due to native dependencies (`libsql-experimental`). Windows users should use WSL.

### Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/CodingWithLewis/ReceiptPrinterAgent
cd ReceiptPrinterAgent

# Run setup script (works on Debian, Ubuntu, Fedora, Arch, WSL)
chmod +x setup_linux.sh
./setup_linux.sh

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Manual Setup

```bash
# Install Python 3, pip, and build tools
# For Debian/Ubuntu:
sudo apt install python3 python3-pip python3-venv build-essential pkg-config libssl-dev

# Install Rust (required for libsql-experimental)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Windows Users

Use **WSL (Windows Subsystem for Linux)** for full compatibility:

```powershell
# Install WSL
wsl --install

# Open WSL terminal, navigate to project
cd /mnt/c/projects/ReceiptPrinterAgent

# Run the setup script
chmod +x setup_linux.sh
./setup_linux.sh
```

## Configuration

Required environment variables:
- `ARCADE_API_KEY` - Get from [arcade.dev](https://arcade.dev)
- `OPENAI_API_KEY` - OpenAI API key
- `TURSO_DATABASE_URL` - Database URL (optional, uses local SQLite by default)
- `TURSO_AUTH_TOKEN` - Database auth token (if using Turso)

## Usage

### Extract tasks from Gmail
```bash
python agent.py
```

### Create a task from text
```bash
python main.py
```

### Use Arcade tools
```bash
python tools.py
```

### Setup database
```bash
python setup_database.py
```

## Requirements

- Python 3.8+
- Thermal receipt printer (USB)
- API keys for OpenAI and Arcade.dev

## License

MIT License - see LICENSE file for details.