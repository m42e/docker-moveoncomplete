# MoveOnComplete

This simple tool, allows to specify an input folder to watch and an output folder to copy files to, as soon as the file does not change any more.
The changes to the file are watched using inotify with a Python wrapper.

## Why?

I am using it in combination with [Mayan-EDMS](https://mayan-edms.com). The document scanner I use is capable of uploading files using SFTP. But while using it with Mayan, I discovered, that sometimes the file is not correctly imported. This happens if Mayan tries to work with the file, while it is still uploaded. As the scanner software is not a subject to change. I decided to build a small to that does one thing well.

## How?

This docker image registers for inotify events in a [folder structure](#IWATCH_FROM). If there is anything written in that structure it keeps an entry with the filepath and the last time it has been written.
Every time an event like MODIFY or CREATE happens the entry is updated.
The inotify events created also contain `None` events. These occur after a configurable [timeout](#IWATCH_TIMEOUT).
If there are no events for a time period longer or equal the [timeout](#IWATCH_TIMEOUT) the file is moved to the (target folder)[#IWATCH_TO]. 


## Usage

Run the docker container with the following environment variables:

### IWATCH_FROM

Folder to watch for new files and changes. (default: `/in`)

### IWATCH_TO

Folder to move files to. (default: `/out`)

### IWATCH_TIMEOUT

Timeout to wait for further changes (default: 30 Seconds).


### Docker commandline

```bash
docker run -v <local path to in folder>:/in -v <local path to output>:/out moveoncomplete
```

