![Example of use](examples/example-use.gif)

# Requirements
A python version between 2.7 and 3.6, and pip (PyPi).
A video player like mpv (https://mpv.io/) or vlc.

# Install

It's optional but recommended to use virtualenv for Python to manage package dependencies.
Install dependencies with ```pip install -r requirements.txt```

### Optional
Bind the python script to an alias in your shell config.

Like this: ```alias sf='python ~/stream-finder/stream_finder.py'```

# Run
```stream_finder.py <service> <query> [--config=<str>]```

# Examples
Twitch channel for summit1g:
```stream_finder.py tw summit1g```

SVT channel 2
```stream_finder.py svt http://www.svtplay.se/kanaler/svt2```

A youtube video
```stream_finder.py yt https://www.youtube.com/watch?v=vwGnXKNGjT0```

# Configuration
There is a configuration file where you may change video player and parameters given to the video player.

# Tests
Tests that connect to 3rd party providers are available. These are useful to detect if a service has changed their api.

### Run tests
```PYTHONPATH=. pytest```

[![Build Status](https://travis-ci.org/kiwiholmberg/stream-finder.svg?branch=master)](https://travis-ci.org/kiwiholmberg/stream-finder)
