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
        commandList = [
            [GRADLE_PREFIX + " publishToMavenLocal unifyMappings", True], 
            ["cd test-mod && " + GRADLE_PREFIX + " build genSources", False]
            ]
    elif mainCommand == "publish":
        commandList = [
            [GRADLE_PREFIX + " publish unifyMappings", True]
            ]
    elif mainCommand == "buildPublishToLocalAndTest":
        commandList = [
            [GRADLE_PREFIX + " build javadocJar checkMappings mapNamedJar unifyMappings", True], 
            [GRADLE_PREFIX + " publishToMavenLocal unifyMappings", True], 
            ["cd test-mod && " + GRADLE_PREFIX + " build genSources", False]
            ]

    failedVersions = []

    for command in commandList:
        testedVersion = [version for version in versions if version not in failedVersions]
        print("Running command '" + command[0] + "' for versions " + ", ".join(testedVersion))

        for version in testedVersion:
            print("Running command for version " + version)
            exitCode = yarn.run_command_with_mcversion(version, command[0])

            if exitCode != 0:
                failedVersions.append(version)
                if command[1]:
                    break
    
    if len(failedVersions) < 1:
        exit(0)
    else:
        print("Command failed for versions: " + ", ".join(failedVersions))
        exit(1)

if __name__ == '__main__':
    main()