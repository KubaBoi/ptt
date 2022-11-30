# ProgTestTest

Script for testing ProgTest from CVUT FIT

## Run

`./ptt.py [args]`

`ptt [args]`

## INSTALATION

`wget https://github.com/KubaBoi/ptt/raw/master/ptt_latest.deb`

`sudo apt install ./ptt_latest.deb`

## DOC

`pandoc ptt.1.md -s -t man -o ptt.1`

`gzip ptt.1`

## Package

`dpkg-deb --build ptt.pack`

`mv ptt.pack.deb ptt-version_amd64.deb`

## Build

Not necessary

`sudo apt install nuitka`

`nuitka3 ptt.py`