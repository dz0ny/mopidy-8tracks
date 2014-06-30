from __future__ import unicode_literals

import logging
from urlparse import urlparse

import os
from mopidy import backend
from mopidy.models import SearchResult, Track, Album, Artist
from mopidy import config, ext
import requests
import pykka


__version__ = '0.0.1'

logger = logging.getLogger(__name__)

headers = {
    'X-Api-Version': 3,
    'X-Api-Key': '8378938a3d129041be5d325a79ea8cdb535f944f',
}


class EightTracksExtension(ext.Extension):
    dist_name = 'Mopidy 8tracks'
    ext_name = 'eight_tracks'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(EightTracksExtension, self).get_config_schema()
        return schema

    def setup(self, registry):
        registry.add('backend', EightTracksBackend)


class EightTracksBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(EightTracksBackend, self).__init__()
        self.config = config
        self.library = EightTracksLibraryProvider(backend=self)
        self.playback = EightTracksPlaybackProvider(audio=audio, backend=self)

        self.uri_schemes = ['8tracks', '8t']


def resolve_playlist(url):
    res = requests.get(url, params={'format': 'json'}, headers=headers)
    res.raise_for_status()
    data = res.json()
    if data.get('status', False):
        mix = data.get('mix')
        token_res = requests.get('http://8tracks.com/sets/new.json',
                                 headers=headers)
        token_res.raise_for_status()
        token = token_res.json().get('play_token')
        tracks = []
        for x in range(0, mix.get('tracks_count')):
            uri = '8t:/{token}/{type}.json?mix_id={mix}'.format(
                token=token,
                mix=mix.get('id'),
                type='play' if x == 0 else 'next'
            )
            track = Track(
                name=mix.get('name'),
                comment=mix.get('description'),
                length=mix.get('duration') * 1000 / mix.get(
                    'tracks_count'),
                album=Album(
                    name=mix.get('name'),
                    images=[mix.get('cover_urls').get('sq500')]
                ),
                uri=uri
            )
            tracks.append(track)
        return tracks
    return []


class EightTracksLibraryProvider(backend.LibraryProvider):
    def lookup(self, track):
        if '8t:' in track:
            track = track.replace('8t:', '')

        if '8tracks.com' in track:
            return resolve_playlist(track)

    def search(self, query=None, uris=None):
        if not query:
            return

        if 'uri' in query:
            search_query = ''.join(query['uri'])
            url = urlparse(search_query)
            if '8tracks.com' in url.netloc:
                return SearchResult(
                    uri='8t:search',
                    tracks=resolve_playlist(url)
                )


def resolve_track(track):
    uri = track.uri.replace('8t:', '')
    res = requests.get(
        'http://8tracks.com/sets%s' % uri, headers=headers)
    res.raise_for_status()
    data = res.json().get('set')
    return Track(
        name=data.get('track').get('name'),
        comment=track.comment,
        length=data.get('track').get('name'),
        album=Album(
            artists=[Artist(name=data.get('track').get('performer'))],
            name=track.album.name,
            images=track.album.images
        ),
        uri=data.get('track').get('track_file_stream_url')
    )


class EightTracksPlaybackProvider(backend.PlaybackProvider):
    def play(self, _track):
        track = resolve_track(_track)
        return super(EightTracksPlaybackProvider, self).play(track)
