FROM python:3.7-alpine

VOLUME ["/in", "/out"]

RUN python -m pip install inotify \
			&& adduser copyuser -D -H -g ""

COPY --chown=copyuser:copyuser script.py /
COPY entrypoint.sh /

CMD ["/entrypoint.sh"]
