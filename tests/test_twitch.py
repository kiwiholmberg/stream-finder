from service.twitch import get_live_stream

TEST_CHANNELS = [
  'twitchplayspokemon', 
  'esl_overwatch', 
  'esl_csgo',
  'summit1g'
]

def test_channels():
	# Test that at least one of the channels loads.
	ok_channels = 0
	for channel in TEST_CHANNELS:
		m3u8_obj = get_live_stream(channel)
		try:
			if m3u8_obj.playlists[0].uri.endswith('.m3u8'):
				ok_channels += 1
				break
		except Exception:
			print('Channel %s failed' % channel)
	assert ok_channels >= 1

