from __future__ import unicode_literals

import unittest

from mopidy.models import Track, Album

from mopidy_eight_tracks import resolve_playlist, resolve_track
import httpretty
import os


def fixture(name):
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data/%s.json' % name
    )
    with open(path, 'r') as content_file:
        return content_file.read()


def patch(url, fix):
    httpretty.register_uri(
        httpretty.GET,
        url,
        body=fixture(fix),
        content_type='application/json'
    )


class ResolveTest(unittest.TestCase):
    @httpretty.activate
    def test_resolve_playlist(self):
        patch('http://8tracks.com/cmaunder/freshly-chilled?format=json', 'mix')
        patch('http://8tracks.com/sets/new.json', 'token')
        t = resolve_playlist('http://8tracks.com/cmaunder/freshly-chilled')
        self.assertEqual(31, len(t))
        self.assertEqual('Freshly Chilled', t[0].name)


    @httpretty.activate
    def test_resolve_track(self):
        patch('http://8tracks.com/sets/964179667/play.json?mix_id=2543880',
              'track')
        track = Track(
            album=Album(
                artists=[],
                images=[
                    u'http: //8tracks.imgix.net/i/000/764/206/JK_WOS_CU_'
                    u'8TRACK01-9273.jpg?fm=jpg&q=65&w=500&h=500&fit=crop'],
                name=u'Freshly Chilled'
            ),
            artists=[],
            comment=u'newtracksforyourears', composers=[],
            length=224548, name=u'Freshly Chilled', performers=[],
            uri=u'8t:/964179667/play.json?mix_id=2543880'
        )
        t = resolve_track(track)
        self.assertIsInstance(t, Track)


