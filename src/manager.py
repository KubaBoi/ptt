
import os
import subprocess
import requests

from manageClasses import V

class Manager:

	@staticmethod
	def install():
		if (os.path.exists("/usr/bin/ptt")):
			if (input("/usr/bin/ptt already exists. Do you want to update ptt? [y/n] ") != "y"):
				print("Aborting installation...")
				return
		print("Downloading latest version...")
		req = requests.get("https://raw.githubusercontent.com/KubaBoi/ptt/master/ptt")
		if (req.status_code == 200):
			print("Installing...")
			content = req.text
		else:
			print("Download was not successfull")
			print("Installing from local sources...")
			with open(os.path.realpath(__file__), "r", encoding="utf-8") as f:
				content = f.read()
				
		try:
			with open("/usr/bin/ptt", "w", encoding="utf-8") as f:
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
	
	@staticmethod
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
	
	@staticmethod
	def version():
		print(f"ProgTestTest v({V.VERSION})")