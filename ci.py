#!/usr/bin/env python3

import os
import sys
import yarn

sys.dont_write_bytecode = True

GRADLE_PREFIX = "gradlew.bat" if os.name == "nt" else "./gradlew"

def main():
    args = sys.argv

    versions = args[1].split(",")
    mainCommand = args[2]

    commandList = []
    if mainCommand == "publishToLocalAndTest":
        commandList = [GRADLE_PREFIX + " publishToMavenLocal unifyMappings", "cd test-mod && " + GRADLE_PREFIX + " build genSources"]
    elif mainCommand == "publish":
        commandList = [GRADLE_PREFIX + " publish unifyMappings"]

    failedVersions = []

    for command in commandList:
        testedVersion = [version for version in versions if version not in failedVersions]
        print("Running command '" + command + "' for versions " + ", ".join(testedVersion))

        for version in testedVersion:
            print("Running command for version " + version)
            exitCode = yarn.run_command_with_mcversion(version, command)

            if exitCode != 0:
                failedVersions.append(version)
    
    if len(failedVersions) < 1:
        exit(0)
    else:
        print("Command failed for versions: " + ", ".join(failedVersions))
        exit(1)

if __name__ == '__main__':
    main()