import json
import os
import boto3
from boto3.dynamodb.conditions import Key

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def handler(event, context):
    event_id = event["eventId"]

    response = table.query(
            IndexName="PilotCheckins",
        KeyConditionExpression=Key("GSI1PK").eq(f"EVENT#{event_id}")
    )

    return {
        "statusCode": 200,
        "body": json.dumps(response["Items"])
    }
