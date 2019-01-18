boinc2docker
============

This package provides a [BOINC](https://boinc.berkeley.edu/) app which can run [Docker](https://www.docker.com/) containers, greatly simplyfing the work it takes to develop and deploy applications for BOINC. It works by combining the power of [boot2docker](http://boot2docker.io/) and [vboxwrapper](http://boinc.berkeley.edu/trac/wiki/VboxApps).

Once installed on your BOINC project, you simply create Docker images to run you science applications, and boinc2docker packages them up 

With boinc2docker,

* You don't need to inject BOINC library calls into your app
* Checkpointing is automatically provided by vboxwrapper
* Your apps automatically work on Windows, Mac OS, and Linux
* You can conveniently build your apps via Dockerfiles
* If you make changes to your images, hosts intelligently download only the updates

This project is currently in development. Use in production at your own risk. 


## Requirements

* At least BOINC [server_release/1.0/1.0.0](https://github.com/BOINC/boinc/releases/tag/server_release%2F1.0%2F1.0.3)

## Install


The easiest way to use boinc2docker is to install your server via [boinc-server-docker](https://github.com/marius311/boinc-server-docker), which comes with boinc2docker pre-installed. 

You can also add boinc2docker to any existing BOINC project with the following steps:

* `git clone` this repository onto your server
* Run `boinc2docker_create_app --projhome <projhomedir>` to copy the app files to your project. This command has a number of options to control things like the name, version, etc... of the created app. See `boinc2docker_create_app -h` for documentation.
* Run `bin/update_versions`

## Usage

Once installed to your server, to submit a Docker job to your server, use the `bin/boinc2docker_create_work.py` command (run with `-h` for documentation). It has all of the same options as BOINC's `bin/create_work` command, and is additionally meant to resemble a `docker run` command. So for example, to create a job which would execute following `docker run` command,
```
docker run python:3-slim python -c "print('Hello BOINC')"
```
you would do,
```
bin/boinc2docker_create_work.py python:3-slim python -c "print('Hello BOINC')"
```
This creates the job on the server. When a client gets this job, their computer will then run the given Docker command (the Docker image for, in this example, `python:3-slim`, is delievered to the client as input files).

### Input and Output Files

All files written to `/root/shared/results/` from inside of the Docker container are automatically returned to the server as an output file from the job `results.tgz`. 

To use custom input files, you'll need to call the Python function directly, see [the Python code](https://github.com/marius311/boinc2docker/blob/master/bin/boinc2docker_create_work.py#L22), in particular the `input_files` option. A command line interface is planned in the future. 

See also the boinc-server-docker [cookbook](https://github.com/marius311/boinc-server-docker/blob/master/docs/cookbook.md).

Limitations 
-----------
* These jobs use vboxwrapper which means they will only run on 64 bit hosts with VT-x extensions enabled.
* There is a one-time download overhead for hosts to get the boinc2docker app (~25Mb). Docker base images then range from ~2Mb for Busybox to ~65Mb for Ubuntu and will also be a one-time download. 



How it works
------------

boot2docker is a compact (~25mb) bootable ISO based on TinyCore Linux which has everything set up so Docker can run inside of it. It also has Virtualbox Guest Additions preinstalled which is necessary to set up the shared folders needed to make this work with BOINC/vboxwrapper. We modify the ISO so that by default on boot it sets up everything needed to interact with vboxwrapper and runs a user provided script which starts a Docker image. Docker images are split into layers, each of which is delievered to hosts as a separate "sticky" BOINC input file. This means each layer is only sent to a given host once (which is nice especially if you use mulitple images which share common base layers).
