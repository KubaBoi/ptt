---
title: ProgTestTest
section: 1
header: User Manual
footer: ptt 0.5.0
date: November 14, 2022
---

# ProgTestTest
ptt - Test tool for ProgTest from CVUT FIT

# SYNOPSIS
**ptt** [-h] [-i] [-u] [-d DATA_PATH] [-v] [-V VAL_ARGS] [-D VAL_DATA] [-c COMPILER] [-C COMPILER_ARGS] [-s] [-n] filename

# DESCRIPTION
**ptt** is simple script for testing your ProgTest. Via oneline shell command you can compile C/C++ script and run them as single instance with user's input or as series of tests with dataset offered by ProgTest as .txt files. There is also option to run script under Valgrind.

# POSITIONAL ARGUMENTS
**filename**
: Path to C/C++ script.

# OPTIONS
**-h, --help**
: Show help message.

**-i, --install**
: Install/update. Need super user.

**-u, --uninstall**
: Uninstall. Need super user.

**-d, --data-path DATA_PATH** 
: Path to directory with test data. If not included, then script is runned only once and waits for users input.

**-v, --valgrind**
: Script is runned under Valgrind.

**-V, --val-args**
: Arguments for Valgrind as string and needs to start with \ .

**-D, --val-data**
: Data for Valgrind as string.

**-c, --compiler**
: Compiler (default is g++).

**-C, --compiler-args**
: Arguments for compiler (default is '-Wall -pedantic').

**-s, --silent**
: ptt will be silend (compiler, valgrind and tested script won't be).

**-n, --no-colors**
: Output of ptt is without any colors.

# EXAMPLES
**ptt cvika/ukol.c**
: Runs script once and waits for user's input.

**ptt -d 'cvika/sample/CZE' cvika/ukol.c**
: Runs script for every test dataset from directory 'cvika/sample/CZE' and compares output with template from dataset.

**ptt -v cvika/ukol.c**
: Runs script once and waits for user's input under Valgrind.

**ptt -v -V '\\--leak-check' -d 'cvika/sample/CZE' cvika/ukol.c**
: Runs script for every test dataset from directory 'cvika/sample/CZE' under Valgrind with Valgrind argument '--leak-check' and compares output with template from dataset.

# AUTHORS
Written by Jakub Anderle

# BUGS
Submit bug report online at: <https://github.com/KubaBoi/ptt/issues>

# SEE ALSO
Full documentation ad sources at: <https://github.com/KubaBoi/ptt>
