import celery
from .models.RaspberryPi import RaspberryPi

@celery.shared_task
def record_video(pk: int, file_path: str, stop_time) -> None:
    """

    This task will be scheduled using a PeriodicTask on the times that are dedicated by the schedule

    celery task for recording on the pi
    :param pk: primary_key of the raspberry pi we want to record on
    :param file_path: file_path where the recording should be stored
    :param stop_time: when the recording should stop
    :return: nothing
    """
    rpi = RaspberryPi.objects.get(id=pk)
    rpi.record(file_path=file_path, stop_time=stop_time)