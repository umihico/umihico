import boto3 as _boto3
import base64 as _base64


def gen_s3(key, secret_key, region_name):
    """
    gen s3 by keys instead of "boto3.resource('s3')"
    when you didn't do "aws configure" well
    """
    s3 = _boto3.session.Session(
        key=key, secret_key=secret_key, region_name=region_name).resource('s3')
    return s3


def download_text(bucketname, path, s3=None):
    s3 = s3 or _boto3.resource('s3')
    obj = s3.Object(bucketname, path)
    text = _base64.b64decode(obj.get()['Body'].read()).decode()
    return text


def upload_text(bucketname, path, text, public_read=False, ContentType='text/plain;charset=utf-8', s3=None):
    s3 = s3 or _boto3.resource('s3')
    acl = {True: "public-read",
           False: "private"}[public_read]
    response = s3.Bucket(bucketname).put_object(
        ACL=acl, Body=_base64.b64encode(text.encode()), Key=path, ContentType=ContentType)


if __name__ == '__main__':
    text = 'あいう生憎'
    bucketname = 'superfast.umihi.co'
    path = 'encoding.txt'
    upload_text(bucketname, path, text, public_read=True)
    print(download_text(bucketname, path))
