import inotify.adapters
import os
import shutil
import time


config = {
    "dirs": {
        "from": os.getenv("IWATCH_FROM", "/in"),
        "to": os.getenv("IWATCH_TO", "/out"),
    },
    "timeout": int(os.getenv("IWATCH_TIMEOUT", 30)),
}

loglines = [""]


def log(line):
    if line == loglines[-1]:
        return
    print(line)
    loglines[-1] = line


def _main():
    i = inotify.adapters.InotifyTree(config["dirs"]["from"])

    files = {}
    lastcount = 0

    log(f'Looking for existing files in {config["dirs"]["from"]}')
    for dirpath, _, filenames in os.walk(config["dirs"]["from"]):
        for f in filenames:
            log(f"found {f}")
            files[dirpath + f] = {"path": dirpath, "filename": f, "time": time.time()}

    log("waiting for events")
    for event in i.event_gen(yield_nones=True):
        if event is None:
            completed = []
            for filename, file in files.items():
                if file["time"] < time.time() - config["timeout"]:
                    completed.append(filename)
                    fpath = os.path.join(file["path"], file["filename"])
                    if not os.path.isfile(fpath):
                        continue
                    tpath = fpath.replace(config["dirs"]["from"], config["dirs"]["to"])
                    shutil.move(fpath, tpath)
                    log(f"moved {fpath}")

            for filename in completed:
                del files[filename]

            if len(files) != lastcount:
                log(f"waiting for {len(files)} files to be completed")
                lastcount = len(files)

            continue

        (_, type_names, path, filename) = event
        if filename == "" or any(filter(lambda x: x in ["IN_MOVED_FROM"], type_names)):
            # Assume we moved the file ourself, so no need to take an action here
            continue

        fname = path + filename
        if "IN_DELETE" in type_names:
            # Ok, the file is gone, just notify and remove from watched files
            log(f"removed file {path}/{filename}")
            if fname in files:
                del files[fname]

            continue

        if not any(filter(lambda x: x in ["IN_MODIFY", "IN_CREATE"], type_names)):
            # skip all uninteresting events
            continue

        if fname not in files:
            log(f"PATH=[{path}] FILENAME=[{filename}] EVENT_TYPES={type_names}")
            files[fname] = {
                "path": path,
                "filename": filename,
            }
        files[fname]["time"] = time.time()


if __name__ == "__main__":
    _main()
