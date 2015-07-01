boinc2docker
============

Based on [boot2docker](http://boot2docker.io/), this packages creates a bootable ISO which is meant to be used as a BOINC [VirtualBox app](http://boinc.berkeley.edu/trac/wiki/VboxApps). This allows running Docker apps on a BOINC project, so rather than having to develop arcane BOINC apps which must be injected with BOINC library calls and cross compiled for all platforms, code simply needs to be packaged in a Docker app (and can now be nearly seamlessly sent to either a BOINC project or any cloud computing service). One limitation is that only 64 bit clients, or 32 bit clients which have the VT-x extension, will be able to run this image (perhaps [32bit docker](https://github.com/docker-32bit) could solve this in the future...)

This project is currently in early development

Instructions
------------

If you manage a BOINC project and would like to use this app, you can follow these instructions. 

The only requirement is a recent version of [Docker](https://www.docker.com/). The shell scripts will only work on Linux (and maybe OSX?) but are trivial to replicate on any other system. 

* Run `./make` to build the modified boot2docker ISO. (Note: this involves downloading a ~1Gb Docker image. In the future just the ISO can be distributed)
* Run `./cp2boinc <boinc-project-dir>` to copy the necessary files as well as the example boinc2docker app to your project directory. 
* Create copies of `apps/boinc2docker/1.0/x86_64-pc-linux-gnu/` for any other (64 bit) app versions you would like to support. 
* Download the `vboxwrapper` executables from [here](http://boinc.berkeley.edu/trac/wiki/VboxApps) and place them the folder for each app version.
* Modify `version.xml` so that in each app version folder it points to the appropriate file name for `vboxwrapper`.
* Add the following to your `project.xml`:
```xml
  <app>
    <name>boinc2docker</name>
    <user_friendly_name>boinc2docker</user_friendly_name>
  </app>
```
* Run `/bin/update_versions`
* Stage the boinc_app and necessary input files with `/bin/stage_file apps_boinc2docker/example/boinc2docker_example_app` and `/bin/stage_file apps_boinc2docker/example/params/boinc2docker_example_params1`
* Submit the job with `bin/create_work --appname boinc2docker boinc2docker_example_boinc_app boinc2docker_example_params1`
