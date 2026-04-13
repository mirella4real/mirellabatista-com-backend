# visitor counter lambda function
import json
import os
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("DYNAMODB_TABLE", "visitor-counter"))


def lambda_handler(event, context):
    response = table.update_item(
        Key={"id": "visitor_count"},
        UpdateExpression="ADD #v :increment",
        ExpressionAttributeNames={"#v": "views"},
        ExpressionAttributeValues={":increment": 1},
        ReturnValues="UPDATED_NEW",
    )
    count = int(response["Attributes"]["views"])
    return {"statusCode": 200, "body": json.dumps({"views": count})}
