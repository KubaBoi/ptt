#!/usr/bin/env python3
"""
Test tool for ProgTests from CVUT FIT

version: 0.5.10
"""
__docformat__ = "reStructedText"

#IMPORT
import sys
import subprocess
import argparse

from manageClasses import *
from compilator import Compilator
from runner import Runner
from manager import Manager
#ENDIMPORT

def main():
	"""
	Entry point into the program.
	"""
	
	parser = argparse.ArgumentParser(
		prog="ptt",
		description="Test tool for ProgTest from CVUT FIT",
		epilog="Neco neco")
		
	parser.add_argument("filename", 
			help="Path to C/C++ script")
			
	parser.add_argument("-i", "--install", action="store_true", default=False,
			help="Install/update. Need super user.")
	parser.add_argument("-u", "--uninstall", action="store_true", default=False,
			help="Uninstall. Need super user.")
	parser.add_argument("-v", "--version", action="store_true", default=False,
			help="Show version")
			
	parser.add_argument("-d", "--data-path", action="store", default=False,
		        help="Path to directory with test data. If path is file, then script is runned only once with data from path file. If not included, then script is runned only once and waits for users input.")
	parser.add_argument("-g", "--valgrind", action="store_true",
			help="Script is runned under Valgrind")
	parser.add_argument("-G", "--val-args", action="store", default="",
			help="Arguments for Valgrind as string and needs to start with \\")
	parser.add_argument("-D", "--val-data", action="store", default="",
			help="Data for Valgrind as string")
	parser.add_argument("-c", "--compiler", action="store", default="g++",
			help="Compiler (default is g++)")
	parser.add_argument("-C", "--compiler-args", action="store", default="\\-Wall -pedantic",
			help="Arguments for compiler (default is '-Wall -pedantic')")
	parser.add_argument("-k", "--keep-links", action="store_true", default=False,
			help="Keeps link (.o) files from compilation")
			
	parser.add_argument("-m", "--milli-seconds", action="store_true", default=False,
			help="Time is counted in milliseconds")
	parser.add_argument("-s", "--silent", action="store_true", default=False,
			help="ptt will be silent (compiler, valgrind and tested script won't be)")
	parser.add_argument("-n", "--no-colors", action="store_true", default=False,
			help="Output is without any colors")
	
	args = parser.parse_args()
	script_path = args.filename
	
	if (args.no_colors):
		C.noColors()
	if (args.silent):
		C.silent()
	if (args.milli_seconds):
		C.milliseconds()
	
	if (args.valgrind):
		val_args = args.val_args.replace("\\", "").strip()
		cmd = ["valgrind", f"{val_args}", f"./{script_path.replace('.c', '')}", f"{args.val_data}"]
	else:
		cmd = [f"./{script_path.replace('.c', '')}"]
	
	while ("" in cmd):
		cmd.remove("")
	
	compiler = args.compiler
	compiler_args = args.compiler_args.replace("\\", "").split(" ")
	
	if (Compilator.compile(script_path, compiler, compiler_args) == 0):
		if (not args.keep_links):
			Compilator.removeLinks(script_path)
	
		if (not args.data_path):
			subprocess.call(cmd)
		else:
			Runner.runTests(script_path, args.data_path, cmd)
		
		C.prnt("\n")
		C.prnt("Testing done:")
		C.prnt("Compiler:", compiler)
		C.prnt("Compiler args:", *compiler_args)
		C.prnt("Valgrind:", args.valgrind)
		C.prnt("Valgrind args:", args.val_args)
		C.prnt("")
		if ("-Wall" not in compiler_args or "-pedantic" not in compiler_args):
			C.prnt(f"{C.WARNING}WARNING - there is missing -Wall or -pedantic in compilation{C.ENDC}")
		if (not args.valgrind):
			if (args.val_args != ""):
				C.prnt(f"{C.WARNING}WARNING - there are valgrind arguments (-V) specified but valgrind (-v) is not enabled{C.ENDC}")
			if (args.val_data != ""):
				C.prnt(f"{C.WARNING}WARNING - there are valgrind data (-D) specified but valgrind (-v) is not enabled{C.ENDC}")

if (__name__ == "__main__"):
	args = args = sys.argv
	if (len(args) > 1):
		if (args[1] == "-i" or args[1] == "--install"):
			exit(Manager.install())
		elif (args[1] == "-u" or args[1] == "--uninstall"):
			exit(Manager.uninstall())
		elif (args[1] == "-v" or args[1] == "--version"):
			exit(Manager.version())
	exit(main())

