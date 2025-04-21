#!/bin/bash

echo "Installing CSUbatch..."

# Create installation directory
INSTALL_DIR="$HOME/CSUbatch"
mkdir -p "$INSTALL_DIR"

# Check if we're running from the extracted directory or alongside the tar.gz
if [ -f "CSUbatch" ]; then
    # We're in the extracted directory
    cp -r * "$INSTALL_DIR"
elif [ -f "CSUbatch-linux.tar.gz" ]; then
    # We're in the directory with the tar.gz
    tar -xzf CSUbatch-linux.tar.gz -C "$INSTALL_DIR"
else
    echo "Error: Could not find CSUbatch files."
    exit 1
fi

# Make files executable
chmod +x "$INSTALL_DIR/CSUbatch"
chmod +x "$INSTALL_DIR/benchmark/batch_job.py"

# Create symbolic link if possible
if [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
    echo "Creating symbolic link in /usr/local/bin..."
    ln -sf "$INSTALL_DIR/CSUbatch" /usr/local/bin/csubatch
    echo "CSUbatch installed successfully! You can run it by typing 'csubatch' from anywhere."
else
    echo "CSUbatch installed successfully in $INSTALL_DIR"
    echo "To run it, execute: $INSTALL_DIR/CSUbatch"
    
    # Add to user's PATH in .bashrc if possible
    if [ -f "$HOME/.bashrc" ] && [ -w "$HOME/.bashrc" ]; then
        echo "Would you like to add CSUbatch to your PATH? (y/n)"
        read answer
        if [ "$answer" == "y" ] || [ "$answer" == "Y" ]; then
            echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> "$HOME/.bashrc"
            echo "Added CSUbatch to your PATH. Please restart your terminal or run 'source ~/.bashrc'"
        fi
    fi
fi

echo "Installation complete!" 