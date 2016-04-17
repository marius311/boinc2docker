#!/usr/bin/env python

import argparse
import boinc_path_config
import json
import sys
import os
import tarfile
import xml.etree.cElementTree as ET
from Boinc.create_work import add_create_work_args, read_create_work_args, create_work, projdir, dir_hier_path
from functools import partial
from os.path import join, split, exists
from subprocess import check_output
from xml.dom import minidom
from inspect import currentframe
from textwrap import dedent
from uuid import uuid4 as uuid
from tempfile import mkdtemp


def boinc2docker_create_work(image,command,
                             appname='boinc2docker',
                             entrypoint=None,
                             env=None,
                             create_work_args=None):

    fmt = partial(lambda s,f: s.format(**dict(globals(),**f.f_locals)),f=currentframe())
    sh = lambda cmd: check_output(['sh','-c',fmt(cmd)]).strip()
    tmpdir = mkdtemp()

    try:

        #get entire image as a tar file
        image_id = sh('docker inspect --format "{{{{ .Id }}}}" {image}').strip().split(':')[1]
        image_filename = fmt("image_{image_id}.tar")
        image_path = dir_hier_path(image_filename)

        if exists(image_path):
            need_extract = False
            manifest = json.load(tarfile.open(image_path).extractfile('manifest.json'))
        else:
            need_extract = True
            sh("docker save {image} | tar xf - -C {tmpdir}")
            manifest = json.load(open(join(tmpdir,'manifest.json')))


        input_files = []


        #generate boinc_app script
        command = ' '.join('"'+str(x)+'"' for x in command)
        entrypoint = '--entrypoint '+entrypoint if entrypoint else ''
        script = dedent(fmt("""
        #!/bin/sh
        set -e 

        mkdir -p /tmp/image
        for f in $(ls /root/shared/image/*.tar); do
            tar xvf $f -C /tmp/image
        done
        tar cvf - -C /tmp/image . | docker load 
        echo Running... && docker run --rm -v /root/shared:/root/shared {entrypoint} {image} {command}
        """))
        input_files.append(('shared/boinc_app',('boinc_app',script)))


        #extract layers to individual tar files, directly into download dir
        for layer in manifest[0]['Layers']:
            layer_id = split(layer)[0]
            layer_filename = fmt("layer_{layer_id}.tar")
            layer_path = sh("bin/dir_hier_path {layer_filename}")
            input_files.append((fmt("shared/image/{layer_filename}"),layer_filename))
            if need_extract: sh("tar cvf {layer_path} -C {tmpdir} {layer_id}")


        #extract remaining image info to individual tar file, directly into download dir
        input_files.append((fmt("shared/image/{image_filename}"),image_filename))
        if need_extract: sh("tar cvf {image_path} -C {tmpdir} {image_id}.json manifest.json repositories")


        #generate input template
        root = ET.Element("input_template")
        workunit = ET.SubElement(root, "workunit")
        for i,(open_name,_) in enumerate(input_files):
            fileinfo = ET.SubElement(root, "file_info")
            ET.SubElement(fileinfo, "number").text = str(i)
            if i!=0: 
                ET.SubElement(fileinfo, "sticky")
                ET.SubElement(fileinfo, "no_delete")
            fileref = ET.SubElement(workunit, "file_ref")
            ET.SubElement(fileref, "file_number").text = str(i)
            ET.SubElement(fileref, "open_name").text = open_name
            ET.SubElement(fileref, "copy_file")
        template_file = join(tmpdir,'boinc2docker_in_'+uuid().hex)
        open(template_file,'w').write(minidom.parseString(ET.tostring(root, 'utf-8')).toprettyxml(indent=" "*4))

        create_work_args['wu_template'] = template_file
        return create_work(appname, create_work_args, [f for _,f in input_files]).strip()

    except KeyboardInterrupt:
        print("Cleaning up temporary files...")
    finally:
        #cleanup
        try:
            sh("rm -rf {tmpdir}")
        except:
            pass


if __name__=='__main__':

    parser = argparse.ArgumentParser(prog='boinc2docker_create_work')

    #docker args
    parser.add_argument('IMAGE', help='Docker image to run')
    parser.add_argument('COMMAND', nargs=argparse.REMAINDER, metavar='COMMAND', help='command to run')
    parser.add_argument('--entrypoint', help='Overwrite the default ENTRYPOINT of the image')

    #BOINC args
    parser.add_argument('--appname', default='boinc2docker', help='appname (default: boinc2docker)')
    add_create_work_args(parser,exclude=['wu_template'])

    args = parser.parse_args()

    print boinc2docker_create_work(image=args.IMAGE, 
                                   command=args.COMMAND, 
                                   appname=args.appname,
                                   entrypoint=args.entrypoint,
                                   create_work_args=read_create_work_args(args))
