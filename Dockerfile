FROM quay.io/thoth-station/s2i-thoth-ubi8-py36

USER 0

RUN dnf install cloc -y --nodocs

USER 1001
