@echo off
SETLOCAL
set mc_versions=1.3.2 1.4.7 1.5 13w11a 1.5.1 2point0_red 2point0_purple 2point0_blue 1.5.2 1.6.4 1.7.2 1.7.10 1.8 15w14a 1.8.9 1.9.4 1.10.2 1.11.2 1.12.2 1.13.2
echo Available MC versions: %mc_versions%

:versionselect
set /p version="Enter the version you want to edit: "

set valid="F"
for %%i in (%mc_versions%) do (
    if %%i == %version% set valid="T"
)

if %valid% == "F" (
    echo Invalid MC version!
    goto versionselect
)

ENDLOCAL & (
    set MC_VERSION=%version%
)

echo Starting Gradle with MC version %MC_VERSION%...

./gradlew.bat yarn
