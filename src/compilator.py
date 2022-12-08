
import os
import subprocess

from managerClasses import M, C

class Compilator:

	@staticmethod
	def findModules(script_path):
		headers = [] 
		sources = []
		for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(script_path))):
			for f in files:
				if (f.endswith(".h")):
					headers.append(f.replace(".h", ".o"))
				elif (f.endswith(".c")):
					sources.append(f.replace(".c", ".o"))
					
		modules = []
		for source in sources: 
			if (source in headers):	
				modules.append(source)
				C.prnt("Adding module:", source) 
		return modules

	@staticmethod
	def removeLinks(script_path):
		for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(script_path))):
			for f in files:
				if (f.endswith(".o")): os.remove(f)

	@staticmethod
	def addFflush(script_path):
		with open(script_path, "r", encoding="utf-8") as f:
			data_lines = f.readlines()

		for i, line in enumerate(data_lines):
			if (line.strip().startswith("printf")):
				data_lines[i] = line.replace("\n", " ") + "fflush(stdout);\n"
	
		with open(script_path.replace(".c", "_temp.c"), "w", encoding="utf-8") as f:
			f.write("".join(data_lines))

	@staticmethod
	def compile(script_path, compiler, compiler_args, is_one_file):
		Compilator.addFflush(script_path)

		name = os.path.basename(script_path).replace(".c", "") + "_temp"
		
		if (not is_one_file):
			modules = Compilator.findModules(script_path)

			mkf = M.MAKE_FILE_TEMP
			mkf = mkf.replace("$NAME$", name)
			mkf = mkf.replace("$MODULES$", " ".join(modules))
			mkf = mkf.replace("$COMPILER$", compiler)
			mkf = mkf.replace("$COMPILER_ARGS$", " ".join(compiler_args))
			
			with open("Makefile", "w") as f:
				f.write(mkf)
			
			ret = subprocess.call(["make"])
		else:
			ret = subprocess.call([compiler, *compiler_args, script_path, "-o", name])

		os.remove(script_path.replace(".c", "_temp.c"))
		if (os.path.exists(script_path.replace(".c", "_temp"))):
			os.rename(script_path.replace(".c", "_temp"), script_path.replace(".c", ""))
			

		if (ret != 0):
			C.prnt(f"{C.FAIL}{10*'='}Compilation process ended with code {C.OKCYAN}{ret}{C.FAIL}{10*'='}{C.ENDC}")
		else:
			C.prnt(f"{C.OKGREEN}{10*'='}Compilation process OK{10*'='}{C.ENDC}")
		return ret
