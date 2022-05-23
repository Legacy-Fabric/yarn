import sys
import os


VERSIONS = ['1.3.2', '1.4.7', '1.5', '13w11a', '1.5.1', '2point0_red', '2point0_purple', '2point0_blue', '1.5.2', '1.6.4', '1.7.2', '1.7.10', '1.8', '15w14a', '1.8.9', '1.9.4', '1.10.2', '1.11.2', '1.12.2', '1.13.2']
HELP_STR = f"""Syntax:
    python ./start.py (edit|publish) mcVersion metaUrl?
Example:
    python ./yarn.py edit 1.8.9
    python ./yarn.py edit 1.7.10 https://meta.legacyfabric.net
    python ./yarn.py publish 1.8.9
Valid Versions: {", ".join(VERSIONS)}
Explanation:
    edit: opens enigma with the given version
    publish: publishes the mappings locally,
             access this version by putting "local"
             instead of a date in your gradle.properties
             and make sure you add mavenLocal() to your repositories block
             in your build.gradle"""

def main():
    args = sys.argv
    if len(set(["--help", "-h"]) & set(args))>0:
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
        if version not in VERSIONS:
            print("Invalid MC version!")
            print("Pick one of " + ", ".join(VERSIONS))
            return
        os.environ['MC_VERSION'] = version
        if os.name == 'nt':
            os.system('gradlew.bat yarn')
        else:
            os.system('gradlew yarn')
    elif action == 'publish':
        os.system('python ./prepare_yarn.py ' + version)
        os.system('gradlew publishToMavenLocal --stacktrace')

if __name__ == '__main__':
    main()
