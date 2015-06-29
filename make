#!/bin/bash

docker build -t boinc2docker .
docker run --rm boinc2docker > app/vm_isocontext.iso
