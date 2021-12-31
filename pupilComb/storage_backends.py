from storages.backends.s3boto3 import S3Boto3Storage

class PublicMediaStorage(S3Boto3Storage):
    file_overwrite = False

    def save(self, name, content, max_length=None):

        if self.exists(name):
            raise AttributeError("The file already exists")

        super(PublicMediaStorage, self).save(name, content, max_length)