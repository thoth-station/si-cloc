FROM quay.io/thoth-station/s2i-thoth-ubi8-py36

USER 0

RUN dnf install cloc -y
RUN pip install --upgrade pip -y
RUN pip install pipenv -y
RUN pipenv shell

USER 1001
