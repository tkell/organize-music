from src.organize_music.add_info_file import add_id_to_folder, _get_id_from_folder


def test_add_id_to_folder_new_id(mocker):
    # Given
    folder_path = "/path/to/my/album"
    existing_metadata = {"discogs_url": "https://www.discogs.com/release/12345678"}
    mock_read_info_file = mocker.patch(
        "src.organize_music.add_info_file.read_info_file",
        return_value=existing_metadata,
    )
    mock_write_info_file = mocker.patch(
        "src.organize_music.add_info_file.write_info_file"
    )

    # When
    add_id_to_folder(folder_path)

    # Then
    expected_id = _get_id_from_folder(folder_path)
    expected_metadata = {
        "discogs_url": "https://www.discogs.com/release/12345678",
        "id": expected_id,
    }
    mock_read_info_file.assert_called_once_with(folder_path)
    mock_write_info_file.assert_called_once_with(folder_path, expected_metadata)
