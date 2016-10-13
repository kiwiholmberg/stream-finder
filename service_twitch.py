import requests
import json
import re
import random
import m3u8
import subprocess


USHER_API = 'http://usher.twitch.tv/api/channel/hls/{channel}.m3u8?player=twitchweb' +\
    '&token={token}&sig={sig}&$allow_audio_only=true&allow_source=true' + \
    '&type=any&p={random}'
TOKEN_API = 'http://api.twitch.tv/api/channels/{channel}/access_token'
TWITCH_URL = 'https://www.twitch.tv'


def get_client_id():
    r = requests.get(TWITCH_URL)
    if r.status_code >= 400:
        raise Exception('Error fetching twitch site.')
    script_matches = re.findall(
        r'<script src="(/assets/global-fe\w*.js)" type="text/javascript"></script>', r.text)
    if len(script_matches) != 1:
        raise Exception('Error finding frontend script on twitch page.')
    # Get the twitch frontend script that contains the Client-ID we need.
    r = requests.get(TWITCH_URL + script_matches[0])
    if r.status_code >= 400:
        raise Exception('Error fetching twitch frontend script.')

    # Find the client ID with a regex that totally wont match anything else /s
    client_ids = re.findall(r'var n={},r="(\w*)";', r.text)
    if len(client_ids) != 1:
        raise Exception(
            'Error finding client ID in twitch frontend script. Got {}'.format(client_ids))
    return client_ids[0]


def get_token_and_signature(channel, client_id):
    url = TOKEN_API.format(channel=channel)
    headers = {'Client-ID': client_id}
    r = requests.get(url, headers=headers)
    if r.status_code >= 400:
        raise Exception('Error requesting token from twitch: {}'.format(r.text))
    data = r.json()
    return data['token'], data['sig']


def get_live_stream(channel):
    client_id = get_client_id()
    token, sig = get_token_and_signature(channel, client_id)
    url = USHER_API.format(channel=channel, sig=sig, token=token, random=random.randint(0, 1E7))
    r = requests.get(url)
    m3u8_obj = m3u8.loads(r.text)
    return m3u8_obj
