import datetime
import pwd
import tarfile
import zipfile
from os import makedirs, pardir, remove, stat, walk
from os.path import abspath, basename, getmtime, getsize, isdir, isfile, join
from shutil import copy, copytree, move, rmtree


def get_owner(file_path):
    return pwd.getpwuid(stat(file_path).st_uid).pw_name


def get_modified_time(file_path):
    return datetime.datetime.fromtimestamp(getmtime(file_path))


def get_dir_size(start_path):
    """Returns the total size of a directory.

    See https://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
    """
    total_size = 0
    for dirpath, dirnames, filenames in walk(start_path):
        for f in filenames:
            fp = join(dirpath, f)
            total_size += getsize(fp)
        for d in dirnames:
            dp = join(dirpath, d)
            total_size += getsize(dp)
    return total_size if total_size else False


def remove_file_or_dir(file_path):
    removed = False
    if isfile(file_path):
        try:
            remove(file_path)
            removed = True
        except Exception as e:
            print(e)
    elif isdir(file_path):
        try:
            rmtree(file_path)
            removed = True
        except Exception as e:
            print(e)
    return removed


def copy_file_or_dir(src, dest):
    copied = False
    if isdir(src):
        copytree(src, dest)
        copied = True
    elif isfile(src):
        if not isdir(abspath(join(dest, pardir))):
            makedirs(abspath(join(dest, pardir)))
        copy(src, dest)
        copied = True
    return copied


def move_file_or_dir(src, dest):
    try:
        if not isdir(abspath(join(dest, pardir))):
            makedirs(abspath(join(dest, pardir)))
        move(src, dest)
        return True
    except Exception as e:
        print(e)
        return False


def is_dir_or_file(file_path):
    result = False
    if isdir(file_path):
        result = True
    if isfile(file_path):
        result = True
    return result


def make_tarfile(src, dest, compressed=True, compresslevel=1, remove_src=False):
    """Creates a TAR file.

    Args:
        src (str): directory to serialize.
        dest(str): file path for TAR file to be created.
        compressed (bool): whether the TAR file should be compressed.
        compresslevel (int): from 0 to 9 controlling the level of compression
        remove_src (bool): whether the src should be deleted after serialization.
    """
    if not isdir(abspath(join(dest, pardir))):
        makedirs(abspath(join(dest, pardir)))
    if compressed:
        with tarfile.open(dest, "w:gz", compresslevel=compresslevel) as tar:
            tar.add(src, arcname=basename(src))
    else:
        with tarfile.open(dest, "w") as tar:
            tar.add(src, arcname=basename(src))
    if remove_src:
        rmtree(src)
    return dest


def anon_extract_all(file_path, tmp_dir):
    """Extracts the contents of a serialized file.

    Handles directories, ZIP and TAR files.

    Args:
        file_path (str): file path for a serialized file.
        tmp_dir (str): file path of the location in which to extract the file.
    """
    extracted = False
    if isdir(file_path):
        extracted = dir_extract_all(file_path, tmp_dir)
    else:
        if file_path.endswith("tar.gz") or file_path.endswith(".tar"):
            extracted = tar_extract_all(file_path, tmp_dir)
        if file_path.endswith(".zip"):
            extracted = zip_extract_all(file_path, tmp_dir)
    return extracted


def zip_extract_all(file_path, tmp_dir):
    """Extracts the contents of a ZIP file."""
    extracted = False
    try:
        zf = zipfile.ZipFile(file_path, "r")
        zf.extractall(tmp_dir)
        zf.close()
        extracted = tmp_dir
    except Exception as e:
        print("Error extracting ZIP file: {}".format(e))
    return extracted


def tar_extract_all(file_path, tmp_dir):
    """Extracts the contents of a TAR file."""
    extracted = False
    try:
        tf = tarfile.open(file_path, "r:*")
        tf.extractall(tmp_dir)
        tf.close()
        extracted = tmp_dir
    except Exception as e:
        print("Error extracting TAR file: {}".format(e))
    return extracted


def dir_extract_all(file_path, tmp_dir):
    """Extracts the contents of a directory."""
    extracted = False
    try:
        target = join(tmp_dir, basename(file_path))
        if is_dir_or_file(target):
            rmtree(target)
        copytree(file_path, target)
        extracted = target
    except Exception as e:
        return e
        print("Error extracting a directory: {}".format(e))
    return extracted
