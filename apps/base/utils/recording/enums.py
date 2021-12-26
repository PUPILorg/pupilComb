from enum import Enum

class EnumWithChoice(Enum):

    @classmethod
    def choices(cls):
        return tuple((tag.name, tag.value) for tag in cls)

class Codec(EnumWithChoice):

    CODEC_H264 = 'h264'
    CODEC_MJPEG = 'mjpeg'


class Resolution(Enum):

    RES_640x480 = '640x480'
    RES_1280x720 ='1280x720'
    RES_1920x1080 = '1920x1080'


class VideoContainer(EnumWithChoice):

    MP4 = 'mp4'
    MOV = 'mov'
