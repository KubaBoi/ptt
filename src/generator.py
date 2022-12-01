
import os
import random

from specifier import *

class Generator:
    """
    Class for dataset generation

    Regex:
        as scanf in c/c++

    Range:
        Every value can have a range

        If range not included then it is totaly random value

        Example:
            %0,5d - decimal number from 0 to 5 (5 not included)
            %10,500s - string with length from 10 to 500 characters (500 included because ending zero)
    
        Groups:
            $(%5,12d - %10s - %f\n)5,10$ 
            
                - 5 to 10 lines with 
                one decimal from 5 to 12, string length 10 and random float

            $(%0,250d,%1,8f,%-10.54,150g\n)5,9$:%2,15s

                - 5 to 9 lines with decimal, float, double 
                and at the end is one 2 to 15 characters long string
    """

    SPECS = {
        "c": "char",
        "d": "decimal",
        "s": "string",
        "g": "double",
        "f": "flt",
        "o": "octa",
        "u": "unsigned",
        "x": "hexa",
        "X": "hexa"
    }

    def __init__(self):
        self.reg = input("Regex for your test data: ")
        self.reg = self.reg.replace("\\n", "\n")
        self.reg = self.reg.replace("\\t", "\t")

    def findSpecs(self, reg):
        specsValues = []

        ignore = -1
        for i, char in enumerate(reg):
            if (i <= ignore): 
                if (ignore == i): ignore = -1
                continue

            if (char == "\\"):
                ignore = i + 1
            elif (char == "%"):
                val = char
                start_index = i
                i += 1
                char = reg[i]
                while (char.isnumeric() or char == "-" or char == "." or char == ","):
                    val += char
                    i += 1
                    if (i >= len(reg)): 
                        raise InvalidRegex(f"Missing end of regex specification at {start_index} position")
                    char = reg[i]

                if (char not in self.SPECS.keys()):
                    raise InvalidRegex(f"Uknown regex specification at {start_index} position")
                val += char
                specsValues.append(val)
            elif (char == "$"):
                val = char
                start_index = i
                i += 1
                char = reg[i]
                if (char != "("):
                    continue

                while (char != "$"):
                    val += char
                    i += 1
                    if (i >= len(reg)):
                        raise InvalidRegex(f"Missing end of group regex specification at {start_index} position")
                    char = reg[i]
                
                ignore = i
                val += char
                rng = val.replace("$", "").split(")")[-1]
                valS = val.replace("$(", "").replace(f"){rng}$", "")
                specsValues.append([rng, self.findSpecs(valS), val])
        return specsValues

    def getName(self, number, count):
        s_number = str(number)
        s_count = str(count)

        val = ""
        for i in range(len(s_count) - len(s_number)):
            val += "0"
        val += s_number + "_in.txt"
        return val

    def generateOne(self, reg, specs):
        for val in specs:
            if (isinstance(val, list)):
                min, max = Specifier.findLimits(val[0], 0, 1000)
                cnt = random.randrange(int(min), int(max))
                vr = ""
                for i in range(cnt):
                    vr += self.generateOne(val[2], val[1])
                vr = vr.replace("$(", "").replace(f"){val[0]}$", "")
                val = val[2]
            else:
                fcn = getattr(Specifier, self.SPECS[val[-1]])
                vr = fcn(val) 
            index = reg.find(val)
            reg = reg[:index] + vr + reg[index + len(val):]
        return reg

    def generate(self, count=100):
        self.specsValues = self.findSpecs(self.reg)
        pth = "./SamplesPPT"

        if (os.path.exists(pth)):
            if (os.path.isdir(pth)):
                i = input(f"{pth} directory already exists. Do you want to continue? [y/n]: ")
                if (i != "y"): return 1
            else:
                print(f"{pth} already exists and it is not a directory.")
                return 1
        else:
            os.mkdir(pth)

        print(f"Generating {count} files...")
        self.printProgressBar(0, count, "Generating:", "Done:", length=50)
        for i in range(count):
            data = self.generateOne(self.reg, self.specsValues)
            with open(os.path.join(pth, self.getName(i, count)), "w") as f:
                f.write(data)
            self.printProgressBar(i+1, count, "Generating:", "Done:", length=50)

    def printProgressBar(self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()