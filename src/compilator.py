
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
	def compile(script_path, compiler, compiler_args):
		name = os.path.basename(script_path).replace(".c", "")
		modules = Compilator.findModules(script_path)
			
		mkf = M.MAKE_FILE_TEMP
		mkf = mkf.replace("$NAME$", name)
		mkf = mkf.replace("$MODULES$", " ".join(modules))
		mkf = mkf.replace("$COMPILER$", compiler)
		mkf = mkf.replace("$COMPILER_ARGS$", " ".join(compiler_args))
		
		with open("Makefile", "w") as f:
			f.write(mkf)
		
		ret = subprocess.call(["make"])
		if (ret != 0):
			C.prnt(f"{C.FAIL}{10*'='}Compilation process ended with code {C.OKCYAN}{ret}{C.FAIL}{10*'='}{C.ENDC}")
		else:
			C.prnt(f"{C.OKGREEN}{10*'='}Compilation process OK{10*'='}{C.ENDC}")
		return ret
