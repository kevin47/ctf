#!/bin/bash

apt-get update
apt-get -y install vim nmap gcc tmux htop gdb make python ipython python-setuptools python-dev build-essential python-pip libffi libffi-dev libssl-dev libsodium-dev curl wget
pip install -U pip
pip install pwntools
