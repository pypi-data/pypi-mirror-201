import collections
import shutil
import tempfile
from pathlib import Path

import pytest

from katalytic.files import _get_all, clear_dir, copy_dir, copy_file, delete_dir, delete_file, get_dirs, get_files, get_unique_path, is_dir_empty, get_all, make_dir, move_dir, move_file


class TestGroup_copy:
    class Test_copy_dir:
        def test_dest_is_dir(self):
            src = Path(_setup_tree('/tmp/{}_src'))

            dest = Path(get_unique_path('/tmp/{}_dest'))
            copy_dir(src, dest)
            _check_tree(src, dest/src.name)

            dest_2 = Path(get_unique_path('/tmp/{}_dest_2'))
            copy_dir(src, dest_2/src.name)
            _check_tree(src, dest_2/src.name)

        def test_dest_is_file(self):
            with pytest.raises(NotADirectoryError):
                src = _setup_dir()
                dest = _setup_file()
                copy_dir(src, dest)

        def test_dir_exists_error(self):
            with pytest.raises(FileExistsError):
                src = _setup_tree()
                dest = _setup_tree()
                copy_dir(src, dest, dir_exists='error', file_exists='skip')

        def test_dir_exists_merge(self):
            src, src_file = _setup_dir_and_file()
            _setup_tree(src + '/{}')

            dest = _setup_tree()
            copy_dir(src, dest, dir_exists='merge', file_exists='skip')

            src_dirs = get_dirs(src, prefix=False, recursive=True)
            dest_dirs = get_dirs(dest, prefix=False, recursive=True)
            assert set(src_dirs).difference(dest_dirs) == set()
            assert set(dest_dirs).difference(src_dirs) != set()

        def test_dir_exists_replace(self):
            src, src_file = _setup_dir_and_file()
            dest = _setup_tree()
            copy_dir(src, dest, dir_exists='replace', file_exists='skip')

            src_tree = get_all(src, prefix=False, recursive=True)
            dest_tree = get_all(dest, prefix=False, recursive=True)
            assert src_tree == dest_tree

            src_tree = set(get_all(src, recursive=True))
            dest_tree = set(get_all(dest, recursive=True))
            pairs = {(fn, fn.replace(src, dest)) for fn in src_tree | dest_tree}
            pairs = {(Path(s), Path(d)) for s, d in pairs if Path(s).is_file()}
            assert all((s.read_text() == d.read_text()) for s, d in pairs)

        def test_dir_exists_skip(self):
            src, src_file = _setup_dir_and_file()
            dest, dest_file = _setup_dir_and_file()
            make_dir(f'{dest}/subdir')

            copy_dir(src, dest, dir_exists='skip', file_exists='replace')
            assert Path(dest_file).read_text() != Path(src_file).read_text()
            assert Path(f'{dest}/subdir').is_dir()

        def test_file_exists_error(self):
            with pytest.raises(FileExistsError):
                src = _setup_tree()
                dest = _setup_tree()
                copy_dir(src, dest, dir_exists='merge', file_exists='error')

        def test_file_exists_replace(self):
            src, src_file = _setup_dir_and_file()
            dest, dest_file = _setup_dir_and_file()

            copy_dir(src, dest, dir_exists='merge', file_exists='replace')
            assert Path(dest_file).read_text() == Path(src_file).read_text()

        def test_file_exists_skip(self):
            src, src_file = _setup_dir_and_file()
            dest, dest_file = _setup_dir_and_file()

            original = Path(dest_file).read_text()
            copy_dir(src, dest, dir_exists='merge', file_exists='skip')
            assert Path(dest_file).read_text() != Path(src_file).read_text()
            assert Path(dest_file).read_text() == original

        def test_make_dirs_false(self):
            with pytest.raises(FileNotFoundError):
                with tempfile.TemporaryDirectory() as d:
                    src = get_unique_path(d + '/{}_src')
                    dest = get_unique_path(d + '/{}_dest')
                    make_dir(src)
                    copy_dir(src, dest, make_dirs=False)

        def test_make_dirs_true(self):
            with tempfile.TemporaryDirectory() as d:
                src = _setup_tree()
                src_name = Path(src).name

                dest = get_unique_path(d + '/{}_dest')
                copy_dir(src, dest, make_dirs=True)
                _check_tree(src, f'{dest}/{src_name}')

                dest_2 = get_unique_path(d + '/{}_dest_2')
                copy_dir(src, f'{dest_2}/{src_name}', make_dirs=True)
                _check_tree(src, f'{dest_2}/{src_name}')

        def test_same_path(self):
            with pytest.raises(ValueError):
                src = _setup_dir()
                copy_dir(src, src)

        def test_src_is_file(self):
            with pytest.raises(NotADirectoryError):
                src = _setup_file()
                dest = get_unique_path('/tmp/{}_new')
                copy_dir(src, dest)

        def test_src_is_missing(self):
            with pytest.raises(FileNotFoundError):
                src = get_unique_path()
                copy_dir(src, f'{src}_copy')

        @pytest.mark.parametrize('mistake', [0, None, {}, True])
        def test_precondition_dest(self, mistake):
            with pytest.raises(TypeError):
                copy_dir('src', mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, True, 'hello'])
        def test_precondition_dir_exists(self, mistake):
            with pytest.raises(ValueError):
                copy_dir('src', 'dest', dir_exists=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, 'hello'])
        def test_precondition_file_exists(self, mistake):
            with pytest.raises(ValueError):
                copy_dir('src', 'dest', file_exists=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_make_dirs(self, mistake):
            with pytest.raises(TypeError):
                src, dest = _setup_dir(n=2)
                copy_dir(src, dest, make_dirs=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, True])
        def test_precondition_src(self, mistake):
            with pytest.raises(TypeError):
                copy_dir(mistake, 'dest')

    class Test_copy_file:
        def test_dir(self):
            with pytest.raises(IsADirectoryError):
                src = _setup_dir()
                dest = get_unique_path()
                copy_file(src, dest)

        def test_exists_error(self):
            with pytest.raises(FileExistsError):
                src, dest = _setup_file(n=2)
                copy_file(src, dest, exists='error')

        def test_exists_replace(self):
            src, dest = _setup_file(n=2)
            copy_file(src, dest, exists='replace')

            text = Path(dest).read_text()
            assert text == Path(src).read_text()
            assert text != dest

        def test_exists_skip(self):
            src, dest = _setup_file(n=2)
            copy_file(src, dest, exists='skip')

            text = Path(dest).read_text()
            assert text != Path(src).read_text()
            assert text == dest

        def test_missing(self):
            dest = _setup_file()
            src = get_unique_path()
            with pytest.raises(FileNotFoundError):
                copy_file(src, dest)

        def test_ends_with_slash(self):
            src = _setup_file()
            root = get_unique_path()
            dest = root + '/1/2/3/'
            copy_file(src, dest)

        def test_make_dirs_false(self):
            with pytest.raises(FileNotFoundError):
                src = _setup_file()
                dest = get_unique_path('/tmp/{}/a/b/c/')
                copy_file(src, dest, make_dirs=False)

        def test_make_dirs_true(self):
            src = _setup_file()
            dest = _setup_path()
            copy_file(src, dest, make_dirs=True)
            assert Path(dest).read_text() == src

        def test_same_path(self):
            with pytest.raises(ValueError):
                src = _setup_file()
                copy_file(src, src)

        @pytest.mark.parametrize('mistake', [0, None, {}, True])
        def test_precondition_src(self, mistake):
            with pytest.raises(TypeError):
                copy_file(mistake, 'a')

        @pytest.mark.parametrize('mistake', [0, None, {}, True])
        def test_precondition_dest(self, mistake):
            with pytest.raises(TypeError):
                copy_file('a', mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, 'hello'])
        def test_precondition_make_dirs(self, mistake):
            with pytest.raises(ValueError):
                src, dest = _setup_file(n=2)
                copy_file(src, dest, make_dirs=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, 'hello'])
        def test_precondition_exists(self, mistake):
            src, dest = _setup_file(n=2)
            with pytest.raises(ValueError):
                copy_file(src, dest, exists=mistake)


class TestGroup_delete:
    class Test_delete_dir:
        def test_file(self):
            with pytest.raises(NotADirectoryError):
                path = _setup_file()
                delete_dir(path)

        def test_empty_dir(self):
            path = _setup_dir()
            delete_dir(path)
            assert not Path(path).exists()

        def test_missing_ok_false(self):
            with pytest.raises(FileNotFoundError):
                path = get_unique_path()
                delete_dir(path, missing_ok=False)

        def test_missing_ok_true(self):
            path = get_unique_path()
            delete_dir(path, missing_ok=True)
            assert not Path(path).exists()

        def test_non_empty_dir_false(self):
            path, _ = _setup_dir_and_file()
            delete_dir(path, non_empty_dir=False)
            assert Path(path).is_dir()

        def test_non_empty_dir_error(self):
            with pytest.raises(OSError):
                path, _ = _setup_dir_and_file()
                delete_dir(path, non_empty_dir='error')

        def test_non_empty_dir_true(self):
            path, _ = _setup_dir_and_file()
            delete_dir(path, non_empty_dir=True)
            assert not Path(path).exists()

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_missing_ok(self, mistake):
            with pytest.raises(TypeError):
                delete_dir(get_unique_path(), missing_ok=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_non_empty_dir(self, mistake):
            with pytest.raises(ValueError):
                delete_dir(get_unique_path(), non_empty_dir=mistake)

        @pytest.mark.parametrize('mistake', [None, '', '.'])
        def test_precondition_path_current_dir(self, mistake):
            with pytest.raises(ValueError):
                delete_dir(mistake)

        @pytest.mark.parametrize('mistake', [0, {}, True])
        def test_precondition_path_type(self, mistake):
            with pytest.raises(TypeError):
                delete_dir(mistake)

    class Test_delete_file:
        def test_dir(self):
            with pytest.raises(IsADirectoryError):
                path = _setup_dir()
                delete_file(path)

        def test_file(self):
            path = _setup_file()
            delete_file(path)
            assert not Path(path).exists()

        def test_missing_ok_false(self):
            with pytest.raises(FileNotFoundError):
                path = get_unique_path()
                delete_file(path, missing_ok=False)

        def test_missing_ok_true(self):
            path = get_unique_path()
            delete_file(path, missing_ok=True)
            assert not Path(path).exists()

        @pytest.mark.parametrize('mistake', [0, None, {}, True])
        def test_precondition_path(self, mistake):
            with pytest.raises(TypeError):
                delete_file(mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_missing_ok(self, mistake):
            with pytest.raises(TypeError):
                delete_file(get_unique_path(), missing_ok=mistake)


class TestGroup_get:
    class Test_get_all:
        def test_prefix_false(self):
            path = _setup_tree()
            expected = ['1.txt', 'a', 'a/2.txt', 'b', 'b/3.txt', 'b/c', 'b/c/4.txt']
            assert get_all(path, prefix=False, recursive=True) == expected

        def test_prefix_true(self):
            path = _setup_tree()
            expected = [
                f'{path}/1.txt',
                f'{path}/a',
                f'{path}/a/2.txt',
                f'{path}/b',
                f'{path}/b/3.txt',
                f'{path}/b/c',
                f'{path}/b/c/4.txt'
            ]
            assert get_all(path, prefix=True, recursive=True) == expected

        def test_path_is_file(self):
            with pytest.raises(NotADirectoryError):
                path = _setup_file()
                get_all(path)

        def test_path_is_missing(self):
            with pytest.raises(FileNotFoundError):
                get_all(get_unique_path())

        def test_iter(self):
            r = get_all('', iter_=True)
            assert isinstance(r, collections.abc.Iterator)

        def test_glob(self):
            path = _setup_tree_2()
            assert get_all(f'{path}/*/a/*') == [f'{path}/a/a/6.py', f'{path}/b/a/5.py']

        def test_glob_recursive(self):
            path = _setup_tree_2()
            expected = sorted(map(str, Path(path).glob('**/a/*')))
            assert get_all(f'{path}/**/a/*') == expected
            assert get_all(f'{path}/*/a/*', recursive=True) == expected

            expected = sorted(map(str, Path(path).glob('**/a/**')))
            assert get_all(f'{path}/**/a/**') == expected
            assert get_all(f'{path}/**/a/**', recursive=True) == expected

        def test_only_dirs(self):
            path = _setup_tree()
            assert _get_all(path, only_dirs=True, prefix=False) == ['a', 'b']

        def test_only_files(self):
            path = _setup_tree()
            assert _get_all(path, only_files=True, prefix=False) == ['1.txt']

        def test_only_conflict(self):
            with pytest.raises(ValueError):
                _get_all('', only_files=True, only_dirs=True)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_glob(self, mistake):
            with pytest.raises(TypeError):
                get_all('', glob=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_iter_(self, mistake):
            with pytest.raises(TypeError):
                get_all('', iter_=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_only_dirs(self, mistake):
            with pytest.raises(TypeError):
                _get_all('', only_dirs=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_only_files(self, mistake):
            with pytest.raises(TypeError):
                _get_all('', only_files=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, True])
        def test_precondition_path(self, mistake):
            with pytest.raises(TypeError):
                get_all(mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_prefix(self, mistake):
            with pytest.raises(TypeError):
                get_all('', prefix=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_recursive(self, mistake):
            with pytest.raises(TypeError):
                get_all('', recursive=mistake)

        def test_recursive(self):
            path = _setup_tree()
            assert set(get_all(path, recursive=True)) == {
                f'{path}/1.txt',
                f'{path}/a',
                f'{path}/a/2.txt',
                f'{path}/b',
                f'{path}/b/3.txt',
                f'{path}/b/c',
                f'{path}/b/c/4.txt',
            }

        def test_sorted(self):
            path = _setup_tree()
            _ = _setup_tree(path + '/b/{}')
            assert get_all(path, iter_=False, recursive=True) == [
                f'{path}/1.txt',
                f'{path}/a',
                f'{path}/a/2.txt',
                f'{path}/b',
                f'{path}/b/1',
                f'{path}/b/1/1.txt',
                f'{path}/b/1/a',
                f'{path}/b/1/a/2.txt',
                f'{path}/b/1/b',
                f'{path}/b/1/b/3.txt',
                f'{path}/b/1/b/c',
                f'{path}/b/1/b/c/4.txt',
                f'{path}/b/3.txt',
                f'{path}/b/c',
                f'{path}/b/c/4.txt',
            ]

    class Test_get_dirs:
        def test_prefix_false(self):
            path = _setup_tree()
            assert get_dirs(path, prefix=False, recursive=True) == ['a', 'b', 'b/c']

        def test_prefix_true(self):
            path = _setup_tree()
            expected = [f'{path}/a', f'{path}/b', f'{path}/b/c']
            assert get_dirs(path, prefix=True, recursive=True) == expected

        def test_path_is_file(self):
            with pytest.raises(NotADirectoryError):
                path = _setup_file()
                get_dirs(path)

        def test_path_is_missing(self):
            with pytest.raises(FileNotFoundError):
                get_dirs(get_unique_path())

        def test_iter(self):
            r = get_dirs('', iter_=True)
            assert isinstance(r, collections.abc.Iterator)

        def test_glob(self):
            path = _setup_tree_2()
            assert get_dirs(f'{path}/*/a') == [f'{path}/a/a', f'{path}/b/a']

        def test_glob_recursive(self):
            path = _setup_tree_2()
            expected = [f'{path}/a', f'{path}/a/a', f'{path}/b/a', f'{path}/b/c/a']
            assert get_dirs(f'{path}/**/a') == expected
            assert get_dirs(f'{path}/*/a', recursive=True) == expected

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_prefix(self, mistake):
            with pytest.raises(TypeError):
                get_dirs('', prefix=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_glob(self, mistake):
            with pytest.raises(TypeError):
                get_dirs('', glob=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_iter_(self, mistake):
            with pytest.raises(TypeError):
                get_dirs('', iter_=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, True])
        def test_precondition_path(self, mistake):
            with pytest.raises(TypeError):
                get_dirs(mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_recursive(self, mistake):
            with pytest.raises(TypeError):
                get_dirs('', recursive=mistake)

        def test_recursive(self):
            path = _setup_tree()
            assert set(get_dirs(path, recursive=True)) == {
                f'{path}/a',
                f'{path}/b',
                f'{path}/b/c',
            }

        def test_sorted(self):
            path = _setup_tree()
            _ = _setup_tree(path + '/b/{}')
            assert get_dirs(path, iter_=False, recursive=True) == [
                f'{path}/a',
                f'{path}/b',
                f'{path}/b/1',
                f'{path}/b/1/a',
                f'{path}/b/1/b',
                f'{path}/b/1/b/c',
                f'{path}/b/c',
            ]

    class Test_get_files:
        def test_prefix_false(self):
            path = _setup_tree()
            expected = ['1.txt', 'a/2.txt', 'b/3.txt', 'b/c/4.txt']
            assert get_files(path, prefix=False, recursive=True) == expected

        def test_prefix_true(self):
            path = _setup_tree()
            expected = [
                f'{path}/1.txt',
                f'{path}/a/2.txt',
                f'{path}/b/3.txt',
                f'{path}/b/c/4.txt'
            ]
            assert get_files(path, prefix=True, recursive=True) == expected

        def test_path_is_file(self):
            with pytest.raises(NotADirectoryError):
                path = _setup_file()
                get_files(path)

        def test_path_is_missing(self):
            with pytest.raises(FileNotFoundError):
                get_files(get_unique_path())

        def test_iter(self):
            r = get_files('', iter_=True)
            assert isinstance(r, collections.abc.Iterator)

        def test_glob(self):
            path = _setup_tree_2()
            assert get_files(f'{path}/*.py') == [f'{path}/1.py']

        def test_glob_recursive(self):
            path = _setup_tree_2()
            expected = [f'{path}/1.py', f'{path}/a/2.py', f'{path}/a/a/6.py', f'{path}/b/a/5.py']
            assert get_files(f'{path}/**/*.py') == expected

        def test_only_conflict(self):
            with pytest.raises(ValueError):
                _get_all('', only_files=True, only_dirs=True)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_prefix(self, mistake):
            with pytest.raises(TypeError):
                get_files('', prefix=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_glob(self, mistake):
            with pytest.raises(TypeError):
                get_files('', glob=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_iter_(self, mistake):
            with pytest.raises(TypeError):
                get_files('', iter_=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, True])
        def test_precondition_path(self, mistake):
            with pytest.raises(TypeError):
                get_files(mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_recursive(self, mistake):
            with pytest.raises(TypeError):
                get_files('', recursive=mistake)

        def test_recursive(self):
            path = _setup_tree()
            assert set(get_files(path, recursive=True)) == {
                f'{path}/1.txt',
                f'{path}/a/2.txt',
                f'{path}/b/3.txt',
                f'{path}/b/c/4.txt',
            }

        def test_sorted(self):
            path = _setup_tree()
            _ = _setup_tree(path + '/b/{}')
            assert get_files(path, iter_=False, recursive=True) == [
                f'{path}/1.txt',
                f'{path}/a/2.txt',
                f'{path}/b/1/1.txt',
                f'{path}/b/1/a/2.txt',
                f'{path}/b/1/b/3.txt',
                f'{path}/b/1/b/c/4.txt',
                f'{path}/b/3.txt',
                f'{path}/b/c/4.txt',
            ]


class TestGroup_misc_dir:
    class Test_clear_dir:
        def test_clear_empty(self):
            path = _setup_dir()
            clear_dir(path)
            assert list(Path(path).iterdir()) == []

        def test_clear_non_empty(self):
            path, _ = _setup_dir_and_file()
            clear_dir(path)
            assert list(Path(path).iterdir()) == []

        def test_create_missing_false(self):
            d = get_unique_path()
            shutil.rmtree(d, ignore_errors=True)
            clear_dir(d, create_missing=False)
            assert not Path(d).exists()

        def test_create_missing_true(self):
            path = get_unique_path()
            clear_dir(path, create_missing=True)
            assert is_dir_empty(path)

        def test_is_file(self):
            with pytest.raises(NotADirectoryError):
                file = _setup_file()
                clear_dir(file)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_create_missing(self, mistake):
            path = get_unique_path()
            with pytest.raises(TypeError):
                clear_dir(path, create_missing=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, True])
        def test_precondition_path(self, mistake):
            with pytest.raises(TypeError):
                clear_dir(mistake)

    class Test_is_dir_empty:
        def test_empty(self):
            path = _setup_dir()
            assert is_dir_empty(path)

        def test_is_file(self):
            with pytest.raises(NotADirectoryError):
                path = _setup_file()
                is_dir_empty(path)

        def test_missing_error(self):
            with pytest.raises(FileNotFoundError):
                is_dir_empty(get_unique_path(), missing='error')

        def test_missing_false(self):
            path = get_unique_path()
            assert is_dir_empty(path, missing=False) is False

        def test_missing_true(self):
            path = get_unique_path()
            assert is_dir_empty(path, missing=True) is True

        def test_non_empty(self):
            path, _ = _setup_dir_and_file()
            assert not is_dir_empty(path)

        @pytest.mark.parametrize('mistake', [[], '', 0, None])
        def test_precondition_missing(self, mistake):
            with pytest.raises(ValueError):
                path = get_unique_path()
                is_dir_empty(path, missing=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, True])
        def test_precondition_path(self, mistake):
            with pytest.raises(TypeError):
                is_dir_empty(mistake)

    class Test_mkdir:
        def test_create(self):
            path = _setup_dir()
            assert Path(path).is_dir()

            path = _setup_dir('/tmp/a/{}/b')
            assert Path(path).is_dir()

        def test_exists_error(self):
            with pytest.raises(FileExistsError):
                path = _setup_dir()
                make_dir(path, exists_ok=False)

        def test_exists_ok(self):
            path = _setup_dir()
            make_dir(path, exists_ok=True)
            assert Path(path).is_dir()

        def test_idempotency(self):
            path = _setup_dir()
            make_dir(path)
            assert Path(path).is_dir()

        def test_is_file(self):
            with pytest.raises(NotADirectoryError):
                path = _setup_file()
                make_dir(path)

        def test_no_parents(self):
            with pytest.raises(FileNotFoundError):
                d = get_unique_path('/tmp/parent/{}/child')
                make_dir(d, create_parents=False)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_create_parents(self, mistake):
            with pytest.raises(TypeError):
                make_dir(get_unique_path(), create_parents=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_exists_ok(self, mistake):
            with pytest.raises(TypeError):
                make_dir(get_unique_path(), exists_ok=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, True])
        def test_precondition_path(self, mistake):
            with pytest.raises(TypeError):
                make_dir(mistake)


class TestGroup_move:
    class Test_move_dir:
        def test_dest_is_dir(self):
            src = Path(_setup_tree('/tmp/{}_src'))
            src_copy = Path(get_unique_path('/tmp/{}_src_copy'))
            copy_dir(src, src_copy)

            dest = get_unique_path('/tmp/{}_dest')
            move_dir(src, dest)
            _check_tree(src_copy, dest)
            assert not src.exists()

            src = Path(_setup_tree('/tmp/{}_src'))
            src_copy = Path(get_unique_path('/tmp/{}_src_copy'))
            copy_dir(src, src_copy)

            dest = Path(get_unique_path('/tmp/{}_dest'))
            move_dir(src, dest/src.name)
            _check_tree(src_copy/src.name, dest/src.name)
            assert not src.exists()

        def test_dest_is_file(self):
            with pytest.raises(NotADirectoryError):
                src = _setup_dir()
                dest = _setup_file()
                move_dir(src, dest)

        def test_dir_exists_error(self):
            with pytest.raises(FileExistsError):
                src = _setup_tree()
                dest = _setup_tree()
                move_dir(src, dest, dir_exists='error', file_exists='skip')

        def test_dir_exists_merge(self):
            src, src_file = _setup_dir_and_file()
            _setup_tree(src + '/{}')
            src_dirs = get_dirs(src, prefix=False, recursive=True)

            dest = _setup_tree()
            move_dir(src, dest, dir_exists='merge', file_exists='skip')

            dest_dirs = get_dirs(dest, prefix=False, recursive=True)
            assert set(src_dirs).difference(dest_dirs) == set()
            assert set(dest_dirs).difference(src_dirs) != set()

        def test_dir_exists_replace(self):
            src, src_file = _setup_dir_and_file()
            src_tree = get_all(src, prefix=False, recursive=True)
            src_tree_2 = set(get_all(src, recursive=True))

            dest = _setup_tree()
            move_dir(src, dest, dir_exists='replace', file_exists='skip')

            dest_tree = get_all(dest, prefix=False, recursive=True)
            assert src_tree == dest_tree

            dest_tree = set(get_all(dest, recursive=True))
            pairs = {(fn, fn.replace(src, dest)) for fn in src_tree_2 | dest_tree}
            pairs = {(Path(s), Path(d)) for s, d in pairs if Path(s).is_file()}
            assert all((s.read_text() == d.read_text()) for s, d in pairs)

        def test_dir_exists_skip(self):
            src, src_file = _setup_dir_and_file()
            dest, dest_file = _setup_dir_and_file()
            make_dir(f'{dest}/subdir')

            move_dir(src, dest, dir_exists='skip', file_exists='replace')
            assert Path(dest_file).read_text() != Path(src_file).read_text()
            assert Path(f'{dest}/subdir').is_dir()

        def test_file_exists_error(self):
            with pytest.raises(FileExistsError):
                src = _setup_tree()
                dest = _setup_tree()
                move_dir(src, dest, dir_exists='merge', file_exists='error')

        def test_file_exists_replace(self):
            src, src_file = _setup_dir_and_file()
            dest, dest_file = _setup_dir_and_file()
            src_file_text = Path(src_file).read_text()

            move_dir(src, dest, dir_exists='merge', file_exists='replace')
            assert Path(dest_file).read_text() == src_file_text

        def test_file_exists_skip(self):
            src, src_file = _setup_dir_and_file()
            dest, dest_file = _setup_dir_and_file()

            src_file_text = Path(src_file).read_text()
            original = Path(dest_file).read_text()

            move_dir(src, dest, dir_exists='merge', file_exists='skip')
            assert Path(dest_file).read_text() != src_file_text
            assert Path(dest_file).read_text() == original

        def test_make_dirs_false(self):
            with pytest.raises(FileNotFoundError):
                with tempfile.TemporaryDirectory() as d:
                    src = get_unique_path(d + '/{}_src')
                    dest = get_unique_path(d + '/{}_dest')
                    make_dir(src)
                    move_dir(src, dest, make_dirs=False)

        def test_make_dirs_true(self):
            with tempfile.TemporaryDirectory() as d:
                src = _setup_tree()
                src_name = Path(src).name
                src_copy = Path(get_unique_path('/tmp/{}_src_copy'))
                copy_dir(src, src_copy)

                dest = get_unique_path(d + '/{}_dest')
                move_dir(src, dest, make_dirs=True)
                _check_tree(src_copy/src_name, f'{dest}/{src_name}')

                src = _setup_tree()
                src_name = Path(src).name
                src_copy = Path(get_unique_path('/tmp/{}_src_copy'))
                copy_dir(src, src_copy)

                dest_2 = get_unique_path(d + '/{}_dest_2')
                move_dir(src, f'{dest_2}/{src_name}', make_dirs=True)
                _check_tree(src_copy/src_name, f'{dest_2}/{src_name}')

        def test_same_path(self):
            with pytest.raises(ValueError):
                src = _setup_dir()
                move_dir(src, src)

        def test_src_is_file(self):
            with pytest.raises(NotADirectoryError):
                src = _setup_file()
                dest = get_unique_path('/tmp/{}_new')
                move_dir(src, dest)

        def test_src_is_missing(self):
            with pytest.raises(FileNotFoundError):
                src = get_unique_path()
                move_dir(src, f'{src}_copy')

        @pytest.mark.parametrize('mistake', [0, None, {}, True])
        def test_precondition_dest(self, mistake):
            with pytest.raises(TypeError):
                move_dir('src', mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, True, 'hello'])
        def test_precondition_dir_exists(self, mistake):
            with pytest.raises(ValueError):
                move_dir('src', 'dest', dir_exists=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, 'hello'])
        def test_precondition_file_exists(self, mistake):
            with pytest.raises(ValueError):
                move_dir('src', 'dest', file_exists=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, ''])
        def test_precondition_make_dirs(self, mistake):
            with pytest.raises(TypeError):
                src, dest = _setup_dir(n=2)
                move_dir(src, dest, make_dirs=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, True])
        def test_precondition_src(self, mistake):
            with pytest.raises(TypeError):
                move_dir(mistake, 'dest')

    class Test_move_file:
        def test_dir(self):
            with pytest.raises(IsADirectoryError):
                src = _setup_dir()
                dest = get_unique_path()
                move_file(src, dest)

        def test_exists_error(self):
            with pytest.raises(FileExistsError):
                src, dest = _setup_file(n=2)
                move_file(src, dest, exists='error')

        def test_exists_replace(self):
            src, dest = _setup_file(n=2)
            expected_text = Path(src).read_text()
            move_file(src, dest, exists='replace')

            text = Path(dest).read_text()
            assert text == expected_text
            assert text != dest
            assert not Path(src).exists()

        def test_exists_skip(self):
            src, dest = _setup_file(n=2)
            move_file(src, dest, exists='skip')

            text = Path(dest).read_text()
            assert text != Path(src).read_text()
            assert text == dest
            assert Path(src).exists()

        def test_make_dirs_false(self):
            with pytest.raises(FileNotFoundError):
                src = _setup_file()
                dest = get_unique_path('/tmp/{}/a/b/c/')
                move_file(src, dest, make_dirs=False)

        def test_make_dirs_true(self):
            src = _setup_file()
            dest = _setup_path()
            move_file(src, dest, make_dirs=True)
            assert Path(dest).read_text() == src
            assert not Path(src).exists()

        def test_same_path(self):
            with pytest.raises(ValueError):
                src = _setup_file()
                move_file(src, src)

        @pytest.mark.parametrize('mistake', [0, None, {}, True])
        def test_precondition_src(self, mistake):
            with pytest.raises(TypeError):
                move_file(mistake, 'a')

        @pytest.mark.parametrize('mistake', [0, None, {}, True])
        def test_precondition_dest(self, mistake):
            with pytest.raises(TypeError):
                move_file('a', mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, 'hello'])
        def test_precondition_make_dirs(self, mistake):
            with pytest.raises(ValueError):
                src, dest = _setup_file(n=2)
                move_file(src, dest, make_dirs=mistake)

        @pytest.mark.parametrize('mistake', [0, None, {}, 'hello'])
        def test_precondition_exists(self, mistake):
            src, dest = _setup_file(n=2)
            with pytest.raises(ValueError):
                move_file(src, dest, exists=mistake)


class TestGroup_paths:
    class Test_get_unique_path:
        def test_consecutive_values(self):
            root = Path(_setup_dir())
            for i in range(1, 11):
                file = get_unique_path(root/'{}')
                assert file == f'{root}/{i}'
                Path(file).touch()

        @pytest.mark.parametrize('mistake', [[], 1, True, None])
        def test_invalid_pattern_type(self, mistake):
            with pytest.raises(TypeError):
                get_unique_path(mistake)

        @pytest.mark.parametrize('mistake', ['', '{0}', '{a}', '{:f}'])
        def test_invalid_placeholder(self, mistake):
            with pytest.raises(ValueError):
                get_unique_path(mistake)

        def test_keeps_slash_at_the_end(self):
            assert get_unique_path('/tmp/{}/').endswith('/')

        @pytest.mark.parametrize('mistake', ['hello_{}', '{}', './{}', '/a/{}', '/{}/a', '{:06d}'])
        def test_not_exists(self, mistake):
            path = get_unique_path(mistake)
            assert not Path(path).exists()


def _check_tree(src, dest):
    for src_item in Path(src).iterdir():
        dest_item = str(src_item).replace(str(src), str(dest))
        dest_item = Path(dest_item)

        if src_item.is_dir():
            assert dest_item.is_dir()
            _check_tree(src_item, dest_item)
        else:
            assert dest_item.is_file()


def _setup_tree(path=None):
    path = _setup_path(path)

    for d in [path, f'{path}/a', f'{path}/b', f'{path}/b/c']:
        _setup_dir(d)

    for f in [f'{path}/1.txt', f'{path}/a/2.txt', f'{path}/b/3.txt', f'{path}/b/c/4.txt']:
        _setup_file(f)

    return str(path)


def _setup_tree_2(path=None):
    path = _setup_tree(path)

    make_dir(f'{path}/a/a')
    make_dir(f'{path}/b/a')
    make_dir(f'{path}/b/c/a')
    make_dir(f'{path}/b/c/a/d')

    Path(f'{path}/1.py').touch()
    Path(f'{path}/a/2.py').touch()
    Path(f'{path}/b/a/5.py').touch()
    Path(f'{path}/a/a/6.py').touch()

    return path


def _setup_dir_and_file(path_dir=None, filename=None):
    if filename is None:
        filename = 'file'

    dir_ = _setup_dir(path_dir)
    file = _setup_file(Path(dir_)/filename)
    return dir_, file


def _setup_file(path=None, n=1):
    files = []
    for _ in range(n):
        file = _setup_path(path)
        make_dir(Path(file).parent)
        Path(file).write_text(file)

        files.append(file)

    if n == 1:
        return files[0]
    else:
        return files


def _setup_dir(path=None, n=1):
    dirs = []
    for _ in range(n):
        path = _setup_path(path)
        make_dir(path)
        dirs.append(path)

    if n == 1:
        return dirs[0]
    else:
        return dirs


def _setup_path(path=None):
    if path is None:
        return get_unique_path()
    elif '{}' in str(path):
        return get_unique_path(path)
    else:
        return str(path)
