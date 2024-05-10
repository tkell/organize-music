from src.organize_music.add_info_file_and_ids_to_digital import get_id_from_folder


def test_folder_hashes_to_id():
    folder_path = "a_test_folder/another_test_folder"
    actual = get_id_from_folder(folder_path)
    expected = 3186958074
    assert actual == expected
