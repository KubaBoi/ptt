
import os

class Builder:

    @staticmethod
    def build(file, output):
        dir_name = os.path.dirname(file)
        output = os.path.join(dir_name, output)
        if (output == file): 
            print("")
            return 0

        with open(file, "r", encoding="utf-8") as f:
            data_lines = f.readlines()

        includes = []
        done_includes = []
        content = ""
        new_data = "$INCLUDES$\n"
        for line in data_lines:
            if (line.lower().startswith("#include")):
                parts = line.split("\"")
                if (len(parts) != 3): 
                    includes.append(line)
                    continue

                if (line in done_includes): continue

                header_name = parts[1]
                cont = Builder.openHeader(dir_name, header_name, done_includes)
                if (content == 0): 
                    includes.append(line)
                    continue
                done_includes.append(line)
                new_data += cont[0] + "\n"

                for incl in cont[1]:
                    if (incl not in includes): includes.append(incl)
            else:
                new_data += line

        includesString = ""
        for incl in includes:
            includesString += incl

        with open(output, "w", encoding="utf-8") as f:
            f.write(new_data.replace("$INCLUDES$", includesString))

        return output

    @staticmethod
    def openHeader(dir_name, header_name, done_includes):
        if (not header_name.endswith(".h") or
            not os.path.exists(os.path.join(dir_name, header_name))): 
            return 0

        content = ""

        src_name = header_name[:-1] + "c"
        hasSrc = os.path.exists(os.path.join(dir_name, src_name))

        with open(os.path.join(dir_name, header_name), "r", encoding="utf-8") as f:
            header_lines = f.readlines()
        
        includes = []
        for line in header_lines:
            if (line.lower().startswith("#include")):
                parts = line.split("\"")
                if (len(parts) != 3): 
                    includes.append(line)
                    continue

                if (line in done_includes): continue

                hdr_name = parts[1]
                cont = Builder.openHeader(dir_name, hdr_name, done_includes)
                if (content == 0): 
                    includes.append(line)
                    continue
                done_includes.append(line)
                content += cont[0] + "\n"

                for incl in cont[1]:
                    if (incl not in includes): includes.append(incl)
            elif (line.lower().startswith("#define") or not hasSrc):
                content += line
                

        content += "\n"
        if (hasSrc):
            with open(os.path.join(dir_name, src_name), "r", encoding="utf-8") as f:
                data_lines = f.readlines()

            for line in data_lines:
                if (not line.lower().startswith("#include")):
                    content += line

        return [content, includes]
        



