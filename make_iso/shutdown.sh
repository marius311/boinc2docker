#!/bin/sh
. /etc/init.d/tc-functions

# Workaround for https://github.com/boot2docker/boot2docker/issues/973
if [ ! -e /root/.shutdown_ran ]; then

    echo "${YELLOW}Running boot2docker shutdown script...${NORMAL}"

    /usr/local/etc/init.d/docker stop

    # Tar up persistence folders and save for next run
    (echo "Saving persistence directories..." ;
     tar cf /root/scratch/boinc2docker_persistence.tar /var/lib/docker/* /var/lib/boot2docker/*) 2&>1 | tee -a /root/shared/results/boot2docker.log

    # Tar up results and log files
    echo "Saving results..."
    (cd /root/shared/results && tar czvf /root/shared/results.tgz *)

    # Alert BOINC of the exit status
    cp /root/shared/boinc_app_exit_status /root/shared/completion_trigger_file


    touch /root/.shutdown_ran

fi

