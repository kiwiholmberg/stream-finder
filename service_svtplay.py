import requests


def get_by_url(url):
    # Get show data from svtplay.se.
    r = requests.get('%s?type=embed&output=json' % (url))

    response_json = r.json()
    video = response_json.get('video')

    # Get the highest quality video stream.
    for vr in video.get('videoReferences'):
        if vr.get('playerType') == 'ios':
            return vr.get('url')
