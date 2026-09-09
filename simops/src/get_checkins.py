import json
import os
import boto3
from boto3.dynamodb.conditions import Key

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def handler(event, context):
    event_id = event["pathParameters"]["eventId"]

    response = table.query(
        KeyConditionExpression=Key("PK").eq(f"EVENT#{event_id}") & Key("SK").begins_with("CHECKIN#")
    )

    return {
        "statusCode": 200,
        "body": json.dumps(response["Items"])
    }
