"""
For tests install:
 - ffmpeg (https://ffmpeg.org)

and add it to PATH
"""

import pytest
import os
import ffmpeg

from concat_video_g4 import concat_video


def test_1():
    out_file = 'tests/test_concatVideo/out.ts'

    if os.path.exists(out_file):
        os.remove(out_file)

    concat_video(
        'tests/test_concatVideo/in_1.ts',
        'tests/test_concatVideo/in_2.ts',
        out_file
    )

    assert os.path.exists(out_file)

    info = ffmpeg.probe(out_file)

    assert info['streams'][0]['codec_name'] == 'h264'
    assert float(info['streams'][0]['duration']) >= 20.0

    os.remove(out_file)
