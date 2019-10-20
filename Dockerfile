FROM python:3.7

VOLUME ["/in", "/out"]

RUN python -m pip install inotify

COPY script.py /

CMD ["python", "-u", "/script.py"]
