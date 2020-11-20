import sys
import re
import os
import ffmpeg
import enlighten
from .utils import get_bitdepth
if sys.platform == 'win32':
    import wexpect as expect
    # patch windows consloe for scale correctly characters
    import ansicon
    ansicon.load()
else:
    import pexpect as expect

__version__ = '0.1.10'

pattern_duration = re.compile('duration[ \t\r]?:[ \t\r]?(.+?),[ \t\r]?start',re.IGNORECASE)
pattern_progress = re.compile('time=(.+?)[ \t\r]?bitrate',re.IGNORECASE)
BAR_FMT = u'{desc}{desc_pad}{percentage:3.0f}%|{bar}| {count:{len_total}.1f}/{total:.1f} ' + \
          u'[{elapsed}<{eta}, {rate:.2f}{unit_pad}{unit}/s]'

COUNTER_FMT = u'{desc}{desc_pad}{count:.1f} {unit}{unit_pad}' + \
              u'[{elapsed}, {rate:.2f}{unit_pad}{unit}/s]{fill}'

CONVERT_COMMAND_10Bits = 'ffmpeg -progress pipe:1 -i "{source}" -map 0 -map -v -map V -c:v libx265 -x265-params crf=26:profile=main10 -c:a aac -y "{dest}"'
CONVERT_COMMAND = 'ffmpeg -progress pipe:1 -i "{source}" -map 0 -map -v -map V -c:v libx265 -crf 26 -c:a aac -y "{dest}"'

def convert_file(source: str, dest: str):
    stream = ffmpeg.input(source)
    stream = ffmpeg.output(stream, dest, vcodec='libx265', crf='28')
    ffmpeg.run(stream)

def convert_video_progress_bar(source: str, dest: str, manager=None):
    if manager is None:
        manager = enlighten.get_manager()
    name = source.rsplit(os.path.sep,1)[-1]
    if get_bitdepth(source).is_10bit:
        args = CONVERT_COMMAND_10Bits.format(source=source, dest=dest)
    else:
        args = CONVERT_COMMAND.format(source=source, dest=dest)
    proc = expect.spawn(args, encoding='utf-8')
    pbar = None
    try:
        proc.expect(pattern_duration)
        total = sum(map(lambda x: float(x[1])*60**x[0],enumerate(reversed(proc.match.groups()[0].strip().split(':')))))
        cont = 0
        pbar = manager.counter(total=100, desc=name, unit='%',bar_format=BAR_FMT, counter_format=COUNTER_FMT)
        while True:
            proc.expect(pattern_progress)
            progress = sum(map(lambda x: float(x[1])*60**x[0],enumerate(reversed(proc.match.groups()[0].strip().split(':')))))
            percent = progress/total*100
            pbar.update(percent-cont)
            cont = percent
    except expect.EOF:
        pass
    finally:
        if pbar is not None:
            pbar.close()
    proc.expect(expect.EOF)
    res = proc.before
    res += proc.read()
    exitstatus = proc.wait()
    if exitstatus:
        raise ffmpeg.Error('ffmpeg','',res)
