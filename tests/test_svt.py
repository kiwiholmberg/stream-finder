from service.svtplay import get_by_url


def test_channel1():
    # It should return a stream uri.
    uri = get_by_url('http://www.svtplay.se/kanaler/svt1')
    assert uri.endswith('.m3u8')
