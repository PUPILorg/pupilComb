import subprocess
from .enums import Resolution, Codec

class Recording:

    _base_command: str = f'ffmpeg '

    def __init__(self, webcam_src: str, video_capture_src: str, webcam_output_file: str, video_capture_output_file: str,
                 duration: int, resolution: str = Resolution.RES_1920x1080.value,
                 webcam_codec: str = Codec.CODEC_H264.value,
                 video_capture_codec: str = Codec.CODEC_MJPEG.value) -> None:
        """

        sets up the class for the recording

        both the codecs for the webcam and video_capture should be direct streams from the hardware. that time the stream
        only has to be copied instead of actually having to be encoded on the actual device

        :param webcam_src: source of the webcam
        :param video_capture_src: source of the video_capture (the hdmi input)
        :param webcam_output_file: webcam output file
        :param video_capture_output_file: video capture output file
        :param duration: duration of the video in seconds
        :param resolution: resolution of the video
        :param webcam_codec: codec for the webcam
        :param video_capture_codec: codec for the video capture
        """

        cam_input = f'-f v4l2 -video_size {resolution} -vcodec {webcam_codec} -i {webcam_src}'
        video_capture_input = f'-f v4l2 -video_size {resolution} -vcodec {video_capture_codec} -i {video_capture_src}'
        self._base_command += f'{cam_input} {video_capture_input} -map 0 -t {duration} -vcodec copy {webcam_output_file} ' \
                              f'-map 1 -t {duration} -vcodec copy {video_capture_output_file}'

    def record(self) -> None:
        """
        starts the recording. As of now this is a blocking command
        :return: None
        """
        subprocess.run(self._base_command, shell=True)