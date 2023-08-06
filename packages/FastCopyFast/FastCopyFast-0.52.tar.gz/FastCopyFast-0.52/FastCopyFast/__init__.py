# based on this answer: https://stackoverflow.com/a/28129677/15096247
import os
import shutil
import sys
from typing import Union

config = sys.modules[__name__]
config.BUFFER_SIZE = 100 * 1024


class CTError(Exception):
    def __init__(self, errors):
        self.errors = errors


try:
    O_BINARY = os.O_BINARY
except:
    O_BINARY = 0
READ_FLAGS = os.O_RDONLY | O_BINARY
WRITE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | O_BINARY


def copyfile(src: str, dst: str, copystat: bool = False) -> bool:
    copyok = False
    try:
        fin = os.open(src, READ_FLAGS)
        stat = os.fstat(fin)
        fout = os.open(dst, WRITE_FLAGS, stat.st_mode)
        for x in iter(lambda: os.read(fin, config.BUFFER_SIZE), b""):
            os.write(fout, x)
        copyok = True
    finally:
        try:
            os.close(fin)
        except Exception:
            pass
        try:
            os.close(fout)
        except Exception:
            pass
    if copystat and copyok:
        try:
            shutil.copystat(src, dst)
            return True
        except Exception:
            return False
    if copyok:
        return True
    return False


def movefile(src: str, dst: str, copystat: bool = False) -> bool:
    copyok = False
    try:
        fin = os.open(src, READ_FLAGS)
        stat = os.fstat(fin)
        fout = os.open(dst, WRITE_FLAGS, stat.st_mode)
        for x in iter(lambda: os.read(fin, config.BUFFER_SIZE), b""):
            os.write(fout, x)
        copyok = True
    finally:
        try:
            os.close(fin)
        except Exception:
            pass
        try:
            os.close(fout)
        except Exception:
            pass
    if copystat and copyok:
        try:
            shutil.copystat(src, dst)
        except Exception:
            return False
    if copyok:
        try:
            os.remove(src)
            return True

        except Exception:
            return False
    return False


def copytree(
    src: str,
    dst: str,
    ignore: Union[list, type(None)] = None,
    symlinks: bool = False,
    copystat: bool = False,
    ignore_exceptions=True,
):
    if ignore is None:
        ignore = []
    names = os.listdir(src)

    if not os.path.exists(dst):
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignore:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, ignore, symlinks)
            else:
                copyfile(srcname, dstname, copystat)

        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        except CTError as err:
            errors.extend(err.errors)
            print(err)
    if errors:
        if not ignore_exceptions:
            raise CTError(errors)
