import celery
from .models.Recorder import Recorder
from django.utils import timezone

@celery.shared_task
def record_video(pk: int, file_folder: str, duration: float, semester_course_id: int) -> None:
    """

    This task will be scheduled using a PeriodicTask on the times that are dedicated by the schedule

    celery task for recording on the recorder
    :param duration: duration of the video to record
    :param semester_course_id: id for the semester course
    :param pk: primary_key of the recorder to record on
    :param file_folder: folder in which the videos should be stored in | ../semester_course_id/date/
    :return: None
    """
    recorder = Recorder.objects.get(id=pk)
    file_folder += f'{file_folder}{timezone.now().date()}/'
    recorder.record(file_folder=file_folder, duration=duration, course_id=semester_course_id)
