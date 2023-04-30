#!/usr/bin/env python3

import threading
import time
import os
import sys
sys.dont_write_bytecode = True

from intermediary_helper import separate, merge


VERSIONS = ['1.3.2', '1.4.7', '1.5', '13w11a', '1.5.1', '2point0_red', '2point0_purple', '2point0_blue', '1.5.2', '1.6.4', '1.7.2', '1.7.10', '1.8', '15w14a', '1.8.9', '1.9.4', '1.10.2', '1.11.2', '1.12.2', '1.13.2']
GRADLE_PREFIX = "gradlew.bat" if os.name == "nt" else "./gradlew"
saving_thread = None
kill = False

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

    os.environ["MC_VERSION"] = version
    separate(version)

    if command.startswith("yarn"):
        start_autosave()

    exitCode = os.system(GRADLE_PREFIX + " " + command)

    stop_autosave()
    merge()

    if exitCode == 0:
        exit(0)
    else:
        exit(1)

def start_autosave():
    global kill, saving_thread
    saving_thread = threading.Thread(target=_autosave)
    saving_thread.setDaemon(True)
    saving_thread.start()

def _autosave():
    # Automerge every 4 minutes
    while True:
        for i in range(480):
            if kill:
                return
            time.sleep(0.5)
        merge(False)

def stop_autosave():
    global kill, saving_thread
    kill = True
    while saving_thread != None and saving_thread.is_alive():
        time.sleep(0.5)

if __name__ == '__main__':
    main()
