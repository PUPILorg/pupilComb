import celery
from .models.Recorder import Recorder
from django.utils import timezone

@celery.shared_task
def record_video(pk: int, file_path: str, stop_time, course_id: int) -> None:
    """

    This task will be scheduled using a PeriodicTask on the times that are dedicated by the schedule

    celery task for recording on the pi
    :param course_id: id for the course
    :param pk: primary_key of the raspberry pi we want to record on
    :param file_path: file_path where the recording should be stored
    :param stop_time: when the recording should stop
    :return: nothing
    """
    rpi = Recorder.objects.get(id=pk)
    file_path += f'--{timezone.now().date()}'
    rpi.record(file_path=file_path, stop_time=stop_time, course_id=course_id)
