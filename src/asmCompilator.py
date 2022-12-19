
import os
import subprocess

from managerClasses import M, C

class AsmCompilator:

    added_files = []

    @staticmethod
    def findModules(script_path):
        file_path = os.path.abspath(script_path)
        dir_path = os.path.dirname(file_path)

        with open(file_path, "r") as f:
            data_lines = f.readlines()

        content = ""
        for line in data_lines:
            if (line.startswith(";import")):
                parts = line.split(" ")

                while " " in parts: 
                    parts.remove("")
                line = ""
                for i in range(1, len(parts)):
                    parts[i] = os.path.join(dir_path, parts[i].strip())
                    if (parts[i] not in AsmCompilator.added_files):
                        if (os.path.exists(parts[i])):
                            line += AsmCompilator.findModules(parts[i])
                            C.prnt("found: ", parts[i])
                            AsmCompilator.added_files.append(parts[i])
                        else:
                            C.prnt(f"ERROR: {parts[i]} does not exists.")
                            exit(1)
            content += line

        return content + "\n\n"

    @staticmethod
    def removeFiles(temp_name, link_name, is_one_file):
        if (not is_one_file and os.path.exists(temp_name)):
            C.prnt("Removing temporary file...")
            os.remove(temp_name)

    @staticmethod
    def compile(script_path, compiler, compiler_args, is_one_file):
        C.prnt("Finding modules...")
        content = AsmCompilator.findModules(script_path) 
        name = script_path.replace(C.POST_FIX, '')
        temp_name = script_path.replace(C.POST_FIX, '_temp.s')
        link_name = temp_name.replace(C.POST_FIX, '.o')
        with open(f"{temp_name}", "w") as f:
            f.write(content)

        C.prnt("Assembling...")
        ret = subprocess.call([compiler, *compiler_args, temp_name])      
        if (ret == 0):
            C.prnt("Linking...")
            ret = subprocess.call(["ld", f"-o", name, link_name])
        AsmCompilator.removeFiles(temp_name, link_name, is_one_file)
        return ret
