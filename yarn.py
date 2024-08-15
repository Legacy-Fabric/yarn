#!/usr/bin/env python3

import os
import sys

sys.dont_write_bytecode = True

VERSIONS = ['15w14a', '1.8.2', '1.8.3', '1.8.4', '1.8.5', '1.8.6', '1.8.7', '1.8.8', '1.8.9',
            '1.9', '1.9.1', '1.9.2', '1.9.3', '1.9.4', '1.10', '1.10.1', '1.10.2',
            '1.RV-Pre1', '1.11', '1.11.1', '1.11.2', '1.12',  '1.12.1', '1.12.2',
            '1.13', '1.13.1', '1.13.2']
GRADLE_PREFIX = "gradlew.bat" if os.name == "nt" else "./gradlew"


def main():
    args = sys.argv

    # Manual mode
    if len(args) <= 1:
        print("Enter the Minecraft version you want to use")
        # print("Available versions: " + ", ".join(VERSIONS))
        while True:
            version = input("> ")
            # if version.lower() in VERSIONS:
            break
            # print(".. Invalid version")

        print("Enter the Gradle command you want to run")
        print("('yarn' to open Enigma)")
        command = input("> ")
    # Argument mode
    else:
        if len(args) <= 2:
            print("Invalid Syntax!")
            print("Syntax:")
            print("    python ./yarn.py {mc version} {gradle command}")
            return

        version = args[1]
        command = " ".join(args[2:])

    exit_code = run_command_with_mcversion(version, GRADLE_PREFIX + " " + command + " unifyMappings")

    if exit_code == 0:
        exit(0)
    else:
        exit(1)

def run_command_with_mcversion(version: str, command: str) -> int:
    os.environ["MC_VERSION"] = version
    return os.system(command)

if __name__ == '__main__':
    main()
