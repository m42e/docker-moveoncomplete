FROM python:3.7

VOLUME ["/in", "/out"]

RUN python -m pip install inotify \
			&& adduser copyuser --disabled-password --disabled-login --no-create-home --gecos ""

COPY --chown=copyuser:copyuser script.py /
COPY entrypoint.sh /

CMD ["/entrypoint.sh"]
