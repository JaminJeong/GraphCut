import os

def split_path_filename_fileext(fullpath):
    path, fullfilename = os.path.split(fullpath)
    filename, fileext = os.path.splitext(fullfilename)
    return path, filename, fileext
