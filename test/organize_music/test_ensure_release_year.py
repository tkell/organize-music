from src.organize_music.ensure_release_year import ensure_release_year


def test_no_discogs_data(mocker):
    folder_path = "/path/to/folder/Artist - Album"
    mock_read = mocker.patch(
        "src.organize_music.ensure_release_year.read_info_file", return_value={}
    )
    mock_write = mocker.patch("src.organize_music.ensure_release_year.write_info_file")
    mocker.patch("builtins.input", return_value="1995")

    discogs_release_data = {}
    ensure_release_year(folder_path, discogs_release_data)

    mock_read.assert_called_once_with(folder_path)
    mock_write.assert_called_once_with(folder_path, {"release_year": 1995})


def test_discogs_data_and_does_not_overwrite(mocker):
    folder_path = "/path/to/folder/Artist - Album"
    mock_read = mocker.patch(
        "src.organize_music.ensure_release_year.read_info_file",
        return_value={"id:": 1234},
    )
    mock_write = mocker.patch("src.organize_music.ensure_release_year.write_info_file")
    discogs_release_data = {"year": 1995}
    ensure_release_year(folder_path, discogs_release_data)

    mock_read.assert_called_once_with(folder_path)
    mock_write.assert_called_once_with(folder_path, {"release_year": 1995, "id:": 1234})
