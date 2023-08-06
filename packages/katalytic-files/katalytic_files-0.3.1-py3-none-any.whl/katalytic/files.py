import itertools
import re
import shutil
from pathlib import Path

from katalytic.pkg import get_version

__version__, __version_info__ = get_version(__name__, __package__)


def clear_dir(path, *, create_missing=True):
    """This function is not named "empty_dir" to avoid confusing it with "is_dir_empty"."""
    if not isinstance(create_missing, bool):
        raise TypeError(f'<create_missing> expects False or True. Got {type(create_missing)}')

    path = Path(path)
    delete_dir(path, missing_ok=True, non_empty_dir=True)
    if create_missing:
        make_dir(path)

    assert is_dir_empty(path, missing=True)


def copy_dir(src, dest, *, dir_exists='error', file_exists='error', make_dirs=True):
    if dir_exists not in ('error', 'merge', 'replace', 'skip'):
        raise ValueError(f'<dir_exists> expects "error", "merge", "replace", "skip". Got {dir_exists!r}')
    elif file_exists not in ('error', 'replace', 'skip'):
        raise ValueError(f'<file_exists> expects "error", False, or True. Got {file_exists!r}')
    elif not isinstance(make_dirs, bool):
        raise TypeError(f'<make_dirs> expects False or True. Got {type(make_dirs)}')

    src = Path(src)
    dest = Path(dest)

    if not src.exists():
        raise FileNotFoundError(f'[Errno 2] <src> directory does not exist: {str(src)!r}')
    elif src.is_file():
        raise NotADirectoryError(f'[Errno 20] Expected a directory, but <src> is a file: {str(src)!r}')
    elif dest.is_file():
        raise NotADirectoryError(f'[Errno 20] Expected a directory, but <dest> is a file: {str(dest)!r}')
    elif dest.is_dir():
        if src.samefile(dest):
            raise ValueError(f'<src> and <dest> are equal: {str(src)!r}')
        elif dir_exists == 'replace':
            delete_dir(dest, non_empty_dir=True)
        elif dir_exists == 'skip':
            return

        for src_item in src.iterdir():
            dest_item = str(src_item).replace(str(src), str(dest))
            if src_item.is_dir():
                if Path(dest_item).is_dir() and dir_exists == 'error':
                    raise FileExistsError(f'[Errno 17] Directory already exists: {str(dest_item)!r}')

                copy_dir(src_item, dest_item, make_dirs=make_dirs, file_exists=file_exists, dir_exists=dir_exists)
            else:
                copy_file(src_item, dest_item, exists=file_exists)
    elif make_dirs is True:
        if src.name != dest.name:
            dest = dest/src.name

        make_dir(dest)
        copy_dir(src, dest, make_dirs=make_dirs, file_exists=file_exists, dir_exists=dir_exists)
    elif make_dirs is False:
        raise FileNotFoundError(f'[Errno 2] No such directory: {str(dest)!r}')


def copy_file(src, dest, *, exists='error', make_dirs=True):
    if exists not in ('error', 'replace', 'skip'):
        raise ValueError(f'<exists> expects "error", "replace", or "skip". Got {exists!r}')
    elif _is_none_of(make_dirs, ('error', False, True)):
        raise ValueError(f'<make_dirs> expects "error", False, or True. Got {make_dirs!r}')

    ends_with_slash = str(dest).endswith('/')
    src = Path(src)
    dest = Path(dest)

    if src.exists() and dest.exists() and src.samefile(dest):
        raise ValueError(f'<src> and <dest> are equal: {str(src)!r}')
    elif not src.exists():
        raise FileNotFoundError(f'[Errno 2] <src> file does not exist: {str(src)!r}')
    elif src.is_dir():
        raise IsADirectoryError(f'[Errno 21] Expected a file, but <src> is a directory: {str(src)!r}')
    elif dest.exists():
        if exists == 'error':
            raise FileExistsError(f'[Errno 17] File exists: {str(dest)!r}')
        elif exists == 'replace':
            shutil.copy2(src, dest)
        elif exists == 'skip':
            pass
    elif make_dirs is False:
        raise FileNotFoundError(f'[Errno 2] No such file: {str(dest)!r}')
    elif make_dirs is True:
        if ends_with_slash:
            make_dir(dest)
        else:
            make_dir(dest.parent)

        shutil.copy2(src, dest)


def delete_dir(path, *, missing_ok=True, non_empty_dir='error'):
    if path is None or path in ('', '.'):
        raise ValueError(f'path={path!r} would delete the current dir')
    elif not isinstance(missing_ok, bool):
        raise TypeError(f'<missing_ok> expects False or True. Got {type(missing_ok)}')
    elif _is_none_of(non_empty_dir, ('error', False, True)):
        raise ValueError(f'<non_empty_dir> expects "error", False, or True. Got {non_empty_dir!r}')

    path = Path(path)
    if path.is_dir():
        if non_empty_dir == 'error':
            path.rmdir()
        elif non_empty_dir is True:
            shutil.rmtree(path)
        elif non_empty_dir is False and not is_dir_empty(path):
            pass
    elif not path.exists():
        if missing_ok:
            pass
        else:
            raise FileNotFoundError(f'[Errno 2] No such directory: {str(path)!r}')
    elif path.is_file():
        raise NotADirectoryError(f'[Errno 20] Expected a directory, but <path> is a file: {str(path)!r}')


def delete_file(path, *, missing_ok=True):
    if not isinstance(missing_ok, bool):
        raise TypeError(f'<missing_ok> expects False or True. Got {type(missing_ok)}')

    path = Path(path)
    if path.is_file():
        path.unlink()
    elif not path.exists():
        if missing_ok:
            pass
        else:
            raise FileNotFoundError(f'[Errno 2] No such file: {str(path)!r}')
    elif path.is_dir():
        raise IsADirectoryError(f'[Errno 21] Expected a file, but <src> is a directory: {str(path)!r}')


def get_all(path='.', *, glob=True, iter_=False, prefix=True, recursive=False):
    return _get_all(path, glob=glob, iter_=iter_, prefix=prefix, recursive=recursive)


def get_dirs(path='.', *, glob=True, iter_=False, prefix=True, recursive=False):
    return _get_all(path, glob=glob, iter_=iter_, prefix=prefix, only_dirs=True, recursive=recursive)


def get_files(path='.', *, glob=True, iter_=False, prefix=True, recursive=False):
    return _get_all(path, glob=glob, iter_=iter_, prefix=prefix, only_files=True, recursive=recursive)


def _get_all(path='.', *, glob=True, iter_=False, only_dirs=False, only_files=False, prefix=True, recursive=False):
    if not isinstance(glob, bool):
        raise TypeError(f'<glob> expects False or True. Got {type(glob)}')
    elif not isinstance(iter_, bool):
        raise TypeError(f'<iter_> expects False or True. Got {type(iter_)}')
    elif not isinstance(only_dirs, bool):
        raise TypeError(f'<only_dirs> expects False or True. Got {type(only_dirs)}')
    elif not isinstance(only_files, bool):
        raise TypeError(f'<only_files> expects False or True. Got {type(only_files)}')
    elif not isinstance(prefix, bool):
        raise TypeError(f'<prefix> expects False or True. Got {type(prefix)}')
    elif not isinstance(recursive, bool):
        raise TypeError(f'<recursive> expects False or True. Got {type(recursive)}')
    elif only_dirs and only_files:
        raise ValueError(f'<only_dirs> and <only_files> can\'t be True at the same time')

    if glob and (path is not None and '*' in str(path)):
        path, _, pattern = str(path).partition('*')
        if recursive:
            pattern = re.sub(r'^\*/', r'**/', f'*{pattern}')
            result = Path(path).rglob(pattern)
        else:
            result = Path(path).glob(f'*{pattern}')
    else:
        result = Path(path).iterdir()
        if recursive:
            result = itertools.chain.from_iterable(
                [p] if p.is_file()
                else itertools.chain([p], _get_all(p, glob=glob, iter_=True, only_dirs=only_dirs, only_files=only_files, prefix=True, recursive=recursive))
                for p in result
            )

    if only_dirs:
        result = (p for p in result if Path(p).is_dir())
    elif only_files:
        result = (p for p in result if Path(p).is_file())

    if prefix:
        result = (str(p) for p in result)
    else:
        result = (str(p).replace(f'{path}/', '', 1) for p in result)

    if iter_:
        return result
    else:
        return sorted(result)


def get_unique_path(pattern='/tmp/{}'):
    if not isinstance(pattern, (str, Path)):
        raise TypeError(f'<pattern> expects a str or pathlib.Path. Got {type(pattern)}')

    pattern = str(pattern)
    placeholders = re.findall(r'{(:((\d*)?d)?)?}', pattern)
    if len(placeholders) != 1:
        raise ValueError(f'Invalid pattern: {pattern!r}.' + 'You must provide exactly one placeholder, optionally with an integer format. Try using "{}" or "{:03d}"')

    n = 0
    while True:
        n += 1
        path = pattern.format(n)
        if not Path(path).exists():
            return path


def is_dir_empty(path, *, missing='error'):
    if _is_none_of(missing, (False, True, 'error')):
        raise ValueError(f'<missing> expects "error", False, or True. Got {missing!r}')

    path = Path(path)
    if path.is_file():
        raise NotADirectoryError(f'[Errno 20] Expected a directory, but "path" is a file: {str(path)!r}')
    elif not path.exists():
        if missing is False:
            return False
        elif missing is True:
            return True
        elif missing == 'error':
            raise FileNotFoundError(f'[Errno 2] No such file or directory: {str(path)!r}')
    else:
        return list(path.iterdir()) == []


def make_dir(path, *, create_parents=True, exists_ok=True):
    if not isinstance(create_parents, bool):
        raise TypeError(f'<create_parents> expects False or True. Got {type(create_parents)}')
    elif not isinstance(exists_ok, bool):
        raise TypeError(f'<exists_ok> expects False or True. Got {type(exists_ok)}')

    path = Path(path)
    if path.is_file():
        raise NotADirectoryError(f'[Errno 20] Expected a directory, but "path" is a file: {str(path)!r}')

    path.mkdir(parents=create_parents, exist_ok=exists_ok)


def move_dir(src, dest, *, dir_exists='error', file_exists='error', make_dirs=True):
    if dir_exists == 'skip' and Path(dest).exists():
        return

    copy_dir(src, dest, dir_exists=dir_exists, file_exists=file_exists, make_dirs=make_dirs)
    delete_dir(src, non_empty_dir=True)


def move_file(src, dest, *, exists='error', make_dirs=True):
    if exists == 'skip' and Path(dest).exists():
        return

    copy_file(src, dest, exists=exists, make_dirs=make_dirs)
    delete_file(src)


def _is_any_of(obj, options):
    """Required when you have singletons (None, False, True) in the options"""
    if _is_singleton(obj):
        return any((obj is option) for option in options)
    else:
        return any((obj == option) for option in options if not _is_singleton(option))


def _is_none_of(obj, options):
    """Required when you have singletons (None, False, True) in the options"""
    return not _is_any_of(obj, options)


def _is_singleton(obj):
    return obj is None or isinstance(obj, bool)
