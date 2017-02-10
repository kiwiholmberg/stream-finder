"""Stream finder.

Supported services:
    svtplay (alias: svt)
    twitch  (alias: tw)
    youtube (alias: yt) Requires mpv with ytdl plugin

Usage:
  stream_finder.py <service> <query> [--autoplay] [--player=<cmd>]

Options:
  -h --help         Show this screen.
  --autoplay        Autoplay
  --version         Show version.
  --player=<cmd>    Player launch command [default: mpv].

"""
import subprocess
from docopt import docopt
from aliases import SERVICES


def launch_player(stream_uri):
    """Execute the media player with the already extracted link."""
    print('Launching player for uri: {}'.format(stream_uri))
    cmd = [arguments.get('--player'),
           '"%s"' % stream_uri,
           '--fullscreen',
           '--ontop']
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

    try:
        # Run function with same name as service, or matching alias.
        locals().get(
            SERVICES.get(service, service)
        )(query)
    except TypeError:
        print('Service \'%s\' not implemented' % service)

    # print(arguments)
