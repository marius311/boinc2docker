#!/bin/bash

if [ ! -n "$1" ] || [ "$#" -ne 1 ]; then
    echo "Usage: ./cp2boinc <boinc project dir>"
    exit
fi

cp -rf apps apps_boinc2docker templates $1
