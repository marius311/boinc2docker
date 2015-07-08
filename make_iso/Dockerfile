FROM boot2docker/boot2docker

# speed up boot by changing to waitusb=0 from whatever it was
# (we don't need Hyper-V, see https://github.com/boot2docker/boot2docker/commit/1ecda6fcc4ac755feeca9612981527702c0daf49)
RUN sed -E -i 's/waitusb=[0-9]+/waitusb=0/g' /tmp/iso/boot/isolinux/isolinux.cfg

# add the BOINC specific startup scripts
COPY *.sh $ROOTFS/opt/

RUN /make_iso.sh
CMD ["cat", "boot2docker.iso"]
