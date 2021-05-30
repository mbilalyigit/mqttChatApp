#!/bin/sh
osName=$(sudo cat /etc/os-release | grep '^NAME=')

echo "Installing Required Packages"
ubuntu="NAME=\"Ubuntu\""

if [ "$osName" = "$ubuntu" ]; then
    echo "Your OS$osName"
    echo "Choosing APT package manager"
    sudo apt install python3 python3-dev python3-pip python3-tk
else
    echo "No OS recognized! Continue with PIP Package Installations? [ Y/n ]"
    read input
    if [ "$input" = "n" ]; then
        exit 1
    fi
fi

echo "Installing Python Packages with PIP..."

pip3 install --upgrade setuptools pip

pip3 install -r requirements.txt

echo "Installation finished!"