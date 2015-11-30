"""Stream finder.

Usage:
  stream_finder.py <service> <query> [--autoplay] [--player=<cmd>]

Options:
  -h --help         Show this screen.
  --autoplay        Autoplay
  --version         Show version.
  --player=<cmd>    Player launch command [default: mpv].

"""
from docopt import docopt
import subprocess


def launch_player(stream_uri):
    print('Launching player: ' + stream_uri)
    cmd = [arguments.get('--player'),
           stream_uri,
           '--fullscreen']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              stdin=subprocess.PIPE
                              )
    out, err = p.communicate()
    print out
    # TODO: Handle keyboard input and send to subprocess.


def twitch(channel_name):
    from service_twitch import get_live_stream
    m3u8_obj = get_live_stream(channel_name)
    if len(m3u8_obj.playlists) > 0:
        launch_player(m3u8_obj.playlists[0].uri)
    else:
        print 'No stream available.'


def svtplay(url):
    from service_svtplay import get_by_url
    stream_uri = get_by_url(url)
    launch_player(stream_uri)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Dev')
    service = arguments.get('<service>')
    query = arguments.get('<query>')
    # Run function with same name as service.
    locals().get(service)(query)

    # print(arguments)
