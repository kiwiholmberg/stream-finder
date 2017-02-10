import requests


def get_by_url(url):
    # Get show data from svtplay.se.
    r = requests.get('%s?type=embed&output=json' % (url))
    r.raise_for_status()
    
    response_json = r.json()
    video = response_json.get('video')

    # Get the highest quality video stream.
    for vr in video.get('videoReferences'):
        if vr.get('playerType') == 'ios':
            unscrubbed_url = vr.get('url')
            try:
                # remove all getvars from link
                scrubbed_url = unscrubbed_url[:unscrubbed_url.index('.m3u8') + 5]
                return scrubbed_url
            except IndexError:
                if unscrubbed_url:
                    print 'Stream url used old format without alt getvar. Trying old style...'
                    return unscrubbed_url
                else:
                    print 'Empty url to stream. Exiting.'

