#! /bin/bash

SRC=posts
PUBLIC=public

python3 -m http.server -d .build &

http_pid=$!

trap cleanup INT

function cleanup() {
    echo "Stop local server"
    kill $http_pid
}

inotifywait -e modify,moved_to,create --format '%f' -m -r "$SRC" "$PUBLIC" | \
    while read -r filename; do
        if [[ "$filename" != .#* ]]; then
            ./build.py
        fi
    done

echo ok
