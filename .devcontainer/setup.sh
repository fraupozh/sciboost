#!/bin/bash

# Output a message to indicate that the script has started
echo "Running setup.sh script..."

# Clone the skr_web_python_api repository
git clone https://github.com/lhncbc/skr_web_python_api.git

# Navigate to the skr_web_python_api directory
cd skr_web_python_api

# Build the wheel package
python3 -m build

# Install the generated wheel package into your virtual environment
python3 -m pip install dist/skr_web_api-0.1-py3-none-any.whl

# Get back to the root directory
cd ..

# Output a message to indicate that the setup is complete
echo "Setup complete."
