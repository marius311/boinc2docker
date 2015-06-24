FROM boot2docker/boot2docker
ADD . $ROOTFS/data/
RUN /make_iso.sh
CMD ["cat", "boot2docker.iso"]
