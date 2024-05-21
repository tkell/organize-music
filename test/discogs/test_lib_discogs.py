from src.discogs.lib_discogs import (
    call_api,
    download_release_data,
    get_folder_name_and_releases,
    get_release_data,
)


def test_call_api_hits_cache(mocker):
    # Given
    mocker.patch("time.time", return_value=1000)
    mocker.patch("src.discogs.lib_discogs._get_cache_expiry", return_value=600)
    cache_data = {"key": "value"}
    cache_timestamp = 500
    cache_contents = (cache_data, cache_timestamp)
    mock_cache = mocker.patch(
        "src.discogs.lib_discogs._read_cache", return_value=cache_contents
    )

    # When
    result = call_api("http://discogs.com/some-url")

    # Then
    assert result == cache_data
    mock_cache.assert_called_once_with("http://discogs.com/some-url")


def test_call_api_hits_cache_but_expired(mocker):
    # Given
    mocker.patch("time.time", return_value=1000)
    mocker.patch("src.discogs.lib_discogs._get_cache_expiry", return_value=600)
    cache_data = {"key": "value"}
    cache_timestamp = 100
    cache_contents = (cache_data, cache_timestamp)
    mock_cache = mocker.patch(
        "src.discogs.lib_discogs._read_cache", return_value=cache_contents
    )
    new_data = {"new_key": "new_value"}
    mock_call = mocker.patch(
        "src.discogs.lib_discogs._call_discogs_api", return_value=new_data
    )
    mock_write = mocker.patch("src.discogs.lib_discogs._write_cache")

    # When
    result = call_api("http://discogs.com/some-url")

    # Then
    assert result == new_data
    mock_cache.assert_called_once_with("http://discogs.com/some-url")
    mock_call.assert_called_once_with("http://discogs.com/some-url")
    mock_write.assert_called_once_with("http://discogs.com/some-url", 1000, new_data)


def test_call_api_misses_cache(mocker):
    # Given
    mocker.patch("time.time", return_value=1000)
    mock_cache = mocker.patch("src.discogs.lib_discogs._read_cache", return_value=None)
    new_data = {"new_key": "new_value"}
    mock_call = mocker.patch(
        "src.discogs.lib_discogs._call_discogs_api", return_value=new_data
    )
    mock_write = mocker.patch("src.discogs.lib_discogs._write_cache")

    # When
    result = call_api("http://discogs.com/some-url")

    # Then
    assert result == new_data
    mock_cache.assert_called_once_with("http://discogs.com/some-url")
    mock_call.assert_called_once_with("http://discogs.com/some-url")
    mock_write.assert_called_once_with("http://discogs.com/some-url", 1000, new_data)


def test_get_releae_data(mocker):
    # Given
    release = {"basic_information": {"resource_url": "http://discogs.com/some-url"}}
    releases = [release]
    new_data = {"new_key": "new_value"}
    mock_api = mocker.patch("src.discogs.lib_discogs.call_api", return_value=new_data)

    # When
    results = get_release_data(releases)
    assert results == [(release, new_data)]
    mock_api.assert_called_once_with("http://discogs.com/some-url")


def test_download_release_data(mocker):
    # Given
    album_url = "https://www.discogs.com/release/4301112-95-North-Let-Go-Remixes"
    new_data = {"new_key": "new_value"}
    mock_api = mocker.patch("src.discogs.lib_discogs.call_api", return_value=new_data)

    # When
    result = download_release_data(album_url)

    # Then
    assert result == new_data
    api_url = "https://api.discogs.com/releases/4301112"
    mock_api.assert_called_once_with(api_url)


def test_get_folder_name_and_releases(mocker):
    # Given
    discogs_folder = {
        "resource_url": "https://api.discogs.com/folders/1234",
        "name": 'My Discogs Folder""',
    }
    folder_data = {"releases": [{"id": 1}, {"id": 2}]}

    mock_call = mocker.patch(
        "src.discogs.lib_discogs._call_discogs_api", return_value=folder_data
    )

    # When
    name, releases = get_folder_name_and_releases(discogs_folder)

    # Then
    assert name == "My Discogs Folder"
    assert releases == [{"id": 1}, {"id": 2}]
    mock_call.assert_called_once_with(
        "https://api.discogs.com/folders/1234/releases?per_page=100"
    )
