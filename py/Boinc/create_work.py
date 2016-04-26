import boinc_path_config
from sched_messages import SchedMessages, CRITICAL
from subprocess import CalledProcessError, check_output as _check_output, STDOUT
from itertools import chain
import os, os.path as osp
from uuid import uuid4
from time import time
import argparse
import re



log = SchedMessages()
class CheckOutputError(Exception): pass

projdir = osp.realpath(osp.join(osp.dirname(__file__),'..','..'))

def _get_create_work_args():
    try: _check_output([osp.join(projdir,'bin','create_work')],stderr=STDOUT)
    except CalledProcessError as e: doc = e.output
    matches = [g.groups() for g in [re.search('--(.*?) (.*?) ',l) for l in doc.splitlines()] if g]
    args = {k:{'n':int,'x':float}.get(v,str) for k,v in matches}
    args['additional_xml']=str
    return args

create_work_args = _get_create_work_args()



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

def dir_hier_path(filename):
    return check_output(['bin/dir_hier_path',filename],cwd=projdir).strip()


def stage_file(name,contents,perm=None):
    base,ext = osp.splitext(name)
    fullname = base + '_' + uuid4().hex + ext
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
                           [stage_file(*i) if isinstance(i,tuple) else i for i in input_files]),
                          cwd=projdir)


def add_create_work_args(parser,exclude=None):
    """
    Add BOINC's bin/create_work arguments to a Python argparse parser
    exclude can be a list of args not to add
    """
    for k,v in sorted(create_work_args.items()):
        if exclude is None or k not in exclude:
            parser.add_argument('--%s'%k,type=v,metavar={int:'n',float:'x',str:'string'}[v])
    parser.add_argument('--credit',type=float, metavar='x')


def read_create_work_args(args):
    """
    Read create_work_args from Python argparse args
    """
    if isinstance(args,argparse.Namespace): args=vars(args)
    cwargs = {k:v for k,v in args.items() if k in create_work_args and v is not None}
    if args.get('credit'): 
        cwargs['additional_xml'] = (args['additional_xml'] or '')+'<credit>%s</credit>'%args['credit']
    return cwargs
