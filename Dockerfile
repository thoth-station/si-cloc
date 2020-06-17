FROM quay.io/thoth-station/s2i-thoth-f32-py38
ENV LANG=en_US.UTF-8
USER 0
RUN dnf install --setopt=tsflags=nodocs -y cloc
USER 1001
