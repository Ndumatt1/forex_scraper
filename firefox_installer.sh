#!/bin/bash
# A bash script to install Firefox and GeckoDriver on Ubuntu

# Add Mozilla PPA and set pin priority
echo | sudo add-apt-repository ppa:mozillateam/ppa
sudo sh -c 'echo "Package: firefox*\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 501" > /etc/apt/preferences.d/mozillateamppa'

# Update and install Firefox
sudo apt-get update -y
sudo apt-get install firefox -y

# Install GeckoDriver and set the executable to PATH
wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
tar -xvzf geckodriver-v0.30.0-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
sudo chmod +x /usr/local/bin/geckodriver

# Install Python dependencies
pip3 install -r requirement.txt
