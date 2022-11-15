#!/usr/bin/env python3
"""
Test tool for ProgTests from CVUT FIT

version: 0.5.4
"""
__docformat__ = "reStructedText"

import os
import sys
import subprocess
import argparse
import inspect
import requests

class V:
	VERSION = "0.5.4"

class C:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	
	SILENT = False
	
	@staticmethod
	def noColors():
		members = inspect.getmembers(C, lambda a:not(inspect.isroutine(a)))
		for i in members:
			if (i[0][0] != "_"): setattr(C, i[0], "")
			
	@staticmethod
	def silent():
		C.SILENT = True
			
	@staticmethod
	def prnt(*str):
		if (not C.SILENT): print(*str)
		
def install():
	if (os.path.exists("/usr/bin/ptt")):
		if (input("/usr/bin/ptt already exists. Do you want to update ptt? [y/n] ") != "y"):
			print("Aborting installation...")
			return
	print("Downloading latest version...")
	req = requests.get("https://raw.githubusercontent.com/KubaBoi/ptt/master/ptt.py")
	if (req.status_code == 200):
		print("Installing...")
		content = req.text
	else:
		print("Download was not successfull")
		print("Installing from local sources...")
		with open(os.path.realpath(__file__), "r") as f:
			content = f.read()
			
	try:
		with open("/usr/bin/ptt", "w") as f:
			f.write(content)
		subprocess.call(["sudo", "chmod", "+x", "/usr/bin/ptt"])
		print("Installation was successfull")
	except Exception as e:
		print("ERROR:", e)
		print("Installation was not successfull")
		print("Try to run 'sudo ptt -i' or 'sudo ptt.py -i'")
		return
	
	print("Downloading latest manual...")
	req = requests.get("https://raw.githubusercontent.com/KubaBoi/ptt/master/ptt.1.gz")
	if (req.status_code == 200):
		print("Installing manual...")
		with open("/usr/share/man/man1/ptt.1.gz", "wb") as f:
			f.write(req.content)
		subprocess.call(["sudo", "mandb"])
	else:
		print("Latest manual was not downloaded. 'man ptt' may not be functional")

	process = subprocess.Popen(['ptt', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = process.communicate()
	print(f"\nSuccessfully installed {out.decode('utf-8')}")
		
def uninstall():
	if (input("Do you really want to uninstall ptt? [y/n] ") != "y"):
		return
	try:
		if (os.path.exists("/usr/bin/ptt")):
			os.remove("/usr/bin/ptt")
		if (os.path.exists("/usr/share/man/man1/ptt.1.gz")):
			os.remove("/usr/share/man/man1/ptt.1.gz")
			subprocess.call(["sudo", "mandb"])
		print("Uninstallation was successfull. Sorry to hear that :(")
	except Exception as e:
		print("ERROR:", e)
		print("Uninstallation was not successfull")
		print("Try to run 'sudo ptt -u' or 'sudo ptt.py -u'")
		
def version():
	print(f"ProgTestTest v({V.VERSION})")
		
def compile(script_path, compiler, compiler_args):
	ret = subprocess.call([compiler, *compiler_args, script_path, "-o", script_path + ".out"])
	if (ret != 0):
		C.prnt(f"{C.FAIL}{10*'='}Compilation process ended with code {C.OKCYAN}{ret}{C.FAIL}{10*'='}{C.ENDC}")
	else:
		C.prnt(f"{C.OKGREEN}{10*'='}Compilation process OK{10*'='}{C.ENDC}")
	return ret

def run(script_path, input_file, output_file, cmd):
	index = cmd.index(f"./{script_path}.out")
	cmd[index] += f" < \"{input_file}\" > \"{output_file}\""
	ret = subprocess.call(" ".join(cmd), shell=True)
	return ret

def readFiles(files_path):
	return sorted( filter( lambda x: os.path.isfile(os.path.join(files_path, x)),
                        os.listdir(files_path) ) )
	
def runTests(script_path, files_path, cmd):
	counter = 0
	fails = 0
	
	if (os.path.isdir(files_path)):
		files = readFiles(files_path)

		for i, file in enumerate(files):
			if (i % 3 != 0): continue
			
			C.prnt("");
			C.prnt(f"{C.HEADER}{5*'='}Test {counter}. - {file}{5*'='}{C.ENDC}")
			counter += 1
			
			fails += runOneFile(script_path, os.path.join(files_path, file), cmd)
	else:
		C.prnt("");
		C.prnt(f"{C.HEADER}{5*'='}Test {counter}. - {files_path}{5*'='}{C.ENDC}")
		counter += 1
		
		fails = runOneFile(script_path, files_path, cmd)
		
	C.prnt(20*"=")
	C.prnt(f"Test count: {counter}")
	C.prnt(f"Failed tests: {fails}")
	
def runOneFile(script_path, file, cmd):
	ret = run(script_path, file, "tmp.txt", cmd.copy())
	if (ret != 0):
		C.prnt(f"{C.WARNING}{10*'='}Process ended with code {C.OKBLUE}{ret}{C.WARNING}{10*'='}{C.ENDC}")			
	
	with open("tmp.txt", "r") as f:
		out = f.read()
	
	with open(file.replace("in", "out"), "r") as fo:
		temp = fo.read()
	
	if (temp != out):	
		with open(file, "r") as f:
			in_data = f.read()
		
		C.prnt("")
		C.prnt("Input:")
		
		C.prnt(in_data)
		
		out_split = out.split("\n")
		temp_split = temp.split("\n")
		
		C.prnt("")
		C.prnt("Output:")
		
		for line1, line2 in zip(out_split, temp_split):
			h = f"{C.OKGREEN}>> {C.ENDC}"
			if (line1 != line2): h = f"{C.FAIL}>> {C.ENDC}"
			C.prnt(f"{h}{line1}{(30 - len(line1)) * ' '} {C.BOLD}|{C.ENDC} {line2}")
			
		if (len(out_split) > len(temp_split)):
			for i in range(len(temp_split), len(out_split)):
				line = out_split[i]
				C.prnt(f"{C.FAIL}>> {C.ENDC}" + line)
				
		elif (len(temp_split) > len(out_split)):
			for i in range(len(out_split), len(temp_split)):
				line = temp_split[i]
				C.prnt(f"{C.FAIL}>> {C.ENDC}" + ((30 - len(line)) * " ") + f" {C.BOLD}|{C.ENDC} " + line)
		
		C.prnt("")
		C.prnt(5*"=")
		C.prnt(f"{C.FAIL}Output not matching{C.ENDC}")
		return 1
	else:
		C.prnt(f"{C.OKGREEN}OK{C.ENDC}")
		return 0
		
	os.remove("tmp.txt")
		
# METHODS

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
		        help="Path to directory with test data. If not included, then script is runned only once and waits for users input")
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
	
	if (args.valgrind):
		val_args = args.val_args.replace("\\", "").strip()
		cmd = ["valgrind", f"{val_args}", f"./{script_path}.out", f"{args.val_data}"]
	else:
		cmd = [f"./{script_path}.out"]
	
	while ("" in cmd):
		cmd.remove("")
	
	compiler = args.compiler
	compiler_args = args.compiler_args.replace("\\", "").split(" ")
	
	if (compile(script_path, compiler, compiler_args) == 0):
		if (not args.data_path):
			subprocess.call(cmd)
		else:
			runTests(script_path, args.data_path, cmd)
		
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
			exit(install())
		elif (args[1] == "-u" or args[1] == "--uninstall"):
			exit(uninstall())
		elif (args[1] == "-v" or args[1] == "--version"):
			exit(version())
	exit(main())

