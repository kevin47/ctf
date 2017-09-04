#!/bin/bash

docker cp ~/.vim $1:/root
docker cp ~/.vimrc $1:/root
docker cp ~/.bashrc $1:/root
docker cp ~/.gbd $1:/root
docker cp ~/.gbdinit $1:/root
docker cp ~/bin/.short.pwd.py $1:/root/bin/.short.pwd.py
