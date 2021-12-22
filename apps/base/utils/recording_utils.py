import subprocess
import enum

class Resolution(enum.Enum):

    RES_640x480 = '640x480'
    RES_1280x720 ='1280x720'
    RES_1920x1080 = '1920x1080'

class Encoding(enum.Enum):

    ENCODING_H264 = 'h264'

class Recording:

    _base_command: str = f'ffmpeg -f v4l2 '

    def __init__(self, src: str, output_file: str, duration: int,resolution: Resolution = Resolution.RES_1920x1080,
                 encoding: Encoding = Encoding.ENCODING_H264):
        """
        initializes the ffmpeg command
        :param src: src of the video
        :param output_file: output file location
        :param duration: duration of video to record in seconds
        :param res: resolution of the video (default 1920x1080)
        :param encoding: encoding of the video (default h264)
        """
        self._base_command += f'-video_size {resolution} -c:v {encoding} -i {src} -t {duration} -c:v copy {output_file}'

    def start(self):
        subprocess.run(self._base_command, shell=True)
#tiny change