[app]
title = Stop smoking
package.name = stopsmoking
package.domain = org.esmajic
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_dirs = buildozer-e
version = 1.0.0
requirements = python3,kivy,kivymd,python.dateutil,Pillow
orientation = portrait
fullscreen = 1

# Target Android 13
android.api = 33
android.minapi = 27
android.ndk = 25b
android.ndk_api = 27
android.arch = armeabi-v7a

android.allow_backup = False
android.enable_androidx = True
android.use_android_native_activity = False
android.logcat_filters = *:S python:D
android.entrypoint = org.kivy.android.PythonActivity
android.build_type = debug
android.debug = 1
android.release = 0
android.new_layout = True
android.support = True

android.gradle_version = 7.5

#android.presplash = assets/presplash.png
#android.icon = assets/icon.png

[buildozer]
log_level = 2
warn_on_root = 1

