---
title: ProgTestTest
section: 1
header: User Manual
footer: ptt 1.0.0
date: December 2, 2022
---

# ProgTestTest
ptt - Test tool for ProgTest from CVUT FIT

# SYNOPSIS
**ptt** [-h] [-i] [-u] [-v] [-d DATA_PATH] [-l] [-L VAL_ARGS] [-D VAL_DATA] [-c COMPILER] [-C COMPILER_ARGS] [-k] [-g] [-m] [-s] [-n] filename

# DESCRIPTION
**ptt** is simple script for testing your ProgTest. Via oneline shell command you can compile C/C++ script (by creating Makefile) and run them as single instance with user's input or as series of tests with dataset offered by ProgTest as .txt files. There is also option to run script under Valgrind.

You can generate own random datasets. Those are not for checking functionality of your program but for checking of your memory management thanks to randomness.

# POSITIONAL ARGUMENTS
**filename**
: Path to C/C++ script.

# OPTIONS
**-h, --help**
: Show help message.

**-v, --version**
: Show version.

**-d, --data-path DATA_PATH** 
: Path to directory with test data. If path is file, then script is runned only once with data from path file. If not included, then script is runned only once and waits for users input.

**-l, --valgrind**
: Script is runned under Valgrind.

**-L, --val-args**
: Arguments for Valgrind as string and needs to start with \ .

**-D, --val-data**
: Data for Valgrind as string.

**-c, --compiler**
: Compiler (default is g++).

**-C, --compiler-args**
: Arguments for compiler (default is '-Wall -pedantic').

**-k, --keep-links**
: Keeps link (.o) files from compilation.

**-g, --generate**
: Starts generator for new dataset and then tests the script. Asks for data regex template and how many files it should generate. More about regex in **REGEX FOR GENERATOR** section.

**-t, --tests**
: Runs tests but does not compare them with output templates but with it's input.

**-m, --milli-seconds**
: Time is counted in milliseconds.

**-s, --silent**
: ptt will be silent (compiler, valgrind and tested script won't be).

**-n, --no-colors**
: Output of ptt is without any colors.

# EXAMPLES
**ptt cvika/ukol.c**
: Runs script once and waits for user's input.

**ptt -d 'cvika/sample/CZE' cvika/ukol.c**
: Runs script for every test dataset from directory 'cvika/sample/CZE' and compares output with template from dataset.

**ptt -g cvika/ukol.c**
: Runs script once and waits for user's input under Valgrind.

**ptt -g -G '\\--leak-check=full' -d 'cvika/sample/CZE' cvika/ukol.c**
: Runs script for every test dataset from directory 'cvika/sample/CZE' under Valgrind with Valgrind argument '--leak-check' and compares output with template from dataset.

# REGEX FOR GENERATOR
Regex is similar to C/C++ scanf or prinf. Every value can have it's range. If range is not included then it is totaly random value. Range is symbolized with ",". If range is only one number than it is not range and value will be the number.

## Specifiers

**%c**
: single character

**%d**
: decimal number (signed int)

**%s**
: string

**%g**
: double

**%f**
: float

**%o**
: octadecimal number 

**%u**
: unsigned int 

**%x**
: hexadecimal number 

**%X**
: hexadecimal number uppercase 

## Examples

**%0,5d**
: decimal number from 0 to 5 (5 not included)

**%10,500s**
: string with length from 10 to 500 characters (500 included, because ending zero)

## Groups
You can set that generator will generate more then one value of each type. For example there should be 100 to 200 lines of some values. So you write regex for those values and include them into group.

Groups are symbolized with "\$()\$".

Count of groups are at the end of group, like in examples. If range not included it will generate 0 to 100 times.

## Examples for groups

**\$(%5,12d - \%10s - \%f\n)5,10\$**
: 5 to 10 lines with 1 decimal from 5 to 12 " - " 1 string length 10 " - " random float. 

**\$(%0,250d,%1,8f,%-10.54,150g\n)5,9\$:%2,15s**
: 5 to 9 lines with 1 decimal from 0 to 250 "," float from 1 to 8 "," double from 10.54 to 150 and at the end of whole file is one 2 to 15 characters long string

# AUTHORS
Written by Jakub Anderle

# BUGS
Submit bug report online at: <https://github.com/KubaBoi/ptt/issues>

# SEE ALSO
Sources at: <https://github.com/KubaBoi/ptt>
