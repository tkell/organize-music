from src.organize_music.get_release_data import get_discogs_release_data


def test_not_on_discogs(mocker):
    folder_path = "/path/to/folder/Artist - Album"
    mock_read_info_file = mocker.patch(
        "src.organize_music.get_release_data.read_info_file",
        return_value={"discogs_url": "not-on-discogs"},
    )

    result = get_discogs_release_data(folder_path)

    mock_read_info_file.assert_called_once_with(folder_path)
    assert result == {}


def test_stray_master_release(mocker):
    """Test when album_source_url contains "master/"."""
    folder_path = "/path/to/folder/Artist - Album"
    mock_read_info_file = mocker.patch(
        "src.organize_music.get_release_data.read_info_file",
        return_value={"discogs_url": "https://www.discogs.com/master/12345"},
    )

    result = get_discogs_release_data(folder_path)

    mock_read_info_file.assert_called_once_with(folder_path)
    assert result == {}


def test_valid_discogs_url(mocker):
    """Test when a valid Discogs release URL is present."""
    folder_path = "/path/to/folder/Artist - Album"
    discogs_url = "https://www.discogs.com/release/98765"
    mock_read_info_file = mocker.patch(
        "src.organize_music.get_release_data.read_info_file",
        return_value={"discogs_url": discogs_url},
    )
    mock_download_discogs_data = mocker.patch(
        "src.organize_music.get_release_data.lib_discogs.download_release_data",
        return_value={"year": 1998, "title": "Test Album"},
    )

    result = get_discogs_release_data(folder_path)

    mock_read_info_file.assert_called_once_with(folder_path)
    mock_download_discogs_data.assert_called_once_with(discogs_url)
    assert result == {"year": 1998, "title": "Test Album"}
