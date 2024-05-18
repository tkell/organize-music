from src.discogs.discogs_search import build_search_urls


def test_search_urls_are_generated_correctly():
    args = {"artist": "The Beatles", "release_title": "Yellow Submarine"}

    actual_urls = build_search_urls(**args)

    expected_urls = [
        "https://api.discogs.com/database/search?artist=The+Beatles&release_title=Yellow+Submarine",
        "https://api.discogs.com/database/search?artist=The+Beatles",
        "https://api.discogs.com/database/search?release_title=Yellow+Submarine",
    ]

    assert actual_urls == expected_urls
