#!/usr/bin/env python3

from typing import NamedTuple
import urllib.request as request
import shutil
import os


URL = "https://github.com/Legacy-Fabric/Legacy-Intermediaries/raw/master/mappings/{}.tiny"

class Intermediaries(NamedTuple):
    classes: dict # { offical name, class }
    fields: dict  # { field, signature }
    methods: dict # { method, signature }

def seperate(minecraft_version: str, try_merge: bool=True):
    if try_merge and os.path.isdir("mappings-active"):
        print("> Found leftover mappings, Merging!")
        merge()

    print("> Seperating mappings for {}..".format(minecraft_version))
    with request.urlopen(URL.format(minecraft_version)) as response:
        intermediary_data = response.read().decode('utf-8')
        mappings = parse_intermediary(intermediary_data.splitlines()[1:])

        os.makedirs("./mappings-active", exist_ok=True)
        with open("./mappings-active/{}.tiny".format(minecraft_version), "w") as f:
            f.write(intermediary_data)

    for folder, dirs, files in os.walk("./mappings"):
        for fname in files:
            if fname.endswith(".mapping"):
                seperate_file(folder, fname, mappings)

def merge(delete: bool=True):
    for file in os.listdir("./mappings-active"):
        if file.endswith(".tiny"):
            print("> Merging mappings for {}..".format(file[:-5]))
            with open("./mappings-active/" + file, 'r') as file:
                mappings = parse_intermediary(file.read().splitlines()[1:])
                break

    class_map = create_class_map()
    for folder, dirs, files in os.walk("./mappings-active"):
        for fname in files:
            if fname.endswith(".mapping"):
                merge_file(folder, fname, mappings, class_map)

    if delete:
        shutil.rmtree("./mappings-active")

# Intermediary Utilities

def parse_intermediary(intermediary_lines: list):
    itm = Intermediaries({}, {}, {})

    for line in intermediary_lines:
        if "#" in line:
            continue

        parts = line.split("	")
        if parts[0] == "CLASS":
            itm.classes[parts[1]] = parts[2]
        elif parts[0] == "FIELD":
            itm.fields[parts[4]] = parts[2]
        else:
            itm.methods[parts[4]] = parts[2]

    for f, d in itm.fields.items():
        itm.fields[f] = remap_signature(d, itm.classes)

    for m, d in itm.fields.items():
        itm.methods[m] = remap_signature(m, itm.classes)

    return itm

def remap_signature(signature: str, classes: dict):
    if not ";" in signature:
        return signature

    new_sig = ""
    mnt = ""
    mnted = False
    for i in signature:
        if mnted:
            if i == ";":
                if mnt in classes.keys():
                    mnt = classes[mnt]
                new_sig = new_sig + mnt + ";"
                mnted = False
            else:
                mnt = mnt + i
        else:
            if i == "L":
                mnted = True
                mnt = ""
            new_sig = new_sig + i

    return new_sig

# Seperating Utilities

def seperate_file(folder: str, fname: str, mappings: Intermediaries):
    new_content = ""
    with open(os.path.join(folder, fname), 'r') as file:
        tabs = 0
        for line in file.read().splitlines():
            new_tabs = line.count("	")
            if new_tabs > tabs:
                continue
            elif new_tabs < tabs:
                tabs = new_tabs

            if is_in_mappings(line, mappings):
                new_content += line + "\n"
                tabs += 1

        if new_content != "":
            new_fname = os.path.join(folder.replace("mappings", "mappings-active", 1), fname)
            os.makedirs(os.path.dirname(new_fname), exist_ok=True)
            with open(new_fname, "w", newline="\n") as f:
                f.write(new_content)

def is_in_mappings(line: str, mappings: Intermediaries, inc_other: bool=True):
    split = line.replace("	", "").split()
    return ((split[0] == "CLASS" and any(cls.endswith(split[1]) for cls in mappings.classes.values()))
        or (split[0] == "FIELD" and split[1] in mappings.fields and split[-1] == mappings.fields[split[1]])
        or (split[0] == "METHOD" and (split[1] == "<init>" or (split[1] in mappings.methods and split[-1] == mappings.methods[split[1]])))
        or (inc_other and (split[0] == "ARG" or split[0] == "COMMENT")))

# Merging Utilities

def create_class_map():
    class_map = {}
    for folder, dirs, files in os.walk("./mappings"):
        for fname in files:
            if fname.endswith(".mapping"):
                path = os.path.join(folder, fname)
                with open(path, 'r') as file:
                    parts = file.readline().rstrip().split()

                class_map[parts[1].split("/")[-1]] = path

    return class_map

def merge_file(folder: str, fname: str, mappings: Intermediaries, class_map: dict):
    path = os.path.join(folder, fname)
    with open(path, 'r') as file:
        lines = file.read().splitlines()
        i_class = lines[0].split()[1].split("/")[-1]
        new_path = os.path.normpath(path.replace("mappings-active", "mappings", 1))

        # Step 1: Rename/create the file we're moving the mappings into
        if os.path.normpath(class_map[i_class]) != new_path:
            while os.path.isfile(new_path):
                new_path = new_path[:-8] + "$.mapping"

            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            os.rename(class_map[i_class], new_path)
            class_map[i_class] = new_path

        with open(new_path, 'r') as new_file:
            new_lines = new_file.read().splitlines()

        if "CLASS" not in new_lines[0]:
            new_lines = [ lines[0] ]

        # Step 2: Rename existing classes/subclasses
        # (We wait with classes that don't exist until step 4 since its more convenient there,
        #  technically this doesn't handle deleting subclasses but there aren't really
        #  any cases where would need to do that)
        for i in range(len(lines)):
            split = lines[i].replace("	", "").split()
            if split[0] == "CLASS":
                ni = indexof(new_lines, "CLASS " + split[1])
                if ni != -1:
                    insert_mapping(lines, new_lines, i, ni, True)

        # Step 3: Delete fields and methods that are in the current intermediaries before merging them
        i = 1
        tabs = 1
        while i < len(new_lines):
            new_tabs = new_lines[i].count("	")
            if new_tabs > tabs:
                i += 1
                continue
            elif new_tabs < tabs:
                tabs = new_tabs

            if is_in_mappings(new_lines[i], mappings, False):
                count = get_mapping_length(new_lines, i)
                if "	CLASS" not in new_lines[i]:
                    for _ in range(count):
                        new_lines.pop(i)
                else:
                    i += count
                tabs += count
            else:
                i += 1

        # Step 4: Readd fields, methods and classes from the active file
        parent_classes = []
        for i in range(len(lines)):
            split = lines[i].replace("	", "").split()
            if split[0] == "CLASS" or split[0] == "FIELD" or split[0] == "METHOD":
                if split[0] == "CLASS":
                    parent_classes = parent_classes[:lines[i].count("	")]
                    if indexof(new_lines, "CLASS " + split[1]) != -1:
                        parent_classes.append(split[1])
                        continue

                ni = indexof(new_lines, "CLASS " + parent_classes[-1]) + 1
                while ni < len(new_lines) and not cmp_mapping(lines[i], new_lines[ni]):
                    ni += 1
                insert_mapping(lines, new_lines, i, ni, False)

                if split[0] == "CLASS":
                    parent_classes.append(split[1])

        with open(new_path, "w+", newline="\n") as new_file:
            new_file.write("\n".join(new_lines) + "\n")

def insert_mapping(from_lines: list, to_lines: list, from_index: int, to_index: int, replace: bool):
    if replace:
        for i in range(get_mapping_length(to_lines, to_index)):
            to_lines.pop(to_index)

    for i in range(get_mapping_length(from_lines, from_index)):
        to_lines.insert(to_index + i, from_lines[from_index + i])

def get_mapping_length(lines: list, index: int):
    count = 1
    while index + 1 < len(lines):
        index += 1
        line = lines[index].replace("	", "")
        if not line.startswith("ARG") and not line.startswith("COMMENT"):
            break
        count += 1

    return count

# Returns the first line while contains this string
def indexof(lines: list, string: str):
    for i in range(len(lines)):
        if string in lines[i]:
            return i

    return -1

# Returns whether line1 should be before line2
def cmp_mapping(line1: str, line2: str):
    sline1 = line1.replace("	", "")
    sline2 = line2.replace("	", "")
    if len(line1) - len(sline1) > len(line2) - len(sline2):
        return True

    if len(line1) - len(sline1) < len(line2) - len(sline2) or sline2.startswith("COMMENT"):
        return False

    if sline1.startswith("CLASS"):
        return sline2.startswith("CLASS") and sline2 > sline1

    if sline2.startswith("CLASS"):
        return True

    return sline2 > sline1

# class Yarn(NamedTuple):
#     mtype: str
#     intermediary: str
#     yarn: str
#     signature: str
# 
#     comments: list#<str>
#     args: list#<Yarn>
#     classes: list#<Yarn>
#     fields: list#<Yarn>
#     methods: list#<Yarn>

# def parse_yarn(lines: list, tabs: int=0):
#     split = lines.pop(0).replace("	", "").split()
#     mapping = Yarn(split[0], split[1],
#                       None if len(split) == 2 or (len(split) == 3 and split[0] != "ARG") else split[2],
#                       None if split[0] != "FIELD" and split[0] != "METHOD" else split[-1],
#                       [], [], [], [], [])
# 
#     while len(lines) > 0 and "	COMMENT" in lines[0]:
#         mapping.comments.append(lines.pop(0).replace("	", "").replace("COMMENT ", "", 1))
# 
#     if split[0] == "CLASS":
#         while len(lines) > 0 and lines[0].count("	") > tabs:
#             m = parse_yarn(lines, tabs + 1)
#             if m.mtype == "CLASS": mapping.classes.append(m)
#             elif m.mtype == "FIELD": mapping.fields.append(m)
#             elif m.mtype == "METHOD": mapping.methods.append(m)
#             else: print("uh oh")
#     elif split[0] == "METHOD":
#         while len(lines) > 0 and "	ARG" in lines[0]:
#             mapping.args.append(parse_yarn(lines, tabs + 1))
# 
#     return mapping

