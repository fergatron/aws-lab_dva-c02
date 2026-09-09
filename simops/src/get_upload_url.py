import json
import os
import boto3
from botocore.client import Config

s3 = boto3.client("s3", config=Config(signature_version="s3v4"))
BUCKET = os.environ["BUCKET_NAME"]

def handler(event, context):
    event_id = event["pathParameters"]["eventId"]
    body = json.loads(event.get("body") or "{}")
    pilot_id = body["pilotId"]
    filename = body["filename"]

    key = f"uploads/{event_id}/{pilot_id}-{filename}"

    url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": BUCKET, "Key": key},
        ExpiresIn=300
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"uploadUrl": url, "key": key})
    }
