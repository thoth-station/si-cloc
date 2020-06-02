FROM registry.access.redhat.com/ubi8/python-36:1-89.1589298690

USER 0

RUN sudo dnf install cloc -y
RUN pip install --upgrade pip
RUN pipenv shell

USER 1001

# TODO: I know this isn't quite right :/

ENTRYPOINT [ "python app.py" ]
