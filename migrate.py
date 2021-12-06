import sys
import os
from urllib.request import urlopen

old_intermediary = "https://github.com/Legacy-Fabric/Legacy-Intermediaries/raw/master/legacy/mappings/{minecraft_version}.tiny"
new_intermediary = "https://github.com/Legacy-Fabric/Legacy-Intermediaries/raw/master/mappings/{minecraft_version}.tiny"

def migrate(version, mappingFolder):
    print("Downloading old intermediary...")
    o_i = urlopen(old_intermediary.replace("{minecraft_version}", version))
    o_i_file = str(o_i.read())
    print("Done")

    print("Downloading new intermediary...")
    n_i = urlopen(new_intermediary.replace("{minecraft_version}", version))
    n_i_file = str(n_i.read())
    print("Done")

    intermediary_map = create_intermediary_map(o_i_file, n_i_file)

    file_list = read_sub_folder(mappingFolder)

    lines = parse_file(file_list[1])

    lines = migrate_file(lines, intermediary_map)

    write_file(file_list[1], lines)

def write_file(path, lines):
    str_lines = []

    for line in lines:
        string = ""

        index = 0
        for i in line:
            if index < 1:
                string = i
            else:
                string += "\t" + i
            
            index += 1
        
        str_lines.append(string)
    
    file_str = ""

    for line in str_lines:
        if len(file_str) == 0:
            file_str = line
        else:
            file_str += "\n" + line

    with open(path, 'w') as f:
        f.write(file_str)
        f.close()

def migrate_file(content: list[list[str]], intermediary: dict):
    lines = []
    for line in content:
        startIndex = 0
        while len(line[startIndex]) < 1:
            startIndex+=1
        
        line_info = line[startIndex].split(" ")

        line_type = line_info[0]

        if line_type == "CLASS":
            line_info[1] = intermediary.get(line_info[1], line_info[1])
        elif line_type == "FIELD":
            line_info[1] = intermediary.get(line_info[1], line_info[1])

            field_type = line_info[3]

            if field_type.startswith("L"):
                field_type = field_type[1:len(field_type)-1]
                line_info[3] = "L" + intermediary.get(field_type, field_type) + ";"
            elif field_type.startswith("[L"):
                field_type = field_type[2:len(field_type)-1]
                line_info[3] = "[L" + intermediary.get(field_type, field_type) + ";"
        elif line_type == "METHOD":
            line_info[1] = intermediary.get(line_info[1], line_info[1])

            if not line_info[1] == "<init>":
                line_info[3] = method_info(line_info[3], intermediary)

        line_str = line_info[0]

        for info in line_info:
            if line_str == info:
                continue
            else:
                line_str += " " + info
        
        line[startIndex] = line_str

        lines.append(line)
    
    return lines

def method_info(info: str, intermediary: dict):
    args, r_type = info.split(")")

    args = args[1:]

    return info

def parse_file(path):
    with open(path, 'r') as f:
        content = f.read()
        lines = content.splitlines()
        f.close()
        parsed_lines = []

        for line in lines:
            parsed_lines.append(line.split("\t"))
        
        return parsed_lines

def read_sub_folder(path):
    path_list = []

    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)

        if os.path.isdir(filepath):
            path_list += read_sub_folder(filepath)
        elif os.path.isfile(filepath):
            path_list.append(filepath)
    
    return path_list

def create_intermediary_map(o_i, n_i):
    o_i_map = parse_intermediary(o_i)
    n_i_map = parse_intermediary(n_i)

    i_map = {}

    for o_line in o_i_map:
        for n_line in n_i_map:
            if o_line[0] == n_line[0]:
                i_map[o_line[1]] = n_line[1]
                break
    
    return i_map

def parse_intermediary(intermediary: str):
    i_map = []
    lines = intermediary.split("\\n")
    for line in lines:
        parts = line.split("\\t")
        name = ""
        
        if line.startswith("CLASS"):
            name = parts[2]
        elif line.startswith("FIELD"):
            name = parts[4]
        elif line.startswith("METHOD"):
            name = parts[4]
        else:
            continue
        
        line = line.replace("\\t" + name, "")

        i_map.append([line, name])
    
    return i_map

if __name__ == '__main__':
    migrate(sys.argv[1], sys.argv[2])