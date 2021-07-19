#! /bin/bash

SRC=posts
PUBLIC=public
TEMPLATES=templates

python3 -m http.server -d .build &

http_pid=$!

trap cleanup INT

function cleanup() {
    echo "Stop local server"
    kill $http_pid
}

./build.py
inotifywait -e modify,moved_to,create --format '%f' -m -r "$SRC" "$PUBLIC" "$TEMPLATES" | \
    while read -r filename; do
        if [[ "$filename" != .\#* && "$filename" != \#*\# ]]; then
            ./build.py
        fi
    done
