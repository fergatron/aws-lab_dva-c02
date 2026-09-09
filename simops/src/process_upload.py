import json
import urllib.parse
import boto3

s3 = boto3.client("s3")

def handler(event, context):
  for record in event["Records"]:
    bucket = record["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])
    size = record["s3"]["object"]["size"]

    print(f"Processing upload: bucket={bucket} key={key} size={size}")

    head = s3.head_object(Bucket=bucket, Key=key)
    print(f"Content-Type: {head.get('ContentType')}, ETag: {head.get('ETag')}")

  return { "statusCode": 200 }
