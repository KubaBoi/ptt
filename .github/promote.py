
import os

root_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), ".."))
path = os.path.join(root_path, "src", "ptt.py")
m_path = os.path.join(root_path, "src", "managerClasses.py")
control_path = os.path.join(root_path, "ptt", "DEBIAN", "control")

with open(path, "r") as f:
	lines = f.readlines()
	
old_version = ""
for line in lines:
	if (line.startswith("version:")):
		vers = line.split(" ")[-1].strip().split(".")
		old_version = ".".join(vers)
		v = int(vers[2]) + 1
		vers[2] = str(v)
		print(".".join(vers))

# main		
with open(path, "r") as f:
	content = f.read()
with open(path, "w") as f:
	f.write(content.replace(old_version, ".".join(vers)))

# manageClasse
with open(m_path, "r") as f:
	content = f.read()
with open(m_path, "w") as f:
	f.write(content.replace(old_version, ".".join(vers)))


# CONTROL

new_control = ""
with open(control_path, "r") as f:
	data_lines = f.readlines()

for line in data_lines:
	if (line.startswith("Version:")):
		new_control += "Version: " + ".".join(vers) + "\n"
	else:
		new_control += line
	
with open(control_path, "w") as f:
	f.write(new_control)
