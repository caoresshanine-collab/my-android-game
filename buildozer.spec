[app]
title = My Mobile Game
package.name = mygame
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,sdl2,sdl2_image,sdl2_mixer,sdl2_ttf
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.api = 34
android.minapi = 21
android.build_tools_version = 34.0.0
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = 1

[buildozer]
log_level = 2
warn_on_root = 1
