from videoprops import get_video_properties
from dataclasses import dataclass

@dataclass
class VideoProp:
    codec : str
    width : int
    height : int
    fps : float
    duration: int


def get_props(src: str) -> VideoProp:
    """

    get the video properties

    :param src: string source of the video file
    :return: VideoProp dataclass or runtime error if the file is not found
    """

    props = get_video_properties(src)

    video_props = {
        'codec' : props['codec'],
        'width' : props['width'],
        'height': props['height'],
        'fps': eval(props['avg_frame_rate']),
        'duration': int(eval(props['duration']))
    }

    return VideoProp(**video_props)