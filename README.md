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

If you would like to add this app to your BOINC project,

* Run `ISOTAG=v0.42 VBOXTAG=v0.5 ./setup_versions`, which downloads the vboxwrapper executables and boinc2docker ISO, and sets up the folder structure in `apps/boinc2docker/1.0`. 
* Run `./install_as <projdir> <appname> <version> <vboxjob.xml>`. This script copies the files set up by the previous step to your project directory `<projdir>` as an app with name `<appname>` and version `<version>`, using the `vboxjob.xml` file specified (you can use the [default](/apps/boinc2docker/1.0/example/vbox_job.xml) or add your own modifications).  If you want multiple apps which use boinc2docker, simply run this command multiple times.
* Add the contents of [/plan_class_spec.xml](/plan_class_spec.xml) to the file in your project directory (or create it if it doesn't exist).
* Add the apropriate app tag to your `project.xml` file, e.g. `<app> <name>boinc2docker</name> </app>` where `boinc2docker` is replaced with the name you gave your app. 
* Run `bin/update_versions`
* Stage input files and create work as usual. 


Limitations 
-----------
* This will only run on 64 bit hosts (or 32 bit hosts with VT-x extensions). 
* There is a one-time download overhead for hosts to get the boinc2docker app (~25Mb). Docker base images then range from ~2Mb for Busybox to ~200Mb for Ubuntu and will also be a one-time download. 
* If your application is not multithreaded and N tasks start simultaneously, its possible the same images will be downloaded N times. 



How it works
------------

boot2docker is a compact (~25mb) bootable ISO based on TinyCore Linux which has everything set up so Docker can run inside of it. It also has Virtualbox Guest Additions preinstalled which is necessary to set up the shared folders needed to make this work with BOINC/vboxwrapper. We modify the ISO so that by default on boot it sets up everything needed to interact with vboxwrapper and runs a user provided script which starts a Docker image. The VM also persists any downloaded Docker images to the hosts `project/` directory via the shared `scratch/` directory, so that each host will never have to redownload any image. This is extremely efficient if your apps are all based off of the same base images. 


TODO:
-----
* Recovering from persistence file corruption
* Framework for assimilators/validators
* Allowing multiple simultaneous tasks without danger of redundant downloading of images. 
