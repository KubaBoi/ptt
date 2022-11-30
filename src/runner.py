
import os
import time
import subprocess

from managerClasses import C

class Runner:
	
	@staticmethod
	def convertTime(tm):
		if (C.MILLI_SECONDS): return f"{1000 * tm} ms"
		return f"{tm} s"

	@staticmethod
	def readFiles(files_path):
		return sorted( filter( lambda x: os.path.isfile(os.path.join(files_path, x)),
		                os.listdir(files_path) ) )

	@staticmethod
	def run(script_path, input_file, output_file, cmd):
		index = cmd.index(f"./{script_path.replace('.c', '')}")
		cmd[index] += f" < \"{input_file}\" > \"{output_file}\""
		tm = time.time()
		ret = subprocess.call(" ".join(cmd), shell=True)
		return ret, time.time() - tm

	@staticmethod		
	def runTests(script_path, files_path, cmd):
		counter = 0
		fails = 0
		
		if (os.path.isdir(files_path)):
			files = Runner.readFiles(files_path)

			for i, file in enumerate(files):
				if (i % 3 != 0): continue
				
				C.prnt("");
				C.prnt(f"{C.HEADER}{5*'='}Test {counter}. - {file}{5*'='}{C.ENDC}")
				counter += 1
				
				fails += Runner.runOneFile(script_path, os.path.join(files_path, file), cmd)
		else:
			C.prnt("");
			C.prnt(f"{C.HEADER}{5*'='}Test {counter}. - {files_path}{5*'='}{C.ENDC}")
			counter += 1
			
			fails = Runner.runOneFile(script_path, files_path, cmd)
			
		C.prnt(20*"=")
		C.prnt(f"Test count: {counter}")
		C.prnt(f"Failed tests: {fails}")
		
	@staticmethod
	def runOneFile(script_path, file, cmd):
		ret, tm = Runner.run(script_path, file, "tmp.txt", cmd.copy())
		if (ret != 0):
			C.prnt(f"{C.WARNING}{10*'='}Process ended with code {C.OKBLUE}{ret}{C.WARNING}{10*'='}{C.ENDC}")			
		
		with open("tmp.txt", "r", encoding="utf-8") as f:
			out = f.read()
		os.remove("tmp.txt")
		
		with open(file.replace("in", "out"), "r", encoding="utf-8") as fo:
			temp = fo.read()
		
		if (temp != out):	
			with open(file, "r", encoding="utf-8") as f:
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
			C.prnt(f"Time: {Runner.convertTime(tm)}")
			return 1
		else:
			C.prnt(f"{C.OKGREEN}OK{C.ENDC}")
			C.prnt(f"Time: {Runner.convertTime(tm)}")
			return 0
