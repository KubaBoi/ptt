#!/usr/bin/env python3
"""
Script makes from src one file
"""

import os

def readLines(file_path):
    if (not os.path.exists(file_path)):
        raise FileNotFoundError()

    if (not file_path.endswith(".py")):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        data_lines = f.read().split("\n")
    return data_lines

def findImports(dir_path):
    imports = []
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            data_lines = readLines(os.path.join(root, f))
            for line in data_lines:
                if (line.startswith("import")):
                    if (line not in imports):
                        imports.append(line)
    return imports

def findClasses(dir_path):
    classes = []

    for root, dirs, files in os.walk(dir_path):
        for f in files:
            data_lines = readLines(os.path.join(root, f))
            for i, line in enumerate(data_lines):
                if (line.startswith("class")):
                    classes.append(line + "\n")

                    i += 1
                    line = data_lines[i]
                    while (not line.startswith("class")):
                        classes[-1] += line + "\n"
                        i += 1
                        if (i >= len(data_lines)):
                            break
                        line = data_lines[i]
    return classes

def getMainNoImports(file_path):
    data_lines = readLines(file_path)
    start_index = data_lines.index("#IMPORT")
    end_index = data_lines.index("#ENDIMPORT")

    new_lines = data_lines[:start_index + 1] + data_lines[end_index + 1:]
    return "\n".join(new_lines)

def prepareImports(imports, classes):
    imps = "\n".join(imports)
    imps += "\n\n"
    imps += "\n".join(classes)
    return imps

    

main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
package_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ptt"))
main_file = os.path.join(main_dir, "ptt.py")

imports = findImports(main_dir)
classes = findClasses(main_dir)
main = getMainNoImports(main_file)
imps = prepareImports(imports, classes)

with open(os.path.join(package_dir, "usr", "bin", "ptt"), "w", encoding="utf-8") as f:
    f.write(main.replace("#IMPORT", imps))