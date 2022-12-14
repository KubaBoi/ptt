
import random
import math
import string

class InvalidRegex(Exception):
    def __init__(self, description):
        super().__init__(self, "Invalid regex", description)

class Specifier:

    @staticmethod
    def findLimits(val, min, max):
        limits = val.split(",")
        if (val != ""):
            if (len(limits) == 1):
                min = 0
                max = float(limits[0])
            else:
                min = float(limits[0])
                max = float(limits[1])
        return min, max

    @staticmethod
    def char(val):
        val = val.replace("%", "").replace("c", "")
        return random.choice(string.ascii_letters)

    @staticmethod
    def decimal(val):
        val = val.replace("%", "").replace("d", "")
        min, max = Specifier.findLimits(val, -32768, 32768)

        return str(random.randrange(int(min), int(max)))

    @staticmethod
    def string(val):
        val = val.replace("%", "").replace("s", "")
        min, max = Specifier.findLimits(val, -1, 100)

        if (min != -1):
            length = random.randrange(int(min), int(max))
        else:
            length = max

        return "".join(random.choices(string.ascii_letters + string.digits,
                k=length))

    @staticmethod
    def double(val):
        val = val.replace("%", "").replace("g", "")
        min, max = Specifier.findLimits(val,
            2.3*math.pow(10, -308),
            1.7*math.pow(10, 308))
        
        return str(random.uniform(min, max))

    @staticmethod
    def flt(val):
        val = val.replace("%", "").replace("f", "")
        min, max = Specifier.findLimits(val,
            1.2*math.pow(10, -38),
            3.4*math.pow(10, 38))
        
        return str(random.uniform(min, max))

    @staticmethod
    def octa(val):
        val = val.replace("%", "").replace("o", "")
        s = Specifier.decimal(val)
        return oct(int(s))

    @staticmethod
    def unsigned(val):
        val = val.replace("%", "").replace("u", "")
        min, max = Specifier.findLimits(val, 0, 65536)

        if (min < 0): min = 0

        return str(random.randrange(int(min), int(max)))

    @staticmethod
    def hexa(val):
        val = val.replace("%", "").replace("x", "")
        s = Specifier.decimal(val)
        return hex(int(s))

    @staticmethod
    def hexA(val):
        val = val.replace("%", "").replace("X", "")
        s = Specifier.decimal(val)
        return hex(int(s)).upper()

