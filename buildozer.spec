[app]

# (str) Title of your application
title = PuffControl

# (str) Package name
package.name = puffcontrol

# (str) Package domain (needed for android/ios packaging)
package.domain = org.pufless

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to include no files)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to include no directories)
#source.exclude_dirs = tests, bin, venv, .buildozer

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,kivymd

# (str) Custom source folders for requirements
# Sets custom source for any requirement with recipes
# requirements.source.kivy = ../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = MyServiceName:subsplash.py

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the named colors (Red, Green, Blue, etc.)
#android.presplash_color = #12141C

# (list) Permissions
android.permissions = VIBRATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 33

# (str) Android NDK version to use
#android.ndk = 25b

# (bool) Use --private data dir (True), or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip python build and only run android packaging step
#p4a.source_build = False

# (str) Python for android branch to use, defaults to master
#p4a.branch = master

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= parameter to the mscore command line
# (WIP for android NDK with webview bootstrap)
#web_port =

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = false, 1 = true)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab. etc) storage
# bin_dir = ./bin
