#!/bin/sh
. /etc/init.d/tc-functions

# Workaround for https://github.com/boot2docker/boot2docker/issues/973
if [ ! -e /root/.shutdown_ran ]; then

    echo "${YELLOW}Running boot2docker shutdown script...${NORMAL}"

    /usr/local/etc/init.d/docker stop

    # Tar up persistence folders and save for next run
    echo "Saving persistence directories -------------------"
    tar czvf /root/scratch/var_lib_docker.tar /var/lib/docker/*
    tar czvf /root/scratch/var_lib_boot2docker.tar /var/lib/boot2docker/*

    # Tar up results and log files
    echo "Saving results -------------------"
    tar czvf /root/shared/results.tgz /root/shared/results/*

    touch /root/.shutdown_ran

fi

