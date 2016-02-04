#!/usr/bin/env python

import argparse
import boinc_path_config
from Boinc.create_work import add_create_work_args, read_create_work_args, create_work

script = """#!/bin/sh
set -e 

REPO={repo}
TAG={tag}
IMG=$REPO:$TAG

docker inspect $IMG > /dev/null && echo Found $IMG 
if [ $? -ne 0 ]; then 
    echo Pulling $IMG 
    docker pull $IMG 
    docker images $REPO | tail -n +2 | awk '{{print $1":"$2}}' | grep -vx $IMG | xargs --no-run-if-empty docker rmi 
    save_docker.sh
fi
echo Running... && docker run --rm -v /root/shared:/root/shared {entrypoint} $IMG {command}
"""


def boinc2docker_create_work(image,command,
                             appname='boinc2docker',
                             entrypoint=None,
                             env=None,
                             create_work_args=None):

    if ':' not in image: image+=':latest'
    repo,tag = image.split(':')
    fscript = script.format(repo=repo,tag=tag,
                            command=' '.join('"'+str(x)+'"' for x in command),
                            entrypoint=('--entrypoint '+entrypoint) if entrypoint else '')

    return create_work(appname, create_work_args, [('boinc_app',fscript)]).strip()



if __name__=='__main__':



    parser = argparse.ArgumentParser(prog='boinc2docker_create_work')

    #docker args
    parser.add_argument('IMAGE', help='Docker image to run')
    parser.add_argument('COMMAND', nargs=argparse.REMAINDER, metavar='COMMAND', help='command to run')
    parser.add_argument('--entrypoint', help='Overwrite the default ENTRYPOINT of the image')

    #BOINC args
    parser.add_argument('--appname', default='boinc2docker', help='appname (default: boinc2docker)')
    add_create_work_args(parser)

    args = parser.parse_args()

    print boinc2docker_create_work(image=args.IMAGE, 
                                   command=args.COMMAND, 
                                   appname=args.appname,
                                   entrypoint=args.entrypoint,
                                   create_work_args=read_create_work_args(args)
                                  )
