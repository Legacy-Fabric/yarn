# Legacy Yarn

![Build](https://img.shields.io/github/actions/workflow/status/Legacy-Fabric/yarn/publish.yml?label=build&branch=master)
![Publish](https://img.shields.io/github/actions/workflow/status/Legacy-Fabric/yarn/publish.yml?label=publish&branch=master)

Legacy Yarn is a set of open, unencumbered Minecraft mappings, free for everyone to use under the Creative Commons Zero license. The intention is to let 
everyone mod Minecraft freely and openly, while also being able to innovate and process the mappings as they see fit.

## Usage

To use yarn-deobfuscated Minecraft for Minecraft modding or as a dependency in a Java project, you can use [loom](https://github.com/fabricmc/fabric-loom) Gradle plugin. See [fabric wiki tutorial](https://fabricmc.net/wiki/tutorial:setup) for more information.

To obtain a deobfuscated Minecraft jar, [`./gradlew mapNamedJar`](#mapNamedJar) will generate a jar named like `<minecraft version>-named.jar`, which can be sent to a decompiler for deobfuscated code.

Please note to run the yarn build script **Java 21** or higher is required!

## Contributing

Please remember that copying and pasting mappings from alternate projects under more restrictive licenses (such as MCP, Spigot's or Mojang's obfuscation maps)
is **completely forbidden** without explicit permission from the owners of said mappings to distribute the names under the CC0 license.
This includes using the names from those mappings for inspiration. Discussing the naming approaches used in said projects
is also not welcome - you have been warned. However, it is a good idea to consult name changes with other people - use pull requests or our community spaces to ask questions!

Please have a look at the [naming conventions](/CONVENTIONS.md) before submitting mappings.

### Getting Started

1. Fork and clone the repo
2. Run `py yarn.py enigma <minecraft version>` to open [Enigma](https://github.com/OrnitheMC/Enigma), a user interface to easily edit the mappings
3. Save your changes in Enigma and store them by running one of the following save tasks (`py yarn.py <task> <minecraft version>`):
    - `saveMappings`: propagate your changes up and down the version graph and save them to every applicable Minecraft version (this is most likely the task you want to use)
    - `insertMappings`: save your changes only to the specified Minecraft version
    - `saveMappingsDown`: propagate your changes down the version graph (to versions further away from the root (1.3.2)) and save them to every applicable Minecraft version
    - `saveMappingsUp`: propagate your changes up the version graph (to versions closer to the root (1.3.2)) and save them to every applicable Minecraft version
4. If you wish to continue working in Enigma, make sure to reload the mappings.
5. When you're done, commit and push your work to your fork
6. Open a pull request with your changes

#### NOTE

The `enigma` task loads the mappings for the specified version out into temporary files in the `/run/` folder. Enigma will read and write to these files, and the save tasks will use these files to save the mappings back into the version graph.

- DO NOT MANUALLY EDIT THESE FILES! You may corrupt the mappings!
- Running the `enigma` task **will** overwrite these files. If you have unsaved changes, make sure to run one of the save tasks **before** running the `enigma` task to open Enigma again!
- You can safely open multiple Enigma instances for *different* Minecraft versions. You **cannot** safely open multiple Enigma instances for *one* Minecraft version.

## Gradle
Legacy Yarn uses Gradle to provide a number of utility tasks for working with the mappings.

### `enigma`
Download and launch the latest version of [Enigma](https://github.com/OrnitheMC/Enigma) automatically configured to use the merged jar and the mappings.

Compared to launching Enigma externally, the gradle task adds a name guesser plugin that automatically map enums and a few constant field names.

### `build`
Build a GZip'd archive containing a tiny mapping between official (obfuscated), intermediary, and Legacy Yarn names ("named") and packages Tiny V1 mappings into a zip archive.

### `mapMinecraftToNamed`
Builds a deobfuscated jar with Legacy Yarn mappings and automapped fields (enums, etc.). Unmapped names will be filled with intermediary names.

### `decompileWithCfr`
Decompile the mapped source code with the CFR decompiler. **Note:** This is not designed to be recompiled.

### `decompileWithVineflower`
Decompile the mapped source code with the Vineflower decompiler. **Note:** This is not designed to be recompiled.

### `downloadMinecraftJars`
Downloads the client and server Minecraft jars for the current Minecraft version to `/lf-keratin/gen2/game-jars/` in your user gradle cache.

### `mergeMinecraftJars`
Merges the client and server jars into one merged jar, located at `/lf-keratin/gen2/game-jars/<minecraft_version>-merged.jar` in your user gradle cache.