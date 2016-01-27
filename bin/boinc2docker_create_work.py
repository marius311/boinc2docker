#!/usr/bin/env python

import argparse
import boinc_path_config
from Boinc.create_work import add_create_work_args, read_create_work_args, create_work

script = """#!/bin/sh
set -e 

docker inspect {image} || {{ docker pull {image} && save_docker.sh; }}
docker run --rm -v /root/shared:/root/shared {entrypoint} {image} {command}
"""



def boinc2docker_create_work(image,command,
                             appname='boinc2docker',
                             entrypoint=None,
                             env=None,
                             create_work_args=None):

    fscript = script.format(image=image,
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
    #call boinc2docker_create_work
