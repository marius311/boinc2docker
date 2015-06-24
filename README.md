boinc2docker
============

Based on [boot2docker](http://boot2docker.io/), this packages creates a bootable ISO which is meant to be used as a BOINC [VirtualBox app](http://boinc.berkeley.edu/trac/wiki/VboxApps). This allows running Docker apps on a BOINC project, so rather than having to develop arcane BOINC apps which must be injected with BOINC library calls and cross compiled for all platforms, code simply needs to be packaged in a Docker app (and can now be nearly seamlessly sent to either a BOINC project or any cloud computing service). One limitation is that only 64 bit clients, or 32 bit clients which have the VT-x extension, will be able to run this image (perhaps [32bit docker](https://github.com/docker-32bit) could solve this in the future...)

This project is currently in early development and no working version exists yet. 
