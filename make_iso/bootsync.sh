#!/bin/sh
. /etc/init.d/tc-functions

# Mount shared folder ASAP so most of logging can be sent back to the host
echo "Mounting BOINC shared/ and scratch/..."
modprobe vboxguest; modprobe vboxsf
mkdir -p /root/shared /root/scratch
mount -t vboxsf shared /root/shared/ 
mount -t vboxsf scratch /root/scratch/ 
mkdir -p /root/shared/results


echo "${YELLOW}Running boot2docker init script...${NORMAL}"

# Log to shared folder on the host
/opt/bootscript.sh 2>&1 | tee -a /root/shared/results/boot2docker.log

echo "${YELLOW}Finished boot2docker init script...${NORMAL}"
