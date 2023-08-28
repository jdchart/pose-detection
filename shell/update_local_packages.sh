#!/bin/bash

# Install adaw once you have made changes to the package.
# Don't forget to give this script permission by running: 
# chmod a+x shell/update_local_packages.sh

echo "Installing local packages..."
pip install posedetector/
pip install posesonifier/
pip install motracker/
echo "Everything is up to date!"