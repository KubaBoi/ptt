#!/usr/bin/env python3
"""
Test tool for ProgTests from CVUT FIT

version: 1.0.14
"""
__docformat__ = "reStructedText"

#IMPORT
import sys
import subprocess
import argparse

from managerClasses import *
from compilator import Compilator
from runner import Runner
from generator import Generator
from builder import Builder
#ENDIMPORT

def main():
	"""
	Entry point into the program.
	"""
	
	parser = argparse.ArgumentParser(
		prog="ptt",
		description="Test tool for ProgTest from CVUT FIT",
		epilog="Full documentation 'man ptt'")
		
	parser.add_argument("filename", 
			help="Path to C/C++ script")
			
	parser.add_argument("-v", "--version", action="store_true", default=False,
			help="Show version")
			
	parser.add_argument("-d", "--data-path", action="store", default=False,
		        help="Path to directory with test data. If path is file, then script is runned only once with data from path file. If not included, then script is runned only once and waits for users input.")
	parser.add_argument("-l", "--valgrind", action="store_true",
			help="Script is runned under Valgrind")
	parser.add_argument("-L", "--val-args", action="store", default="",
			help="Arguments for Valgrind as string and needs to start with \\")
	parser.add_argument("-g", "--gdb", action="store_true", default=False,
			help="Script is runned under GDB")
	parser.add_argument("-D", "--val-data", action="store", default="",
			help="Data for Valgrind as string")
	parser.add_argument("-c", "--compiler", action="store", default="g++",
			help="Compiler (default is g++)")
	parser.add_argument("-C", "--compiler-args", action="store", default="\\-Wall -pedantic",
			help="Arguments for compiler (default is '-Wall -pedantic')")
	parser.add_argument("-k", "--keep-links", action="store_true", default=False,
			help="Keeps link (.o) files from compilation")

	parser.add_argument("--generate", action="store_true", default=False,
			help="Starts generator for new dataset and then tests the script")
	parser.add_argument("-o", "--output", action="store", default="",
			help="Makes one .c file from all .h and .c source files. And runs this one .c file. If script is ASM, ptt will not remove temporary file after compilation.")

	parser.add_argument("-r", "--raw", action="store_true", default=False,
			help="Runs tests but only prints output to terminal. Does not compare with anything")
	parser.add_argument("-t", "--tests", action="store_true", default=False,
			help="Runs tests but does not compare them with output templates but with it's input")
	parser.add_argument("-m", "--milli-seconds", action="store_true", default=False,
			help="Time is counted in milliseconds")
	parser.add_argument("-s", "--silent", action="store_true", default=False,
			help="ptt will be silent (compiler, valgrind and tested script won't be)")
	parser.add_argument("-n", "--no-colors", action="store_true", default=False,
			help="Output is without any colors")
	parser.add_argument("-q", "--quit-fflush", action="store_true", default=False,
			help="Turn off adding 'fflush()' after every 'printf()' in script. Output would not be reachable for ptt if process ends by error.")
	
	args = parser.parse_args()
	script_path = args.filename
	is_one_file = False

	if (script_path.endswith(".s")):
		C.assembler()
		if (args.compiler_args == "\\-Wall -pedantic"):
			args.compiler_args = "\\-f elf64"
		if (args.compiler == "g++"):
			args.compiler = "nasm"

	
	if (args.no_colors):
		C.noColors()
	if (args.silent):
		C.silent()
	if (args.milli_seconds):
		C.milliseconds()
	if (args.raw):
		C.raw()
	if (args.tests):
		C.tests()
	if (args.output != ""):
		is_one_file = True
		if (C.MODE == 0):
			script_path = Builder.build(script_path, args.output)
			if (script_path == 0): 
				C.prnt(f"{C.WARNING}Cannot make one file source code because{C.ENDC}")
				C.prnt(f"{C.WARNING}chosen name is same as main script.{C.ENDC}")
				return
	if (args.quit_fflush):
		C.fflush()
	
	if (args.valgrind):
		val_args = args.val_args.replace("\\", "").strip()
		cmd = ["valgrind", f"{val_args}", f"./{script_path.replace(C.POST_FIX, '')}", f"{args.val_data}"]
	elif (args.gdb):
		cmd = ["gdb", f"./{script_path.replace(C.POST_FIX, '')}"]
	else:
		cmd = [f"./{script_path.replace(C.POST_FIX, '')}"]
	
	while ("" in cmd):
		cmd.remove("")
	
	compiler = args.compiler
	compiler_args = args.compiler_args.replace("\\", "").split(" ")

	compil = Compilator.compile(script_path, compiler, compiler_args, is_one_file)
	if (compil == 0):
		C.prnt(f"{C.OKGREEN}{10*'='}Compilation process OK{10*'='}{C.ENDC}")
		
		if (not args.keep_links):
			Compilator.removeLinks(script_path)
	
		if (not args.data_path):
			subprocess.call(cmd)
		else:
			Runner.runTests(args.data_path, cmd)
		
		C.prnt("\n")
		C.prnt("Testing done:")
		C.prnt("Compiler:", compiler)
		C.prnt("Compiler args:", *compiler_args)
		C.prnt("Valgrind:", args.valgrind)
		C.prnt("Valgrind args:", args.val_args)
		C.prnt("")
		if (C.MODE == 0):
			if ("-Wall" not in compiler_args or "-pedantic" not in compiler_args):
				C.prnt(f"{C.WARNING}WARNING - there is missing -Wall or -pedantic in compilation{C.ENDC}")
			if (not args.valgrind):
				if (args.val_args != ""):
					C.prnt(f"{C.WARNING}WARNING - there are valgrind arguments (-L) specified but valgrind (-l) is not enabled{C.ENDC}")
				if (args.val_data != ""):
					C.prnt(f"{C.WARNING}WARNING - there are valgrind data (-D) specified but valgrind (-l) is not enabled{C.ENDC}")
	else:
		C.prnt(f"{C.FAIL}{10*'='}Compilation process ended with code {C.OKCYAN}{compil}{C.FAIL}{10*'='}{C.ENDC}")

if (__name__ == "__main__"):
	args = args = sys.argv
	if (len(args) > 1):
		if (args[1] == "-v" or args[1] == "--version"):
			exit(f"ProgTestTest v({V.VERSION})")
		elif (args[1] == "-g" or args[1] == "--generate"):
			g = Generator()
			count = int(input("How many files do you want to generate? "))
			g.generate(count)
			exit()
	exit(main())

