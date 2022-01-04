import os

from django.core.files.storage import default_storage

import threading

class UploadToS3Threaded(threading.Thread):

    def __init__(self, local_file: str, upload_path: str, media_id: int):
        """
        initializes the thread for uploading a file to S3 and sets the uploaded to True
        :param local_file: local path to the video file
        :param upload_path: path to where the file will be stored on S3
        :param media_id: id of the Media object
        """
        super(UploadToS3Threaded, self).__init__()
        self.local_file = local_file
        self.upload_path = upload_path
        self.media_id = media_id

    def run(self) -> None:
        from apps.base.models.Media import Media


        with open(self.local_file, 'rb') as video_file:
            default_storage.save(self.upload_path, video_file)

        media = Media.objects.get(id = self.media_id)
        media.set_uploaded()

        os.remove(self.local_file)