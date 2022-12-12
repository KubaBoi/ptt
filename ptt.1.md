---
title: ProgTestTest
section: 1
header: User Manual
footer: ptt 1.0.11
date: December 10, 2022
---

# ProgTestTest
ptt - Test tool for ProgTest from CVUT FIT

# SYNOPSIS
**ptt** [-h] [-i] [-u] [-v] [-d DATA_PATH] [-l] [-L VAL_ARGS] [-D VAL_DATA] [-c COMPILER] [-C COMPILER_ARGS] [-k] [-g] [-m] [-s] [-n] [-q] filename

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
: Starts generator for new dataset. Asks for data regex template and how many files it should generate. More about regex in **REGEX FOR GENERATOR** section.

**-o, --output**
: Makes one .c file from all .h and .c source files. And runs this one .c file.

**-r, --raw**
: Runs tests but only prints output to terminal. Does not compare with anything.

**-t, --tests**
: Runs tests but does not compare them with output templates but with it's input.

**-m, --milli-seconds**
: Time is counted in milliseconds.

**-s, --silent**
: ptt will be silent (compiler, valgrind and tested script won't be).

**-n, --no-colors**
: Output of ptt is without any colors.

**-q, --quit-fflush**
: Turn off adding 'fflush()' after every 'printf()' in script. Output would not be reachable for ptt if process ends by error.

# EXAMPLES
**ptt cvika/ukol.c**
: Runs script once and waits for user's input.

**ptt -d 'cvika/sample/CZE' cvika/ukol.c**
: Runs script for every test dataset from directory 'cvika/sample/CZE' and compares output with template from dataset.

**ptt -l cvika/ukol.c**
: Runs script once and waits for user's input under Valgrind.

**ptt -l -L '\\--leak-check=full' -d 'cvika/sample/CZE' cvika/ukol.c**
: Runs script for every test dataset from directory 'cvika/sample/CZE' under Valgrind with Valgrind argument '--leak-check' and compares output with template from dataset.

# REGEX FOR GENERATOR
Regex is similar to C/C++ scanf or prinf. Every value can have it's range. If range is not included then it is totaly random value. Range is symbolized with ",". If range is only one number than it's range starts at 0 (cannot go to negative values, only forwards).

## Specifiers

**%c**
: single character

**%d**
: decimal number (signed int)Example generated file:


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

**\$(%5,12d - %10s - %f\\n)5,10\$**
: 5 to 10 lines with 1 decimal from 5 to 12 " - " 1 string length 10 " - " random float.
```
Example of generated file:
9 - S2rz - 3.8328348747078637e+37
7 -  - 4.926247000847152e+37
7 - 6uvED3Jm - 1.5525009816519334e+37
8 -  - 1.7615361925092063e+37
11 - AmJZ - 2.075909449890427e+38
11 - fPWdo7J0 - 2.1674784130879944e+38
```


**\$(%0,250d, %1,8f, %-10.54,150g\\n)5,9\$:%2,15s**
: 5 to 9 lines with 1 decimal from 0 to 250 "," float from 1 to 8 "," double from 10.54 to 150 and at the end of whole file is ":" and one 2 to 15 characters long string.
```
Example of generated file:
73, 4.445772835342223, 146.17131540588755
188, 4.465919464359487, 12.900279129182966
217, 2.7150156163309758, 115.90500331811384
92, 2.2112414659558794, 35.54010634748203
117, 5.811310246641262, 42.38128446686212
133, 4.131879588745505, 76.45844625121993
1, 5.192964977710644, 76.70838507583821
:2,15s  
```

# AUTHORS
Written by Jakub Anderle

# BUGS
Submit bug report online at: <https://github.com/KubaBoi/ptt/issues>

# SEE ALSO
Sources at: <https://github.com/KubaBoi/ptt>
