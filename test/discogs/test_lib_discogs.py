from src.discogs.lib_discogs import call_api


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
