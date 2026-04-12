import json
import os

import boto3
import pytest
from moto import mock_aws


@pytest.fixture
def aws_credentials():
    """Mock AWS credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture
def dynamodb_table(aws_credentials):
    """Create a mock DynamoDB table."""
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName="visitor-counter",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        table.put_item(Item={"id": "visitor_count", "views": 0})
        yield table


def test_lambda_returns_200(dynamodb_table):
    """Test that the Lambda function returns HTTP 200."""
    with mock_aws():
        os.environ["DYNAMODB_TABLE"] = "visitor-counter"
        from lambda_function import lambda_handler

        response = lambda_handler({}, {})
        assert response["statusCode"] == 200


def test_lambda_returns_views_count(dynamodb_table):
    """Test that the response body contains a views count."""
    with mock_aws():
        os.environ["DYNAMODB_TABLE"] = "visitor-counter"
        from lambda_function import lambda_handler

        response = lambda_handler({}, {})
        body = json.loads(response["body"])
        assert "views" in body
        assert isinstance(body["views"], int)
        assert body["views"] > 0
