#!/bin/bash

docker build -t boinc2docker make_iso
docker run --rm boinc2docker > apps/boinc2docker/1.0/x86_64-pc-linux-gnu/vm_isocontext.iso
