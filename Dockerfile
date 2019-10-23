FROM python:3.7

VOLUME ["/in", "/out"]

RUN python -m pip install inotify \
			&& adduser mayan --disabled-password --disabled-login --no-create-home --gecos ""

COPY --chown=mayan:mayan script.py /
COPY entrypoint.sh /

CMD ["/entrypoint.sh"]
