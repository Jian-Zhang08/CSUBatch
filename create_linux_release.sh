#!/bin/bash

# Build the executable
echo "Building CSUbatch executable..."
./build_executable.sh

# Create release directory
echo "Creating release package..."
mkdir -p release

# Create the release package
cd dist
tar -czf ../release/CSUbatch-linux.tar.gz CSUbatch benchmark performance results
cd ..

# Create a simple installer script
cat > release/install.sh << 'EOF'
#!/bin/bash
echo "Installing CSUbatch..."
mkdir -p $HOME/CSUbatch
tar -xzf CSUbatch-linux.tar.gz -C $HOME/CSUbatch
chmod +x $HOME/CSUbatch/CSUbatch
chmod +x $HOME/CSUbatch/benchmark/batch_job.py

# Create a symbolic link in /usr/local/bin if possible
if [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
  echo "Creating symbolic link in /usr/local/bin..."
  ln -sf $HOME/CSUbatch/CSUbatch /usr/local/bin/csubatch
  echo "You can now run CSUbatch from anywhere by typing 'csubatch'"
else
  echo "To run CSUbatch, execute: $HOME/CSUbatch/CSUbatch"
fi

echo "Installation complete!"
EOF

chmod +x release/install.sh

# Add the install script to the archive
cd release
tar -czf CSUbatch-linux.tar.gz -C .. release/install.sh
mv CSUbatch-linux.tar.gz ..
cd ..
rm -rf release

echo "Release package created: CSUbatch-linux.tar.gz"
echo "This package contains the CSUbatch executable and all necessary files."
echo "Users can extract it and run CSUbatch directly or use the included install.sh script." 