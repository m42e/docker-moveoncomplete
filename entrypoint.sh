#!/bin/sh

DEFAULT_USER_UID=1000
DEFAULT_USER_GID=1000

MAYAN_USER_UID=${MAYAN_USER_UID:-${DEFAULT_USER_UID}}
MAYAN_USER_GID=${MAYAN_USER_GID:-${DEFAULT_USER_GID}}

update_uid_gid() {
    groupmod mayan -g ${MAYAN_USER_GID} 2>/dev/null || true
    usermod mayan -u ${MAYAN_USER_UID} -g ${MAYAN_USER_GID} 2>/dev/null
		chown -R mayan:mayan /in /out 
}

update_uid_gid

su mayan -c "python -u /script.py"
