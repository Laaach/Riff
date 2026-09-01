import os
import stat
import pwd
import grp

def present(file):

    st = os.stat(file)


    owner = pwd.getpwuid(st.st_uid).pw_name
    group = grp.getgrgid(st.st_gid).gr_name
    path = os.path.abspath(file)
    is_dir = int(stat.S_ISDIR(st.st_mode))
    perm = st.st_mode & 0o7777

    return f"owner={owner:<12} group={group:<12} perm={perm:04o} is_dir={is_dir:<3} path={path}"
