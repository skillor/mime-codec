import unittest
import os

from mime_codec import *


class Tests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.current_dir = os.path.dirname(os.path.realpath(__file__))

    async def test_mime_type_fallback(self):
        self.assertEqual('fallback/fallback',
                         get_mime_type('test', fallback='fallback/fallback'))

    async def test_video_mp4(self):
        self.assertEqual('video/mp4; codecs="avc1.42401e,mp4a.40.2"',
                         get_mime_codec(os.path.join(self.current_dir, 'test_files', 'small.mp4')))

    async def test_video_webm(self):
        self.assertEqual('video/webm; codecs="vp8,vorbis"',
                         get_mime_codec(os.path.join(self.current_dir, 'test_files', 'small.webm')))


if __name__ == '__main__':
    unittest.main()
