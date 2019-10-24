#!/bin/sh

DEFAULT_UID=1000
DEFAULT_GID=1000

COPYUSER_UID=${COPYUSER_UID:-${DEFAULT_UID}}
COPYUSER_GID=${COPYUSER_GID:-${DEFAULT_GID}}

groupmod copyuser -g ${COPYUSER_GID} 2>/dev/null || true
usermod copyuser -u ${COPYUSER_UID} -g ${COPYUSER_GID} 2>/dev/null
chown -R copyuser:copyuser /in /out 

su copyuser -c "python -u /script.py"
