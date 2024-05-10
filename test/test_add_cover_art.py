from src.organize_music.add_cover_art import ensure_cover_art
from src.organize_music.add_cover_art import _find_and_download_discog_cover


def test_find_and_download_discog_cover_success(mocker):
    # Given
    album_source_url = "https://www.discogs.com/release/123456-Artist-Album"
    folder = "/path/to/folder"
    release_data = {"images": [{"uri": "https://img.discogs.com/cover.jpg"}]}

    mock_call_discogs = mocker.patch(
        "src.organize_music.add_cover_art.lib_discogs.call_discogs",
        return_value=release_data,
    )
    mock_download_file = mocker.patch(
        "src.organize_music.add_cover_art.download_file",
        return_value="/path/to/folder/cover.jpg",
    )

    # When
    result = _find_and_download_discog_cover(album_source_url, folder)

    # Then
    mock_call_discogs.assert_called_once_with("https://api.discogs.com/releases/123456")
    mock_download_file.assert_called_once_with(
        "https://img.discogs.com/cover.jpg", folder, "cover.jpg"
    )
    assert result == "/path/to/folder/cover.jpg"


def test_find_and_download_discog_cover_master_release(mocker):
    # Given
    album_source_url = "https://www.discogs.com/release/master/123456-Artist-Album"
    folder = "/path/to/folder"

    mock_call_discogs = mocker.patch(
        "src.organize_music.add_cover_art.lib_discogs.call_discogs"
    )
    mock_download_file = mocker.patch("src.organize_music.add_cover_art.download_file")

    # When
    result = _find_and_download_discog_cover(album_source_url, folder)

    # Then
    mock_call_discogs.assert_not_called()
    mock_download_file.assert_not_called()
    assert result is None


def test_find_and_download_discog_cover_no_images(mocker):
    # Given
    album_source_url = "https://www.discogs.com/release/123456-Artist-Album"
    folder = "/path/to/folder"
    release_data = {}

    mock_call_discogs = mocker.patch(
        "src.organize_music.add_cover_art.lib_discogs.call_discogs",
        return_value=release_data,
    )
    mock_download_file = mocker.patch("src.organize_music.add_cover_art.download_file")

    # When
    result = _find_and_download_discog_cover(album_source_url, folder)

    # Then
    mock_call_discogs.assert_called_once_with("https://api.discogs.com/releases/123456")
    mock_download_file.assert_not_called()
    assert result is None


def test_ensure_cover_art_already_exists(mocker):
    # Given
    folder_path = "/path/to/folder/Artist - Album"
    mock_listdir = mocker.patch("os.listdir", return_value=["cover.jpg"])

    mock_read_info_file = mocker.patch(
        "src.organize_music.add_cover_art.read_info_file"
    )
    mock_find_and_download_discog_cover = mocker.patch(
        "src.organize_music.add_cover_art._find_and_download_discog_cover"
    )

    # When
    ensure_cover_art(folder_path)

    # Then
    mock_listdir.assert_called_once_with(folder_path)
    mock_read_info_file.assert_not_called()
    mock_find_and_download_discog_cover.assert_not_called()


def test_ensure_cover_art_not_on_discogs(mocker):
    # Given
    folder_path = "/path/to/folder/Artist - Album"
    mock_listdir = mocker.patch("os.listdir", return_value=[])
    mock_read_info_file = mocker.patch(
        "src.organize_music.add_cover_art.read_info_file",
        return_value={},
    )
    mock_find_and_download_discog_cover = mocker.patch(
        "src.organize_music.add_cover_art._find_and_download_discog_cover"
    )

    # When
    ensure_cover_art(folder_path)

    # When
    mock_listdir.assert_called_once_with(folder_path)
    mock_read_info_file.assert_called_once_with(folder_path)
    mock_find_and_download_discog_cover.assert_not_called()


def test_ensure_cover_art_downloads_cover(mocker):
    # Given
    folder_path = "/path/to/folder/Artist - Album"
    mock_listdir = mocker.patch("os.listdir", return_value=[])
    mock_read_info_file = mocker.patch(
        "src.organize_music.add_cover_art.read_info_file",
        return_value={"discogs_url": "https://www.discogs.com/release/12345"},
    )
    mock_find_and_download_discog_cover = mocker.patch(
        "src.organize_music.add_cover_art._find_and_download_discog_cover",
        return_value="/path/to/folder/cover.jpg",
    )

    # When
    ensure_cover_art(folder_path)

    # Then
    mock_listdir.assert_called_once_with(folder_path)
    mock_read_info_file.assert_called_once_with(folder_path)
    mock_find_and_download_discog_cover.assert_called_once_with(
        "https://www.discogs.com/release/12345", folder_path
    )
