import ffmpeg

__version__ = '0.1.0'


def convert_video(source: str, dest: str):
    stream = ffmpeg.input(source)
    stream = ffmpeg.output(stream, dest, vcodec='libx265', crf='28')
    ffmpeg.run(stream)
