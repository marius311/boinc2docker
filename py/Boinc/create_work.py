import boinc_path_config
from sched_messages import SchedMessages, CRITICAL
from subprocess import CalledProcessError, check_output as _check_output, STDOUT
from itertools import chain
import os, os.path as osp
from hashlib import md5
from time import time
import argparse

log = SchedMessages()
class CheckOutputError(Exception): pass

projdir = osp.realpath(osp.join(osp.dirname(__file__),'..','..'))

def check_output(cmd,*args,**kwargs):
    """
    Wraps subprocess.check_output and logs errors to BOINC
    """
    try:
        return _check_output(cmd,stderr=STDOUT,*args,**kwargs)
    except CalledProcessError as e:
        log.printf(CRITICAL,"Error calling %s:\n%s\n",str(cmd),e.output)
        raise CheckOutputError
    except Exception as e:
        log.printf(CRITICAL,"Error calling %s:\n%s\n",str(cmd),str(e))
        raise CheckOutputError


def stage_file(name,contents,perm=None):
    base,ext = osp.splitext(name)
    fullname = base + '_' + md5(str(contents)+str(time())).hexdigest() + ext
    download_path = check_output(['bin/dir_hier_path',fullname],cwd=projdir).strip()
    with open(download_path,'w') as f: f.write(contents)
    if perm: os.chmod(download_path,perm)
    return fullname


def create_work(appname,create_work_args,input_files):
    """
    Creates and stages input files based on a list of (name,contents) in input_files,
    and calls bin/create_work with extra args specified by create_work_args
    """
    
    return check_output((['bin/create_work','--appname',appname]+
                           list(chain(*(['--%s'%k,'%s'%v] for k,v in create_work_args.items())))+
                           [stage_file(*i) for i in input_files]),
                          cwd=projdir)


create_work_args = {
    'target_nresults': int,
    'max_error_results': int,
    'max_success_results': int,
    'max_total_results': int,
    'min_quorum': int,
    'priority': float,
    'rsc_disk_bound': float,
    'wu_name':str,
    'wu_template':str
}

def add_create_work_args(parser):
    """
    Add BOINC's bin/create_work arguments to a Python argparse parser
    """

    for k,v in create_work_args.items():
        parser.add_argument('--%s'%k,type=v,metavar={int:'n',float:'x',str:'string'}[v])

def read_create_work_args(args):
    """
    Read create_work_args from the 
    """
    if isinstance(args,argparse.Namespace): args=vars(args)
    return {k:v for k,v in args.items() if k in create_work_args and v is not None}
