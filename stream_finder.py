"""Stream finder.

Supported services:
    svtplay (alias: svt)
    twitch  (alias: tw)
    youtube (alias: yt) Requires mpv video player with ytdl plugin.

Usage:
  stream_finder.py <service> <query> [--config=<str>]
  stream_finder.py twitch twitchplayspokemon

Options:
  -h --help         Show this screen.
  --config=<str>    Config file to use. [default: config.ini]

"""
import subprocess
import configparser
from docopt import docopt
from aliases import SERVICES


def launch_player(stream_uri):
    """Launch the media player with stream uri."""
    cmd = [
        config.get('player', 'launch_cmd'),
        '"%s"' % stream_uri,
    ] + ['--{}'.format(p) for p in config.get('player', 'parameters').split(',')]
    subprocess.call(' '.join(cmd), shell=True)


def twitch(channel_name):
    """Handle twitch.tv streams"""
    from service.twitch import get_live_stream
    m3u8_obj = get_live_stream(channel_name)
    if len(m3u8_obj.playlists) > 0:
        launch_player(m3u8_obj.playlists[0].uri)
    else:
        print('No stream available.')


def svtplay(url):
    """Handle svtplay.se streams"""
    from service.svtplay import get_by_url
    stream_uri = get_by_url(url)
    launch_player(stream_uri)


def youtube(url):
    """Handle youtube.com streams"""
    launch_player(url)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Dev')
    service = arguments.get('<service>')
    query = arguments.get('<query>')

    config = configparser.ConfigParser()
    config.read(arguments.get('--config'))

    try:
        # Run function with same name as service, or matching alias.
        locals().get(
            SERVICES.get(service, service)
        )(query)
    except NotImplementedError:
        print('Service \'%s\' not implemented' % service)
