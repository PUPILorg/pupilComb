import cv2

def get_video_props(filepath: str) -> (int, int, float, float):
    """
    gets properties from a video
    :param filepath: filepath to the video
    :return: (height : int, width: int, fps: float, video_length: float)
    """
    video = cv2.VideoCapture(filepath)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)


    framecount = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    video_length = framecount / fps

    return height, width, fps, video_length