#!/bin/sh
# Do all the VBox app necessary stuff, run our BOINC app, then shut down

echo "${YELLOW}Running BOINC app...${NORMAL}"

#mount shared folder
mkdir -p /root/shared
mount -t vboxsf shared /root/shared
cd /root/shared

#if these are tgz files, untar them
#ok if this fails
tar zxvf boinc_app
tar zxvf params

#where the app will put results
mkdir results

#run the app
chmod +x boinc_app
./boinc_app

#tar up any results
tar czvf results.tgz results/*


echo "${YELLOW}Finished BOINC app...${NORMAL}"

shutdown -h now
