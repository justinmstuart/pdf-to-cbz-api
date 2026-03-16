import os
from unittest.mock import MagicMock

from utils.files import delete_directory, save_file_to_directory


def test_save_file_creates_directory(tmp_path):
    target_dir = str(tmp_path / 'nested' / 'subdir')
    mock_file = MagicMock()

    result = save_file_to_directory(mock_file, 'test.pdf', target_dir)

    assert os.path.isdir(target_dir)
    mock_file.save.assert_called_once_with(os.path.join(target_dir, 'test.pdf'))
    assert result == os.path.join(target_dir, 'test.pdf')


def test_save_file_to_existing_directory(tmp_path):
    mock_file = MagicMock()

    result = save_file_to_directory(mock_file, 'doc.pdf', str(tmp_path))

    mock_file.save.assert_called_once()
    assert result == os.path.join(str(tmp_path), 'doc.pdf')


def test_delete_directory_removes_files_and_subdirs(tmp_path):
    subdir = tmp_path / 'nested'
    subdir.mkdir()
    (subdir / 'file1.txt').write_text('hello')
    (tmp_path / 'file2.txt').write_text('world')

    delete_directory(str(tmp_path))

    assert not os.path.exists(str(tmp_path))


def test_delete_nonexistent_directory_does_nothing(tmp_path):
    nonexistent = str(tmp_path / 'does_not_exist')
    delete_directory(nonexistent)  # should not raise


def test_delete_empty_directory(tmp_path):
    target = tmp_path / 'empty_dir'
    target.mkdir()

    delete_directory(str(target))

    assert not os.path.exists(str(target))
