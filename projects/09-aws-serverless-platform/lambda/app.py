import json
import os
import uuid

import boto3


def _table():
    return boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def handler(event, context):
    method = event.get("httpMethod", "GET")
    if method == "POST":
        body = event.get("body") or "{}"
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            return _response(400, {"error": "invalid JSON"})
        message = payload.get("message")
        if not isinstance(message, str) or not message.strip():
            return _response(400, {"error": "message is required"})
        item = {"id": str(uuid.uuid4()), "message": message.strip()}
        _table().put_item(Item=item)
        return _response(201, item)
    if method == "GET":
        return _response(200, {"status": "ok"})
    return _response(405, {"error": "method not allowed"})


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }
