#!/bin/bash

# Install Python and pip if not installed
echo "Checking for Python installation..."
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Installing Python..."
    sudo apt update && sudo apt install python3 python3-pip -y
else
    echo "Python is already installed."
fi

# Install required Python modules
echo "Installing required Python modules..."

# List of Python modules to install
modules=(
    "requests"
    "selenium"
    "beautifulsoup4"
    "lxml"
    "pycryptodome"
    "fake_useragent"
    "pyfiglet"
    "sklearn"
    "numpy"
    "scikit-learn"
    "tensorflow"
    "keras"
    "tensorflow-gpu"
)

for module in "${modules[@]}"; do
    pip3 install "$module" || {
        echo "Failed to install $module. Please check the error messages.";
        exit 1;
    }
done

# Install additional dependencies for system utilities (e.g., curl, wget, etc.)
echo "Installing additional system dependencies..."
sudo apt install curl wget git -y

# Clone any repositories if needed
# Example:
# git clone 

echo "Installation complete!"
