FROM python:2.7
COPY ./install_ssh_keys.py /opt/bin/install_ssh_keys.py
RUN pip install PyGithub PyCrypto
ENTRYPOINT ["/opt/bin/install_ssh_keys.py"]
