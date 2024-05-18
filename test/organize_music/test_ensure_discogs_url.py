from src.organize_music.ensure_discogs_url import ensure_discogs_url


def test_ensure_discogs_url_returns_when_url_exists(mocker):
    # Given
    folder_path = "/path/to/Test Artist - Test Album [Test Label]"
    existing_metadata = {"discogs_url": "https://www.discogs.com/existing_url"}
    mock_read_info_file = mocker.patch(
        "src.organize_music.ensure_discogs_url.read_info_file",
        return_value=existing_metadata,
    )

    # When
    res = ensure_discogs_url(folder_path)

    # Then
    assert res is None
    mock_read_info_file.assert_called_once_with(folder_path)


def test_ensure_discogs_url_writes_when_url_does_not_exist(mocker):
    # Given
    folder_path = "/path/to/Test Artist - Test Album [Test Label]"
    existing_metadata = {}
    mock_read_info_file = mocker.patch(
        "src.organize_music.ensure_discogs_url.read_info_file",
        return_value=existing_metadata,
    )

    mock_search = mocker.patch(
        "src.organize_music.ensure_discogs_url.search_for_albums",
        return_value="https://www.discogs.com/new_url",
    )

    new_metadata = {"discogs_url": "https://www.discogs.com/new_url"}
    mock_write_info_file = mocker.patch(
        "src.organize_music.ensure_discogs_url.write_info_file",
        return_value=new_metadata,
    )

    # When
    res = ensure_discogs_url(folder_path)

    # Then
    assert res == new_metadata
    expected_search_args = ("Test Artist", "Test Album", "Test Label")
    mock_search.assert_called_once_with(*expected_search_args)
    mock_read_info_file.assert_called_once_with(folder_path)
    mock_write_info_file.assert_called_once_with(folder_path, new_metadata)
