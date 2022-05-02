import unittest

import mime_codec


class Tests(unittest.IsolatedAsyncioTestCase):
    async def test_mime_type_fallback(self):
        self.assertEqual('fallback/fallback', mime_codec.get_mime_type('test', fallback='fallback/fallback'))


if __name__ == '__main__':
    unittest.main()
