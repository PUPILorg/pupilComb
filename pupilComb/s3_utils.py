import boto3
from .settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from botocore.errorfactory import ClientError

s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

def does_file_exist(filename: str) -> bool:
    """
    check if the file exists in the pupil-backend-bucket
    :param filename: str of the file location
    :return: bool
    """

    try:
        s3.head_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=filename)
        return True
    except ClientError:
        return False
