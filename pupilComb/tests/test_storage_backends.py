from unittest import TestCase

import boto3
from django.core.files.storage import default_storage
from pupilComb.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

tearDown = False

class PublicMediaStorageTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
        make sure the test folder in s3 is empty
        :return:
        """
        cls.s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY_ID,
                               aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

        response = cls.s3.list_objects_v2(Bucket=AWS_STORAGE_BUCKET_NAME, Prefix = 'recordings/tests/')
        if not response['KeyCount'] == 0:
            for obj in response['Contents']:
                print('Deleting', obj['Key'])
                cls.s3.delete_object(Bucket = AWS_STORAGE_BUCKET_NAME, Key = obj['Key'])

    def tearDown(self) -> None:
        """
        clear the bucket after each test has been run
        :return:
        """
        if tearDown:
            self.s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

            response = self.s3.list_objects_v2(Bucket=AWS_STORAGE_BUCKET_NAME, Prefix='recordings/tests/')

            if not response['KeyCount'] == 0:
                for obj in response['Contents']:
                    print('Deleting', obj['Key'])
                    self.s3.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=obj['Key'])

    def test_upload_same_raises(self):
        with open('sample_upload_files/out_cam.mp4', 'rb') as f:
            default_storage.save('tests/out_cam.mp4', f)

        with open('sample_upload_files/out_cam.mp4', 'rb') as f:
            with self.assertRaises(AttributeError):
                default_storage.save('tests/out_cam.mp4', f)
