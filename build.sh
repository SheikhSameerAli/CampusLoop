#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
rm -rf build/classes
mkdir -p build/classes
java -m jdk.compiler/com.sun.tools.javac.Main --release 17 -encoding UTF-8 -d build/classes src/campusloop/*.java
cp -R web build/classes/web
java -m jdk.jartool/sun.tools.jar.Main --create --file campusloop.jar --main-class campusloop.App -C build/classes .
echo 'Built campusloop.jar'
