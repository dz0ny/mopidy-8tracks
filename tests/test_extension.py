from __future__ import unicode_literals

import unittest
from mopidy_eight_tracks import EightTracksExtension

class ExtensionTest(unittest.TestCase):

    def test_get_default_config(self):
        ext = EightTracksExtension()

        config = ext.get_default_config()

        self.assertIn('[eight_tracks]', config)
        self.assertIn('enabled = true', config)

    def test_get_config_schema(self):
        ext = EightTracksExtension()
        schema = ext.get_config_schema()
