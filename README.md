boinc2docker
============

This package creates a [BOINC](https://boinc.berkeley.edu/) app which can run [Docker](https://www.docker.com/) containers, greatly simplyfing the work it takes to develop and deploy applications for BOINC. It works by combining the power of [boot2docker](http://boot2docker.io/) and [vboxwrapper](http://boinc.berkeley.edu/trac/wiki/VboxApps).

Once installed on your BOINC project, you simply create Docker images and push them to the free public [Docker hub](http://hub.docker.com) (or host your own Docker registry). You then submit BOINC jobs to your hosts which automatically download images and run them. Images will remain cached on the hosts so they never download the same one twice. 

With boinc2docker,

* You don't need to inject BOINC library calls into your app
* Checkpointing is automatically provided by vboxwrapper
* Your apps automatically work on Windows, Mac OS, and Linux
* You can conveniently build your apps via Dockerfiles
* If you make changes to your images, hosts intelligently download only the updates

This project is currently in development. Use in production at your own risk. 

Instructions
------------

#### Install

To add this app to your BOINC project,

* `git clone` this repository onto your server
* Run `boinc2docker_create_app --projhome <projhomedir>` to copy the app files to your project. This command has a number of options to control things like the name, version, etc... of the created app. See `boinc2docker_create_app -h` for documentation.
* Run `bin/update_versions`

#### Submit Jobs

To submit a Docker job to your server, use the `bin/boinc2docker_create_work.py` command (run with `-h` for documentation). It has all of the same options as BOINC's `bin/create_work` command, and is additionally meant to resemble a `docker run` command. So for example, to create a job which would execute following `docker run` command,
```
docker run python:3-slim python -c "print('Hello BOINC')"
```
you would do,
```
bin/boinc2docker_create_work.py python:3-slim python -c "print('Hello BOINC')"
```
This creates the job on the server. When a client gets this job, their computer will then run the given Docker command, automatically downloading any images (in this case `python:3-slim`) as necessary.

#### Input and Output Files

All files written to `/root/shared/results/` from inside of the Docker container are automatically returned to the server as an output file from the job `results.tgz`. 

(TODO: custom input files don't work yet) 
<!-- To use input files for your job, edit the [`boinc2docker_in`](/templates/boinc2docker_in) file to add any extra input files you may need and copy it to the `templates` folder on your server. Input files with logical name `shared/X` will appear as `/root/shared/X` inside the Docker container. -->


Limitations 
-----------
* This will only run on 64 bit hosts (or 32 bit hosts with VT-x extensions). 
* There is a one-time download overhead for hosts to get the boinc2docker app (~25Mb). Docker base images then range from ~2Mb for Busybox to ~65Mb for Ubuntu and will also be a one-time download. 
* If your application is not multithreaded and N tasks start simultaneously, its possible the same images will be downloaded N times. 



How it works
------------

boot2docker is a compact (~25mb) bootable ISO based on TinyCore Linux which has everything set up so Docker can run inside of it. It also has Virtualbox Guest Additions preinstalled which is necessary to set up the shared folders needed to make this work with BOINC/vboxwrapper. We modify the ISO so that by default on boot it sets up everything needed to interact with vboxwrapper and runs a user provided script which starts a Docker image. The VM also persists any downloaded Docker images to the hosts `project/` directory via the shared `scratch/` directory, so that each host will never have to redownload any image. This is extremely efficient if your apps are all based off of the same base images. 


TODO:
-----
* Recovering from persistence file corruption
* Framework for assimilators/validators
* Allowing multiple simultaneous tasks without danger of redundant downloading of images. 
