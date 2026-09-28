[app]
title = Asistencia
package.name = asistencia
package.domain = org.secretaria
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0
requirements = python3,kivy,jsonstore
orientation = portrait
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1

[android]
api = 31
minapi = 21
ndk_api = 21
archs = arm64-v8a, armeabi-v7a
permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.enable_androidx = True

[p4a]
bootstrap = sdl2