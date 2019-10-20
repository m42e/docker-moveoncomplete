import inotify.adapters
import os
import shutil
import time


config = {
    'dirs':{
        'from': os.getenv('IWATCH_FROM', '/in'),
        'to': os.getenv('IWATCH_TO', '/out'),
    },
    'action': 'move',
    'timeout': int(os.getenv('IWATCH_TIMEOUT', 30)),
}

def _main():
    i = inotify.adapters.InotifyTree(config['dirs']['from'])

    files = {}
    lastcount = 0

    print('Looking for existing files in in')
    for dirpath, dirnames, filenames in os.walk(config['dirs']['from']):
        for f in filenames:
            print('found {}'.format(f))
            files[dirpath + f] = {
                'path': dirpath,
                'filename': f,
                'time': time.time()
            }

    print('waiting for events')
    for event in i.event_gen(yield_nones=True):
        if event is None:
            completed = []
            for filename, file in files.items():
                if file['time'] < time.time()-config['timeout']:
                    completed.append(filename)
                    fpath = os.path.join(file['path'], file['filename'])
                    if not os.path.isfile(fpath):
                        continue
                    if config['action'] == 'move':
                        tpath = fpath.replace(config['dirs']['from'], config['dirs']['to'])
                        shutil.move(fpath, tpath)
                        print('moved {}'.format(fpath))
                    else:
                        print('action unknown')
            for filename in completed:
                del files[filename]
            if len(files) != lastcount:
                print('waiting for {} files to be completed'.format(len(files)))
                lastcount = len(files)
            continue
        (_, type_names, path, filename) = event
        if filename == '' or any(filter(lambda x: x in ['IN_MOVED_FROM'], type_names)):
            continue

        fname = path + filename 
        if 'IN_DELETE' in type_names:
            print('removed file {}/{}'.format(path, filename))
            if fname in files:
                del files[path + filename]
            continue

        if not any(filter(lambda x: x in ['IN_MODIFY', 'IN_CREATE'], type_names)):
            continue

        print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format( path, filename, type_names))

        files[path + filename] = {
            'path': path,
            'filename': filename,
            'time': time.time()
        }


if __name__ == '__main__':
    _main()
