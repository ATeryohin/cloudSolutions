import boto.s3.connection
import boto.s3.key

bucket_name = "python_test"

def get_file_names_in_bucket(bucket):
    list_file_names_in_bucket = [key.key for key in bucket.list()]
    return list_file_names_in_bucket

def get_bucket_by_name(name):

    access_key = 'xxx'
    secret_key = 'xxxxx'

    conn = boto.connect_s3(
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key,
            host = 'hb.bizmrg.com',
            calling_format = boto.s3.connection.OrdinaryCallingFormat(),
            )

    for bucket in conn.get_all_buckets():
        if bucket.name == name:
            return bucket

bucket = get_bucket_by_name(bucket_name)
get_file_names_in_bucket(bucket)
