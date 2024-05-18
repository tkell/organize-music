import json
import pytest
from unittest.mock import mock_open, patch

from src.organize_music.local_file_io import albums_dir_to_folder_paths
from src.organize_music.local_file_io import read_info_file
from src.organize_music.local_file_io import write_info_file


mocked_files = ["folder1", "folder2", ".DS_Store", "folder3"]


@pytest.mark.parametrize("files", [(mocked_files)])
def test_albums_dir_to_folder_paths(mocker, files):
    mocker.patch("os.listdir", return_value=files)
    albums_dir = "/path/to/albums"
    folder_paths = albums_dir_to_folder_paths(albums_dir)

    expected_paths = [
        "/path/to/albums/folder1",
        "/path/to/albums/folder2",
        "/path/to/albums/folder3",
    ]
    actual = folder_paths
    assert actual == expected_paths


def test_write_info_file(mocker):
    folder_path = "/path/to/album"
    metadata = {"title": "New Title", "year": 2023}
    mock_json_dump = mocker.patch("json.dump")
    with patch("builtins.open", mock_open()) as mock_file:
        write_info_file(folder_path, metadata)
        mock_file.assert_called_with("/path/to/album/info.json", "w")
        mock_json_dump.assert_called_once_with(metadata, mock_file())


def test_read_info_file_not_exists(mocker):
    mocker.patch("os.path.exists", return_value=False)
    folder_path = "/path/to/album"
    metadata = read_info_file(folder_path)
    assert metadata == {}


def test_read_info_file_exists(mocker):
    mocker.patch("os.path.exists", return_value=True)
    folder_path = "/path/to/album"
    metadata = {"title": "New Title", "year": 2023}
    file_read_data = json.dumps(metadata)

    with patch("builtins.open", mock_open(read_data=file_read_data)) as mock_file:
        actual_metadata = read_info_file(folder_path)
        mock_file.assert_called_with("/path/to/album/info.json", "r")
        assert actual_metadata == metadata
