#!/bin/sh
# Do all the VBox app necessary stuff, run our BOINC app, then shut down

echo "${YELLOW}Running BOINC app...${NORMAL}"

#mount shared folder
mkdir -p /root/shared
mount -t vboxsf shared /root/shared
cd /root/shared

#any tgz files in this folder are considererd inputs
#this will include the code to run the app itself, as well as any "parameters"
tar zxvf *.tgz

#where the app will put results
mkdir results

#run the app
./boinc_app

#tar up any results
tar czvf results.tgz results/*


echo "${YELLOW}Finished BOINC app...${NORMAL}"

shutdown -hP now
