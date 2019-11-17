import boto.s3.connection
import boto3
from botocore.exceptions import ClientError


bucket_name = "python_test"
bucket = None

def get_file_names_in_bucket():
    bucket = get_bucket_by_name()
    list_file_names_in_bucket = [key.key for key in bucket.list()]
    return list_file_names_in_bucket

def get_bucket_name():
    return bucket_name

access_key = 'access_key'
secret_key = 'secret_key'

def get_bucket_by_name():

    conn = boto.connect_s3(
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key,
            host = 'hb.bizmrg.com',
            calling_format = boto.s3.connection.OrdinaryCallingFormat(),
            )

    for bucket in conn.get_all_buckets():
        if bucket.name == bucket_name:
            return bucket

def upload_file_to_s3(file_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False

    """
    bucket = get_bucket_by_name()

    print(f"filename = {file_name}")
    if object_name is None:
        object_name = file_name

    try:
        s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key,endpoint_url="http://hb.bizmrg.com")
        with open(file_name, "rb") as f:
            print(file_name)
            s3.upload_fileobj(f, bucket.name, file_name.split("/")[-1])
    except ClientError as e:
        return False
    return True

