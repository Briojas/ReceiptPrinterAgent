#!/bin/bash
# Linux Development Environment Setup Script
# Compatible with: Debian, Ubuntu, WSL, and other Linux distributions

set -e  # Exit on error

echo "================================"
echo "Linux Development Environment Setup"
echo "Receipt Printer Agent"
echo "================================"

# Detect package manager
if command -v apt &> /dev/null; then
    PKG_MANAGER="apt"
    UPDATE_CMD="sudo apt update"
    INSTALL_CMD="sudo apt install -y"
elif command -v dnf &> /dev/null; then
    PKG_MANAGER="dnf"
    UPDATE_CMD="sudo dnf check-update || true"
    INSTALL_CMD="sudo dnf install -y"
elif command -v yum &> /dev/null; then
    PKG_MANAGER="yum"
    UPDATE_CMD="sudo yum check-update || true"
    INSTALL_CMD="sudo yum install -y"
elif command -v pacman &> /dev/null; then
    PKG_MANAGER="pacman"
    UPDATE_CMD="sudo pacman -Sy"
    INSTALL_CMD="sudo pacman -S --noconfirm"
else
    echo "❌ Unsupported package manager. Please install dependencies manually."
    exit 1
fi

echo "Detected package manager: $PKG_MANAGER"

# Update package lists
echo ""
echo "📦 Updating package lists..."
$UPDATE_CMD

# Install Python 3 and pip
echo ""
echo "🐍 Installing Python 3 and pip..."
if [ "$PKG_MANAGER" = "apt" ]; then
    $INSTALL_CMD python3 python3-pip python3-venv
elif [ "$PKG_MANAGER" = "dnf" ] || [ "$PKG_MANAGER" = "yum" ]; then
    $INSTALL_CMD python3 python3-pip python3-virtualenv
elif [ "$PKG_MANAGER" = "pacman" ]; then
    $INSTALL_CMD python python-pip python-virtualenv
fi

# Install build essentials (required for compiling Python packages)
echo ""
echo "🔧 Installing build tools..."
if [ "$PKG_MANAGER" = "apt" ]; then
    $INSTALL_CMD build-essential pkg-config libssl-dev curl
elif [ "$PKG_MANAGER" = "dnf" ] || [ "$PKG_MANAGER" = "yum" ]; then
    $INSTALL_CMD gcc gcc-c++ make pkgconfig openssl-devel curl
elif [ "$PKG_MANAGER" = "pacman" ]; then
    $INSTALL_CMD base-devel pkgconf openssl curl
fi

# Install Rust (required for libsql-experimental)
echo ""
echo "🦀 Installing Rust..."
if command -v rustc &> /dev/null; then
    echo "   Rust already installed: $(rustc --version)"
else
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
    echo "   Rust installed: $(rustc --version)"
fi

# Verify installations
echo ""
echo "✅ Verifying installations..."
python3 --version
pip3 --version
rustc --version
cargo --version

# Install Python dependencies
echo ""
echo "📚 Installing Python dependencies..."

# Check if running in WSL with Windows filesystem
if [[ "$PWD" == /mnt/* ]]; then
    echo "⚠️  Detected WSL with Windows filesystem mount"
    echo "   Installing packages globally (venv has permission issues on /mnt/)"
    echo ""
    pip3 install --upgrade pip --break-system-packages
    pip3 install -r requirements.txt --break-system-packages
else
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
fi

echo ""
echo "================================"
echo "✅ Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure environment variables:"
echo "   cp .env.example .env"
echo "   nano .env  # Add your API keys"
echo ""
echo "2. Run the application:"
echo "   python3 agent.py       # Gmail task extraction"
echo "   python3 main.py        # Task card generation"
echo "   python3 tools.py       # Arcade integrations"
echo "   python3 setup_database.py  # Database setup"
echo ""
if [[ "$PWD" != /mnt/* ]]; then
    echo "Note: Activate venv in future sessions with: source venv/bin/activate"
    echo ""
fi
