#!/bin/sh
. /etc/init.d/tc-functions

# Separate function so we can more easily pipe this entire output to log file
run_showdown() {

    echo "${YELLOW}Running boot2docker shutdown script...${NORMAL}"
    /usr/local/etc/init.d/docker stop

    # Tar up persistence folders and save for next run
    # Save RAM by creating the tar file directly on the host computer via the shared folder
    # Make the operation as atomic as possible by creating a temporary tar first, then moving it inplace
    echo "Saving persistence directories..."
    UUID=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 32 | head -n 1)
    tar cf /root/scratch/boinc2docker_persistence_$UUID.tar /var/lib/docker/* &&
    mv /root/scratch/boinc2docker_persistence_$UUID.tar /root/scratch/boinc2docker_persistence.tar

    # Tar up results and log files
    echo "Saving results..."
    (cd /root/shared/results && tar czvf /root/shared/results.tgz *)
    
    # Alert BOINC of the exit status
    cp /root/shared/boinc_app_exit_status /root/shared/completion_trigger_file

}



# Workaround for https://github.com/boot2docker/boot2docker/issues/973
if [ ! -e /root/.shutdown_ran ]; then

    run_showdown 2&>1 | tee -a /root/shared/results/boot2docker.log

    touch /root/.shutdown_ran

fi

