import ffmpeg


def concat_video(in_path_1: str, in_path_2: str, out_path: str) -> None:
    """
    Concat 2 video files with same codecs (it use ffmpeg)
    :param in_path_1: Path to 1 input video file
    :type in_path_1: str
    :param in_path_2: Path to 2 input video file
    :type in_path_2: str
    :param out_path: Path to output video file
    :type out_path: str
    :return: None
    """

    ffmpeg.input(f'concat:{in_path_1}|{in_path_2}')\
        .output(out_path, vcodec='copy', acodec='copy')\
        .overwrite_output()\
        .run(quiet=True)
