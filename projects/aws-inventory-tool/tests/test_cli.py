import boto3
from botocore.stub import Stubber

from aws_inventory_tool.cli import extract_name_tag, list_instances


def test_extract_name_tag_returns_name_value():
    tags = [{"Key": "Environment", "Value": "dev"}, {"Key": "Name", "Value": "web-1"}]
    assert extract_name_tag(tags) == "web-1"


def test_extract_name_tag_returns_default_when_missing():
    assert extract_name_tag(None) == "-"
    assert extract_name_tag([{"Key": "Env", "Value": "dev"}]) == "-"


def test_list_instances_maps_expected_fields():
    ec2 = boto3.client(
        "ec2",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    stubber = Stubber(ec2)

    stubber.add_response(
        "describe_instances",
        {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceId": "i-0123456789abcdef0",
                            "InstanceType": "t3.micro",
                            "State": {"Name": "running"},
                            "Tags": [{"Key": "Name", "Value": "api-node"}],
                        }
                    ]
                }
            ]
        },
    )

    stubber.activate()
    instances = list_instances(ec2)
    stubber.deactivate()

    assert instances == [
        {
            "instance_id": "i-0123456789abcdef0",
            "state": "running",
            "instance_type": "t3.micro",
            "name": "api-node",
        }
    ]


def test_list_instances_empty_response():
    ec2 = boto3.client(
        "ec2",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    stubber = Stubber(ec2)
    stubber.add_response("describe_instances", {"Reservations": []})

    stubber.activate()
    instances = list_instances(ec2)
    stubber.deactivate()

    assert instances == []
