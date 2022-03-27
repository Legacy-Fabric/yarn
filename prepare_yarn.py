#!/usr/bin/env python3

import urllib.request as request
import os
import sys

url = "https://github.com/Legacy-Fabric/Legacy-Intermediaries/raw/master/mappings/{}.tiny"

def prepare():
    minecraft_version = sys.argv[1]

    with request.urlopen(url.format(minecraft_version)) as response:
        intermediary_str = response.read().decode('utf-8').splitlines()
        intermediary_str.pop(0)
        mappings = parse_intermediary(intermediary_str)

        for i in os.listdir("./mappings"):
            remap("./mappings", i, mappings)

def remap(path: str, part: str, mappings: dict):
    if ".mapping" in part:
        remap_file(path + "/" + part, mappings)
    else:
        path = path + "/" + part
        for i in os.listdir(path):
            remap(path, i, mappings)

def remap_file(path: str, mappings: dict):
    with open(path, 'r') as m_file:
        lines = m_file.read().splitlines()
        class_name = lines[0].split(" ")[1]
        
        m_file.close()

        if not class_name in mappings.keys():
            os.remove(path)
        else:
            new_lines = []

            class_infos = mappings[class_name]
            fields_infos = class_infos["fields"]

            for i in lines:
                parts = i.split(" ")
                header = parts[0].split("	")

                if len(header) > 2 or len(header) == 0:
                    new_lines.append(i)
                elif parts[0].endswith("FIELD") and parts[1] in fields_infos.keys():
                    if (len(parts) == 3 and parts[2] == fields_infos[parts[1]]) or parts[3] == fields_infos[parts[1]]:
                        new_lines.append(i)
                elif not parts[0].endswith("FIELD"):
                    new_lines.append(i)
            new_str = new_lines.pop(0)

            for i in new_lines:
                new_str = new_str + "\n" + i
            
            with open(path, 'w') as m_write:
                m_write.write(new_str)
                m_write.close()


def parse_intermediary(intermediary):
    classes = {}
    field = {}
    method = {}

    for line in intermediary:
        if "#" in line:
            break
        parts = line.split("	")

        if parts[0] == "CLASS":
            classes[parts[1]] = parts[2]
            field[parts[1]] = {}
            method[parts[1]] = {}
        elif parts[0] == "FIELD":
            field[parts[1]][parts[3]] = [parts[4], parts[2]]
        else:
            method[parts[1]][parts[3]] = [parts[4], parts[2]]
    
    mappings = {}

    for i in classes:
        mappings[classes[i]] = {
            "fields": {}, "methods": {}
        }
    
    for i in field:
        for j in field[i]:
            descriptor = field[i][j][1]
            mappings[classes[i]]["fields"][field[i][j][0]] = remap_descriptor(descriptor, classes)
    
    for i in method:
        for j in method[i]:
            descriptor = method[i][j][1]
            mappings[classes[i]]["methods"][method[i][j][0]] = remap_descriptor(descriptor, classes)
    
    return mappings

def remap_descriptor(descriptor: str, classes: dict):
    if ";" in descriptor:
        chrs = ""
        mnt = ""
        mnted = False
        for i in descriptor:
            if mnted:
                if i == ";":
                    if mnt in classes.keys():
                        mnt = classes[mnt]
                    chrs = chrs + mnt + ";"
                    mnted = False
                else:
                    mnt = mnt + i
            else:
                if i == "L":
                    mnted = True
                    mnt = ""
                chrs = chrs + i
        
        descriptor = chrs
    
    return descriptor

if __name__ == '__main__':
    prepare()