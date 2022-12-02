
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
	def run(input_file, cmd):
		tm = time.time()
		process = subprocess.Popen(cmd, text=True,
			stdin=open(input_file, "rb"),
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT)

		ret = process.wait()
		out = process.stdout.read()

		return ret, out, time.time() - tm

	@staticmethod		
	def runTests(files_path, cmd):
		counter = 0
		fails = 0
		
		if (os.path.isdir(files_path)):
			files = Runner.readFiles(files_path)

			for i, file in enumerate(files):
				if (i % 3 != 0): continue
				
				C.prnt("");
				C.prnt(f"{C.HEADER}{5*'='}Test {counter}. - {file}{5*'='}{C.ENDC}")
				counter += 1
				
				fails += Runner.runOneFile(os.path.join(files_path, file), cmd)
		else:
			C.prnt("");
			C.prnt(f"{C.HEADER}{5*'='}Test {counter}. - {files_path}{5*'='}{C.ENDC}")
			counter += 1
			
			fails = Runner.runOneFile(files_path, cmd)
			
		C.prnt(C.HEADER + 20*"=" + C.ENDC)
		C.prnt(f"Test count: {counter}")
		C.prnt(f"Failed tests: {fails}")

	@staticmethod
	def printInput(file):
		with open(file, "r", encoding="utf-8") as f:
				in_data = f.read()
		C.prnt("")
		C.prnt("Input:")		
		C.prnt(in_data)

	@staticmethod
	def compare(out_split, temp_split):
		max_len = 29
		for line in out_split:
			if (max_len < len(line)):
				max_len = len(line)
		max_len += 1

		delimiter = f"{C.BOLD}{C.OKBLUE}|{C.ENDC}"

		for line1, line2 in zip(out_split, temp_split):
			h = f"{C.OKGREEN}>> {C.ENDC}"
			if (line1 != line2): h = f"{C.FAIL}>> {C.ENDC}"
			C.prnt(f"{h}{line1}{(max_len - len(line1)) * ' '} {delimiter} {line2}")
			
		if (len(out_split) > len(temp_split)):
			for i in range(len(temp_split), len(out_split)):
				line = out_split[i]
				C.prnt(f"{C.FAIL}>> {C.ENDC}" + line)
				
		elif (len(temp_split) > len(out_split)):
			for i in range(len(out_split), len(temp_split)):
				line = temp_split[i]
				C.prnt(f"{C.FAIL}>> {C.ENDC}" + ((max_len * " ") + f" {delimiter} " + line))
		
		
	@staticmethod
	def runOneFile(file, cmd):
		ret, out, tm = Runner.run(file, cmd.copy())
		if (ret != 0):
			C.prnt(f"{C.WARNING}{10*'='}Process ended with code {C.OKBLUE}{ret}{C.WARNING}{10*'='}{C.ENDC}")			
		
		temp_file = file
		if (C.TESTS):
			temp_file = temp_file.replace("in", "out")

		with open(temp_file, "r", encoding="utf-8") as fo:
			temp = fo.read()
		
		if (temp != out and C.TESTS):	
			Runner.printInput(file)
			
			out_split = out.split("\n")
			temp_split = temp.split("\n")
			
			C.prnt("")
			C.prnt("Output:")
			
			Runner.compare(out_split, temp_split)

			C.prnt("")
			C.prnt(5*"=")
			C.prnt(f"{C.FAIL}Output not matching{C.ENDC}")
			C.prnt(f"Time: {Runner.convertTime(tm)}")
			return 1
		elif (C.TESTS):
			C.prnt(f"{C.OKGREEN}OK{C.ENDC}")
			C.prnt(f"Time: {Runner.convertTime(tm)}")
			return 0
		else:
			out_split = out.split("\n")
			temp_split = temp.split("\n")
			
			C.prnt("")
			C.prnt("Output:")
			
			Runner.compare(out_split, temp_split)

			C.prnt("")
			C.prnt(5*"=")
			C.prnt(f"Time: {Runner.convertTime(tm)}")
			return 0

