#!/bin/bash

if [ ! -n "$1" ] || [ "$#" -ne 1 ]; then
    echo "Usage: ./setup_versions <vboxwrapper-version>"
    echo "Downloads the vboxwrapper executables and sets up the app version folders."
    echo "See http://boinc.berkeley.edu/dl/ for the latest vboxwrapper version."
    exit
fi

cd apps/boinc2docker/1.0

if [ ! -f example/vm_isocontext.iso ]; then
    echo "Downloading boinc2docker ISO..."
    wget $(curl -s https://api.github.com/repos/marius311/boinc2docker/releases | grep browser_download_url | head -n 1 | cut -d '"' -f 4) -O example/vm_isocontext.iso
fi

for platform in x86_64-pc-linux-gnu windows_x86_64 x86_64-apple-darwin; do 
    cp -r example ${platform}__vbox64_mt &&
    cd ${platform}__vbox64_mt && 
    vboxwrapper=vboxwrapper_$1_${platform} && 
    if [[ $platform == "windows"* ]]; then vboxwrapper=${vboxwrapper}.exe; fi &&
    if [[ ! -f vboxwrapper_$1_${platform}.zip ]]; then
        wget http://boinc.berkeley.edu/dl/vboxwrapper_$1_${platform}.zip
    fi &&
    if [[ ! -f $vboxwrapper ]]; then
        files=$(unzip -j *.zip | grep inflating | awk '{print $NF}') &&
        rm ${files/$vboxwrapper/} *.zip
    fi &&
    sed -E -i "s/<physical_name>vboxwrapper<\/physical_name>/<physical_name>$vboxwrapper<\/physical_name>/g" version.xml &&
    cd ..
done
