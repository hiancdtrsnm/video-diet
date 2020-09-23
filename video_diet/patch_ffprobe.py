import os
import re
import pipes
import platform
import subprocess
from ffprobe.ffprobe import FFStream

class FFProbe:
    """
    FFProbe wraps the ffprobe command and pulls the data into an object form::
        metadata=FFProbe('multimedia-file.mov')
    """

    def __init__(self, path_to_video):
        self.path_to_video = path_to_video

        try:
            with open(os.devnull, 'w') as tempf:
                subprocess.check_call(["ffprobe", "-h"], stdout=tempf, stderr=tempf)
        except FileNotFoundError:
            raise IOError('ffprobe not found.')

        if os.path.isfile(self.path_to_video):
            if platform.system() == 'Windows':
                cmd = ["ffprobe", "-show_streams", self.path_to_video]
            else:
                cmd = ["ffprobe -show_streams " + pipes.quote(self.path_to_video)]

            out = subprocess.getoutput(cmd)
            out = out.split('\n')

            stream = False
            self.streams = []
            self.video = []
            self.audio = []
            self.subtitle = []
            self.attachment = []

            self.metadata = {}
            is_metadata = False
            stream_metadata_met = False
            chapter_metadata_met = False

            for line in out:

                if 'Metadata:' in line and not (stream_metadata_met or chapter_metadata_met):
                    is_metadata = True
                elif 'Stream #' in line:
                    is_metadata = False
                    stream_metadata_met = True
                elif 'Chapter #' in line:
                    is_metadata = False
                    chapter_metadata_met = True
                elif is_metadata:
                    splits = line.split(',')
                    for s in splits:
                        m = re.search(r'(\w+)\s*:\s*(.*)$', s)
                        self.metadata[m.groups()[0]] = m.groups()[1].strip()

                if '[STREAM]' in line:
                    stream = True
                    data_lines = []
                elif '[/STREAM]' in line and stream:
                    stream = False
                    self.streams.append(FFStream(data_lines))
                elif stream:
                    data_lines.append(line)

            for stream in self.streams:
                if stream.is_audio():
                    self.audio.append(stream)
                elif stream.is_video():
                    self.video.append(stream)
                elif stream.is_subtitle():
                    self.subtitle.append(stream)
                elif stream.is_attachment():
                    self.attachment.append(stream)
        else:
            raise IOError('No such media file ' + self.path_to_video)

    def __repr__(self):
        return "<FFprobe: {metadata}, {video}, {audio}, {subtitle}, {attachment}>".format(**vars(self))
