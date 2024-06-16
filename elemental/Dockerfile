FROM registry.suse.com/suse/sle-micro/5.5:latest AS build

RUN rpm --import https://download.opensuse.org/distribution/leap/15.5/repo/oss/gpg-pubkey-29b700a4-62b07e22.asc && \
    zypper addrepo --refresh http://download.opensuse.org/distribution/leap/15.5/repo/oss/ oss && \
    zypper --non-interactive rm k9s kernel-firmware* && \
    zypper --non-interactive in ncdu htop kernel-firmware-brcm && \
    zypper clean --all

COPY --chmod=0600 wifi.nmconnection /etc/NetworkManager/system-connections/wifi.nmconnection

# IMPORTANT: /etc/os-release is used for versioning/upgrade. The
# values here should reflect the tag of the image currently being built
ARG IMAGE_REPO=ghcr.io/dgiebert/cloudland-2024
ARG IMAGE_TAG=1.0.0
RUN echo "IMAGE_REPO=${IMAGE_REPO}"          > /etc/os-release && \
    echo "IMAGE_TAG=${IMAGE_TAG}"           >> /etc/os-release && \
    echo "IMAGE=${IMAGE_REPO}:${IMAGE_TAG}" >> /etc/os-release

# Flatten the image to reduce the final size since we are not interested in layers
FROM scratch as os
COPY --from=build / /

FROM registry.suse.com/suse/sle-micro/5.5:latest AS builder
ARG TARGETARCH
WORKDIR /iso
COPY --from=os / rootfs

# Fix needed for buildah
RUN --mount=type=bind,source=./,target=/output,rw \
    rm -rf rootfs/etc/resolv.conf && \
    elemental build-iso \
        dir:rootfs \
        --bootloader-in-rootfs \
        --squash-no-compression \
        -n "elemental-teal-${TARGETARCH}" \
        -o /output -n "elemental-${TARGETARCH}"