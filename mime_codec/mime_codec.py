import mimetypes
import ffmpeg

from .profiles_avc import get_avc_profile
from .exceptions import CodecException
from .profiles_mp4a import get_mp4a_profile
from .webm_mime_types import WEBM_MIME_TYPES


def get_mime_type(file_path: str, fallback: str = 'video/mp4'):
    mime_type = mimetypes.guess_type(file_path)[0]
    if mime_type is None:
        mime_type = fallback
    return mime_type


def get_codec(probe_stream, mime_type: str):
    if mime_type in WEBM_MIME_TYPES:
        return probe_stream['codec_name']

    if probe_stream['codec_tag_string'] == 'avc1':
        level = probe_stream['level']
        level = f'{int(level):02x}'
        number, constraint = get_avc_profile(probe_stream['profile'])
        return 'avc1.{}{}{}'.format(number, constraint, level).lower()

    if probe_stream['codec_tag_string'] == 'mp4a':
        return 'mp4a.40.{}'.format(get_mp4a_profile(probe_stream['profile']))

    raise CodecException('Codec not found', probe_stream)


def get_codecs(file_path: str, mime_type: str = None):
    if mime_type is None:
        mime_type = get_mime_type(file_path)
    probe = ffmpeg.probe(file_path)
    return list(map(lambda x: get_codec(x, mime_type), probe['streams']))


def get_mime_codec(file_path: str):
    mime_type = get_mime_type(file_path)
    codecs = get_codecs(file_path)

    return '{0}; codecs="{1}"'.format(mime_type, ','.join(codecs))
