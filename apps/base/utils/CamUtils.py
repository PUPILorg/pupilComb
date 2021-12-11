import cv2

from queue import Queue
import threading
import numpy as np

import time

class WebCam(threading.Thread):

    _src: int
    _width: int
    _height: int
    _queue: Queue[np.array]
    _end_time: float

    def __init__(self, src:int, width: int, height: int, queue: Queue[np.array], end_time: float
                 ,group=None, target=None, name=None):
        """
        :param src: source of the camera
        :param width: width of the image
        :param height: height of the image
        :param queue: queue to store the frames into
        :param end_time: when to stop recording
        """
        super(WebCam, self).__init__(group=group, target=target, name=name)

        self._src = src
        self._queue = queue
        self._width = width
        self._height = height
        self._end_time = end_time

        return

    def run(self) -> None:
        """
        writes the frames to the queue for the VideoWriter to write into a file

        once false is written the VideoWriter knows to stop writing

        :return:
        """
        capture = cv2.VideoCapture(self._src)

        while time.time() <= self._end_time:
            ret, frame = capture.read()
            self._queue.put(frame)

        self._queue.put(False) # the exit token so the Writer knows to stop writing
        capture.release()
        return




class VideoWriter(threading.Thread):

    _width: int
    _height: int
    _queue: Queue[np.array] # queue to monitor for new frames to write
    _filepath: str
    _fps: int
    _fourcc: int

    def __init__(self, width: int, height: int, queue: Queue[np.array], fps: int, filepath: str, fourcc: int,group=None, target=None,
                 name=None):
        """
        Writes the video stored in the queue into a file
        :param width: width of the video
        :param height: height of the video
        :param queue: queue the video is stored in
        :param fps: fps of the video to write
        :param fourcc: code for the video writer
        """
        super(VideoWriter, self).__init__(group=group, target=target, name=name)

        self._queue = queue
        self._width = width
        self._height = height
        self._filepath = filepath
        self._fps = fps
        self._fourcc = fourcc
        return

    def run(self) -> None:
        output = cv2.VideoWriter(self._filepath, self._fourcc, self._fps, (self._width, self._height))
        while frame := self._queue.get() is not False:
            output.write(frame)

        output.release()
        return