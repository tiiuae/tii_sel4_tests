#/usr/bin/env bash

docker run --restart always -d -p 20408:20408 -v /home/crossbar/.crossbar/:/app/.crossbar
