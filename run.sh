#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
exec java -cp 'campusloop.jar:lib/*' campusloop.App
