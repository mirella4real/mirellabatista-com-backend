"""AWS Lambda function that tracks and returns a visitor view count.

Connects to DynamoDB via boto3. The target table is read from the
DYNAMODB_TABLE environment variable, defaulting to 'visitor-counter'.
"""
import json
import os
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("DYNAMODB_TABLE", "visitor-counter"))


def lambda_handler(event, context):
    """AWS Lambda entry point. Increments the visitor counter and returns the updated count.

    Performs an atomic ADD on the 'views' attribute of the 'visitor_count'
    item in DynamoDB, ensuring correctness under concurrent invocations.

    Args:
        event: The Lambda event payload (unused).
        context: The Lambda runtime context (unused).

    Returns:
        dict: A Lambda proxy response with HTTP 200 and a JSON body containing
        the updated view count. Example::

            {"statusCode": 200, "body": '{"views": 42}'}
    """
    response = table.update_item(
        Key={"id": "visitor_count"},
        UpdateExpression="ADD #v :increment",
        ExpressionAttributeNames={"#v": "views"},
        ExpressionAttributeValues={":increment": 1},
        ReturnValues="UPDATED_NEW",
    )
    count = int(response["Attributes"]["views"])
    return {"statusCode": 200, "body": json.dumps({"views": count})}
