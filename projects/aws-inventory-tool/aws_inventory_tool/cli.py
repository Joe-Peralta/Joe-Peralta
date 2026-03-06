import argparse
import logging
import os
from typing import Any

import boto3

LOGGER = logging.getLogger("aws_inventory_tool")


def configure_logging() -> None:
    """Set basic structured logging for CLI output."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s event=%(message)s",
    )


def get_aws_config() -> tuple[str | None, str]:
    """Load AWS profile and region from environment variables."""
    profile = os.getenv("AWS_PROFILE")
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    return profile, region


def build_session(profile: str | None, region: str):
    """Create a boto3 session from resolved configuration."""
    if profile:
        return boto3.Session(profile_name=profile, region_name=region)
    return boto3.Session(region_name=region)


def extract_name_tag(tags: list[dict[str, str]] | None) -> str:
    """Return Name tag value if present, else fallback placeholder."""
    if not tags:
        return "-"

    for tag in tags:
        if tag.get("Key") == "Name":
            return tag.get("Value", "-")
    return "-"


def list_instances(ec2_client: Any) -> list[dict[str, str]]:
    """Collect key EC2 fields for all reservations in the account/region."""
    response = ec2_client.describe_instances()
    instances: list[dict[str, str]] = []

    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            instances.append(
                {
                    "instance_id": instance.get("InstanceId", "-"),
                    "state": instance.get("State", {}).get("Name", "unknown"),
                    "instance_type": instance.get("InstanceType", "-"),
                    "name": extract_name_tag(instance.get("Tags")),
                }
            )
    return instances


def print_instances(instances: list[dict[str, str]]) -> None:
    """Print a compact table-like output for EC2 inventory."""
    if not instances:
        print("No EC2 instances found.")
        return

    print("INSTANCE_ID\tSTATE\tTYPE\tNAME")
    for item in instances:
        print(
            f"{item['instance_id']}\t{item['state']}\t{item['instance_type']}\t{item['name']}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List AWS EC2 instances")
    parser.add_argument(
        "--region",
        help="AWS region override (default from AWS_REGION/AWS_DEFAULT_REGION)",
    )
    parser.add_argument(
        "--profile",
        help="AWS profile override (default from AWS_PROFILE)",
    )
    return parser.parse_args()


def main() -> int:
    configure_logging()
    args = parse_args()

    env_profile, env_region = get_aws_config()
    profile = args.profile or env_profile
    region = args.region or env_region

    LOGGER.info("config_resolved profile=%s region=%s", profile or "default", region)

    session = build_session(profile, region)
    ec2_client = session.client("ec2")

    LOGGER.info("fetching_instances")
    instances = list_instances(ec2_client)
    print_instances(instances)
    LOGGER.info("instances_listed count=%d", len(instances))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
