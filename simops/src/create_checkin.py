import json
import os
import boto3
from datetime import datetime, timezone

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def handler(event, context):
    event_id = event["pathParameters"]["eventId"]
    body = json.loads(event.get("body") or "{}")
    pilot_id = body["pilotId"]
    timestamp = datetime.now(timezone.utc).isoformat()

    table.put_item(Item={
        "PK": f"EVENT#{event_id}",
        "SK": f"CHECKIN#{timestamp}#{pilot_id}",
        "GSI1PK": f"PILOT#{pilot_id}",
        "GSI1SK": f"EVENT#{event_id}#{timestamp}",
        "pilotName": body.get("pilotName", ""),
        "aircraft": body.get("aircraft", ""),
    })

    return {
        "statusCode": 201, 
        "body": json.dumps({"status": "checked in", "timestamp": timestamp})
    }
