# ProgTestTest

Script for testing ProgTest from CVUT FIT

## Build

Not necessary

`sudo apt install nutika3`

`nuitka3 ptt.py`

## Run

`./ptt.py [args]`

`ptt [args]`

## INSTALATION

Download `ptt.py` from https://github.com/KubaBoi/ptt/blob/master/ptt.py (or just copy content and make file with that content inside named `ptt.py`)

Run:

`sudo chmod +x ptt.py`

`sudo ./ptt.py -i`

Script will be installed inside your `/usr/bin` directory and also will be made manual page in `/usr/share/man/man1` directory.

Make sure you are connected to internet. Otherwise latest version will not be downloaded and `man ptt` will not be functional or if you are updating `ptt` there may be old version of manual.

## DOC

`pandoc ptt.1.md -s -t man -o ptt.1`

`gzip ptt.1`

