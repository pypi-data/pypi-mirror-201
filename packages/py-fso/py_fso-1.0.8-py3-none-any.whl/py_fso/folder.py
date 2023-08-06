"""Module for processing folder with its subfolders and files."""
# Use the built-in version of scandir if possible,
# otherwise use the scandir module version
try:
    from os import scandir
except ImportError:
    from scandir import scandir

from collections import deque
from inspect import isfunction


def process(init_dir, process_files=True, proc_file_function=None, process_dirs=False, proc_dir_function=None,
            go_into_subdirs=True, follow_symlinks=False) -> int:
    """
    Process all files and dirs in given init_dir (and its subdirs if go_into_subdirs = True).

    :param init_dir: an initial folder to process, required
    :type init_dir: string
    :param process_files: whether the files need to be processed
    :type process_files: bool
    :param proc_file_function: function for a file's processing, optional
    :type proc_file_function: function|None
    :param process_dirs: whether the subdirs need to be processed
    :type process_dirs: bool
    :param proc_dir_function: function for a dir's processing, optional
    :type proc_dir_function: function|None
    :param go_into_subdirs: whether the subdirs should be processing
    :type go_into_subdirs: bool
    :param follow_symlinks: whether the symlinks should be treated as normal folders
    :type follow_symlinks: bool
    :return: -1 if failed and 0 if succeded
    :rtype: int

    """

    if process_files and not isfunction(proc_file_function):
        print("No function for files")
        return -1
    if process_dirs and not isfunction(proc_dir_function):
        print("No function for dirs")
        return -1

    dir_list = deque()
    dir_list.append(init_dir)

    while len(dir_list) > 0:
        path = dir_list.popleft()
        try:
            dir_iterator = scandir(path)
        except PermissionError:
            # System Volume Information, Recycle and the like
            print("Permission denied: ", path)
            continue
        for entry in dir_iterator:
            if entry.is_dir(follow_symlinks=follow_symlinks):
                if process_dirs:
                    proc_dir_function(entry)
                if go_into_subdirs:
                    dir_list.append(entry.path)
            else:
                if process_files:
                    proc_file_function(entry)
    return 0
