import sys
import os


HELP_STR = """Syntax:
    python ./start.py action mcVersion metaUrl
Example:
    python ./start.py yarn 1.8.9
    python ./start.py yarn 1.7.10 https://meta.legacyfabric.net
    python ./start.py publishlocal 1.8.9"""

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
    if action == 'yarn':
        os.environ['MC_VERSION'] = version
        if os.name == 'nt':
            os.system('gradlew.bat yarn')
        else:
            os.system('gradlew yarn')
    elif action == 'publishlocal':
        os.system('python ./prepare_yarn.py ' + version)
        os.system('gradlew publishToMavenLocal --stacktrace')

if __name__ == '__main__':
    main()