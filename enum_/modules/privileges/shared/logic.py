import stat
import os
import subprocess
import threading

lock = threading.Lock()
suids = None
sgids = None

def filter_suid_sgid():

    global suids
    global sgids

    with lock:
        if not suids and not sgids:
            suids = []
            sgids = []
            suids_sgids = subprocess.run(['find', '/', '(', '-path', '/proc', '-o', '-path', '/var/lib/docker', '-o', '-path', '/snap', ')', '-prune','-o', '-type', 'f', '(', '-perm', '-u=s', '-o', '-perm', '-g=s', ')', '-print'], text=True,stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.splitlines()

            for path in suids_sgids:
                mode = os.stat(path).st_mode

                if mode & stat.S_ISUID:
                    suids.append(path)

                if mode & stat.S_ISGID:
                    sgids.append(path)

        return suids, sgids