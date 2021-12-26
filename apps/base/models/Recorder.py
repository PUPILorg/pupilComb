from django.db import models
from django.utils import timezone

from apps.base.utils.recording.recording_utils import Recording
from .Media import Media
from .SemesterCourseRecordingItem import SemesterCourseRecordingItem
from .Input import Input


class Recorder(models.Model):

    is_active = models.BooleanField(default=True)
    room = models.OneToOneField('base.Room', on_delete=models.CASCADE)

    queue_name = models.CharField(null=False, blank=True, max_length=100, unique=True, editable=False)

    def __str__(self):
        return f'{self.room}'

    def record(self, file_folder :str, end_time: float, semester_course_id: int) -> None:
        """

        records the video on the pi and sets up the Media and SemesterCourseRecordingItem models

        :param file_folder: folder path to where the videos should be stored should end in trailing '/'
        :param end_time: end_time of the video in datetime format
        :param semester_course_id: id of the semester_course the video is associated with
        :return: None
        """
        duration = (end_time - timezone.now()).seconds

        inputs = Input.objects.filter(recorder=self)
        webcam_input = inputs.get(type_device=Input.TYPE_webcam)
        video_capture_input = inputs.get(type_device=Input.TYPE_video_capture)

        webcam_file = f'{file_folder}webcam.{webcam_input.file_container}'
        video_capture_file = f'{file_folder}video_capture.{video_capture_input.file_container}'

        recording = Recording(webcam_src=webcam_input.path_to_input, video_capture_src=video_capture_input.path_to_input,
                              webcam_output_file=webcam_file, video_capture_output_file=video_capture_file,
                              duration=duration, webcam_codec=webcam_input.codec,
                              video_capture_codec=video_capture_input.codec)
        recording.record()

        scri = SemesterCourseRecordingItem.objects.create(semester_course_id=semester_course_id)

        Media.objects.bulk_create([
            Media(semester_course_recording_item=scri, file=webcam_file),
            Media(semester_course_recording_item=scri, file=video_capture_file)
        ])


    def set_active(self) -> None:
        """
        sets the Recorder status to active
        :return: None
        """
        self.is_active = True
        self.save()