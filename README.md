boinc2docker
============

This package creates a [BOINC](https://boinc.berkeley.edu/) app which can run [Docker](https://www.docker.com/) images, greatly simplyfing the work it takes to develop and deploy applications for BOINC. It works by combining the power of [boot2docker](http://boot2docker.io/) and [vboxwrapper](http://boinc.berkeley.edu/trac/wiki/VboxApps).

Once installed on your BOINC project, you simply create Docker images and push them to the free public Docker [hub](http://hub.docker.com) (or host your own Docker registry). When you submit jobs, your BOINC hosts will automatically download the images from there and run them. This removes the need to inject BOINC library calls into your app, to provide checkpointing (this is automatically handled by the Virtualbox wrapper), or to cross compile (you only need to install your app inside the Docker container, and it will run on any system which supports Virtualbox, including Linux, Windows, and OSX). 

This project is currently in early development. Please do not use for production. 

Instructions
------------

If you manage a BOINC project and would like to use this app, follow these instructions. 

The only requirement is a recent version of [Docker](https://www.docker.com/). The shell scripts will only work on Linux (and maybe OSX?) but are trivial to replicate on any other system. 

* Run `./make` to build the modified boot2docker ISO. (Note: this involves downloading a ~1Gb Docker image. In the future this ISO will be distributed)
* Run `./cp2boinc <boinc-project-dir>` to copy the necessary files as well as the example boinc2docker app to your project directory. 
* Create copies of `apps/boinc2docker/1.0/x86_64-pc-linux-gnu/` for any other app versions you would like to support. 
* Download the `vboxwrapper` executables from [here](http://boinc.berkeley.edu/trac/wiki/VboxApps#Premadevboxwrapperexecutables) and place them the folder for each app version.
* Modify `version.xml` so that in each app version folder it points to the appropriate file name for `vboxwrapper`.
* Add the following to your `project.xml`:
```xml
  <app>
    <name>boinc2docker</name>
    <user_friendly_name>boinc2docker</user_friendly_name>
  </app>
```
* Run `/bin/update_versions`
* Stage the boinc app and necessary input files (e.g. `/bin/stage_file apps_boinc2docker/example/boinc2docker_example_app` and `/bin/stage_file apps_boinc2docker/example/params/boinc2docker_example_params1`)
* Submit the job (e.g. `bin/create_work --appname boinc2docker boinc2docker_example_boinc_app boinc2docker_example_params1`)


Limitations 
-----------
* This will only run on 64 bit hosts (or 32 bit hosts with VT-x extensions). 
* There is a one-time download overhead for hosts to get the boinc2docker app (~25Mb). Docker base images then range from ~2Mb for Busybox to ~200Mb for Ubuntu and will also be a one-time download. 
* Currently, only one boinc2docker task can run at a time per host (thus your Docker app must be multithreaded to take advtange of multi-CPU hosts)



How it works
------------

boot2docker is a compact (~25mb) bootable ISO based on TinyCore Linux which has everything set up so Docker can run inside of it. It also has Virtualbox Guest Additions preinstalled which is necessary to set up the shared folders needed to make this work with BOINC/vboxwrapper. We modify the ISO so that by default on boot it sets up everything needed to interact with vboxwrapper and runs a user provided script which starts a Docker image. (TODO:) The VM is also attached to a Virtualbox drive which persists in your project directory on the host. Any downloaded Docker images will be cached here, thus each host will never have to redownload any image. This is extremely efficient if your apps are all based off of the same base images. 


TODO:
-----
* Persistence drive. 
  * How exactly will vboxwrapper handle it? (will require some modifications to vboxwrapper)
  * How to recover if it becomes corrupt.
* How to limit 1 task / host. 
  * WISHLIST: Allow for more than 1? Can't see how that would work with current set up. 
* Progress file
* Allow multithreaded VM
* Better logging
