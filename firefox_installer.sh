##!/usr/bin/bash
# A bash script to install firefox and geckcodriver on ubuntu

#echo | sudo add-apt-repository ppa:mozillateam/ppa
#echo -ne '\n'
#sudo echo "Package: firefox*\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 501" > /etc/apt/preferences.d/mozillateamppa
#sudo apt update -y
#sudo apt install -y

# Install firefox driver and set the executable to PATH
#wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz -y
#tar -xvzf geckodriver-v0.30.0-linux64.tar.gz
#sudo mv geckodriver /usr/local/bin/
#sudo chmod +x /usr/local/bin/geckodriver

#pip install -r requirement.txt
#!/bin/bash
# A bash script to install firefox and geckodriver on ubuntu

# Add repository
#if [ -w "/etc/apt/preferences.d/mozillateamppa" ]; then
    #echo "Package: firefox*\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 501" > /etc/apt/preferences.d/mozillateamppa
#else
    #echo "Cannot write to /etc/apt/preferences.d/mozillateamppa. Moving to a writable directory."
    #tmpfile=$(mktemp)
    #echo "Package: firefox*\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 501" > "$tmpfile"
    #mv "$tmpfile" /etc/apt/preferences.d/mozillateamppa
#fi

firefox -v

# Update and install
apt-get update -y
apt-get install -y firefox
firefox -v

# Install geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
tar -xvzf geckodriver-v0.30.0-linux64.tar.gz
#mv geckodriver /usr/local/bin/
#chmod +x /usr/local/bin/geckodriver

# Install Python dependencies
pip install -r requirement.txt
