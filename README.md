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

If you manage a BOINC project and would like to use boinc2docker, follow these instructions. 

Requirements:

* A recent version of [Docker](https://www.docker.com/).

boinc2docker is a regular BOINC application. To install,

* Download `vm_isocontext.iso` from the [latest release](https://github.com/marius311/boinc2docker/releases) of boinc2docker and place it in `apps/boinc2docker/1.0/x86_64-pc-linux-gnu__vbox64_mt` (alternatively build the ISO yourself by running `./make_iso.sh`, this requires a ~1GB download). 
* Run `./cp2boinc <boinc-project-dir>` to copy the necessary files and example boinc2docker app to your project directory. 
* Create copies of `apps/boinc2docker/1.0/x86_64-pc-linux-gnu__vbox64_mt/` with appropriate names for other app versions you would like to support. 
* Download the `vboxwrapper` executables from [here](http://boinc.berkeley.edu/dl) and place them in each app version folder (note: you need version >= 26169)
* Modify `version.xml` so that in each app version folder it points to the appropriate file name for `vboxwrapper`.
* Add the contents of `project.xml` and `plan_class_spec.xml` to these same files in your project directory (or create them if they don't exist).
* Run `/bin/update_versions`
* Stage the boinc app and necessary input files (e.g. `/bin/stage_file apps_boinc2docker/example/boinc2docker_example_app` and `/bin/stage_file apps_boinc2docker/example/params/boinc2docker_example_params1`)
* Submit the job (e.g. `bin/create_work --appname boinc2docker boinc2docker_example_boinc_app boinc2docker_example_params1`)


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
