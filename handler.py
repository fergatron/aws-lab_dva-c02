import json
import os

def handler(event, context):
    print(f"Remaining time (ms): {context.get_remaining_time_in_millis()}")
    print(f"Request ID: {context.aws_request_id}")
    raise Exception("Deliberate exception for testing error handling")
    return {
            "statusCode": 200,
            "body": json.dumps({"message": "hello", "env": os.environ.get("STAGE", "unset")})
            }
