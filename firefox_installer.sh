#!/usr/bin/bash
# A bash script to install firefox and geckcodriver on ubuntu

echo | sudo add-apt-repository ppa:mozillateam/ppa
#echo -ne '\n'
sudo echo "Package: firefox*\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 501" > /etc/apt/preferences.d/mozillateamppa
sudo apt update -y
sudo apt install -y

# Install firefox driver and set the executable to PATH
wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz -y
tar -xvzf geckodriver-v0.30.0-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
sudo chmod +x /usr/local/bin/geckodriver