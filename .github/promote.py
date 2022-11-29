
import os

path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "..", "src", "ptt.py"))

with open(path, "r") as f:
	lines = f.readlines()
	
old_version = ""
for line in lines:
	if (line.startswith("version:")):
		vers = line.split(" ")[-1].strip().split(".")
		old_version = ".".join(vers)
		v = int(vers[2]) + 1
		vers[2] = str(v)
		print("Promoting version:", ".".join(vers))
		
with open(path, "r") as f:
	content = f.read()
with open(path, "w") as f:
	f.write(content.replace(old_version, ".".join(vers)))
	
