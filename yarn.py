import sys
import os


VERSIONS = ['1.3.2', '1.4.7', '1.5', '13w11a', '1.5.1', '2point0_red', '2point0_purple', '2point0_blue', '1.5.2', '1.6.4', '1.7.2', '1.7.10', '1.8', '15w14a', '1.8.9', '1.9.4', '1.10.2', '1.11.2', '1.12.2', '1.13.2']
ACTIONS = ['edit', 'publish']
HELP_STR = f"""Syntax:
    python ./start.py ({"|".join(ACTIONS)}) mcVersion metaUrl?
Values:
    edit: Opens enigma with the given version.
    publish: Publishes the mappings locally,
             access this version by putting "local"
             instead of a date in your gradle.properties
             and adding mavenLocal() to your repositories block
             in your build.gradle.
    mcVersion: The Minecraft version to use.
    metaUrl: The meta url if you're using a custom meta server.
Examples:
    python ./yarn.py edit 1.8.9
    python ./yarn.py edit 1.7.10 https://meta.legacyfabric.net
    python ./yarn.py publish 1.8.9"""

def main():
    args = sys.argv

    # Manual mode
    if len(args) <= 1:
        print("Enter the action you want to perform")
        print("Available actions: " + ", ".join(ACTIONS))
        while True:
            action = input("> ")
            if action.lower() in ACTIONS:
                break
            print(".. Invalid action")

        print("Enter the Minecraft version you want to use")
        print("Available versions: " + ", ".join(VERSIONS))
        while True:
            version = input("> ")
            if version.lower() in VERSIONS:
                break
            print(".. Invalid version")
    # Argument mode
    else:
        if args[0] in ["--help", "-h"]:
            print(HELP_STR)
            return
        if len(args) < 2:
            print("Action wasn't specified, input should look like")
            print(HELP_STR)
            return
        if len(args) < 3:
            print("Version wasn't specified, input should look like:")
            print(HELP_STR)
            return
        action = args[1]
        version = args[2]
        if len(args) == 4:
            os.environ['LEGACY_FABRIC_META_URL'] = args[3]

    if action == 'edit':
        os.environ['MC_VERSION'] = version
        os.system('gradlew yarn')
    elif action == 'publish':
        os.system('python ./prepare_yarn.py ' + version)
        os.system('gradlew publishToMavenLocal --stacktrace')

if __name__ == '__main__':
    main()
