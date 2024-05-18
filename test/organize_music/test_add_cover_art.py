from src.organize_music.add_cover_art import ensure_cover_art


def test_ensure_cover_art_already_exists(mocker):
    # Given
    folder_path = "/path/to/folder/Artist - Album"
    mock_listdir = mocker.patch("os.listdir", return_value=["cover.jpg"])
    mock_download = mocker.patch("src.organize_music.add_cover_art.download_file")

    # When
    discogs_release_data = {"images": [{"uri": "https://discogs.com/some-image-uri"}]}
    ensure_cover_art(folder_path, discogs_release_data)

    # Then
    mock_listdir.assert_called_once_with(folder_path)
    mock_download.assert_not_called()


def test_ensure_cover_art_not_on_discogs(mocker):
    # Given
    folder_path = "/path/to/folder/Artist - Album"
    mock_listdir = mocker.patch("os.listdir", return_value=[])
    mock_download = mocker.patch("src.organize_music.add_cover_art.download_file")
    discogs_release_data = {}

    # When
    ensure_cover_art(folder_path, discogs_release_data)

    # When
    mock_listdir.assert_called_once_with(folder_path)
    mock_download.assert_not_called()


def test_ensure_cover_art_bad_data_from_discogs(mocker):
    # Given
    folder_path = "/path/to/folder/Artist - Album"
    mock_listdir = mocker.patch("os.listdir", return_value=[])
    mock_download = mocker.patch("src.organize_music.add_cover_art.download_file")
    discogs_release_data = {"images": []}

    # When
    ensure_cover_art(folder_path, discogs_release_data)

    # When
    mock_listdir.assert_called_once_with(folder_path)
    mock_download.assert_not_called()


def test_ensure_cover_art_downloads_cover(mocker):
    # Given
    folder_path = "/path/to/folder/Artist - Album"
    mock_listdir = mocker.patch("os.listdir", return_value=[])
    mock_download = mocker.patch(
        "src.organize_music.add_cover_art.download_file",
        return_value="/path/to/folder/cover.jpg",
    )
    discogs_release_data = {"images": [{"uri": "https://discogs.com/some-image-uri"}]}

    # When
    ensure_cover_art(folder_path, discogs_release_data)

    # Then
    mock_listdir.assert_called_once_with(folder_path)
    mock_download.assert_called_once_with(
        "https://discogs.com/some-image-uri", folder_path, "cover.jpg"
    )
