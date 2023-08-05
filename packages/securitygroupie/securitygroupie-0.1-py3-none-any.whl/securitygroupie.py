import boto3
import botocore
import logging
import datetime

from models import SecurityGroup

logging.basicConfig(filename="FindMyEndpoints.log",
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.WARN)


def get_current_account() -> str:
    sts_client = boto3.client("sts")
    response = sts_client.get_caller_identity()
    return response.get("Account")


def get_regions() -> list:
    """
    Returns of AWS regions
    Inputs:
        None
    Returns:
        [
            {
                'Endpoint': 'string',
                'RegionName': 'string',
                'OptInStatus': 'string'
            },
        ]
    """

    ec2 = boto3.client("ec2")
    regions_raw = ec2.describe_regions(
        AllRegions=False
    )["Regions"]
    for i in regions_raw:
        yield i.get("RegionName")


def iter_network_interfaces(ec2_client: botocore.client) -> list:
    """
    Returns elastic network interfaces in a region
    Inputs:
        session = boto3 client object
    Returns:
    [
        {
            'Association': {
                'AllocationId': 'string',
                'AssociationId': 'string',
                'IpOwnerId': 'string',
                'PublicDnsName': 'string',
                'PublicIp': 'string',
                'CustomerOwnedIp': 'string',
                'CarrierIp': 'string'
            },
            'NetworkInterfaceId': 'string',
            ...,
},
    ]
    """

    next_token = "X"
    network_interfaces = []
    while next_token is not None:
        if next_token == "X":
            response = ec2_client.describe_network_interfaces()
        else:
            response = ec2_client.describe_network_interace(
                NextToken=next_token
            )
        next_token = response.get("NextToken")
        for i in response.get("NetworkInterfaces"):
            network_interfaces.append(i)
    for network_interface in network_interfaces:
        yield network_interface


def iter_security_groups(ec2_client: botocore.client) -> list:
    """
    Returns security groups in a region

    Inputs:
        session = boto3 client object
    Returns:
{
    'SecurityGroups': [
        {
            'Description': 'string',
            'GroupName': 'string',
            'IpPermissions': ...
            'OwnerId': 'string',
            'GroupId': 'string',
            ...
    """
    security_groups = []
    response = ""
    next_token = "X"
    while next_token is not None:
        if next_token == "X":
            response = ec2_client.describe_security_groups()
        else:
            response = ec2_client.describe_security_groups(
                NextToken=next_token
            )
        next_token = response.get("NextToken")
        for security_group in response.get("SecurityGroups"):
            security_groups.append(security_group)
    for security_group in security_groups:
        yield security_group


def output_csv(account_id, security_groups):
    print("Account Id, Region, Security Group Id, Security Group Name, Attached Resources")
    for sg_key in security_groups.keys():
        attached_resources = None
        if security_groups.get(sg_key).get_attached_resources():
            attached_resources = ' '.join((security_groups.get(sg_key).get_attached_resources()))
        print(f"{account_id},{security_groups.get(sg_key).get_region_name()},{security_groups.get(sg_key).get_security_group_id()},{security_groups.get(sg_key).get_security_group_name()}, {attached_resources}")


def main():
    security_groups = {}
    account_id = get_current_account()
    for region in get_regions():
        ec2_client = boto3.client("ec2", region_name=region)
        for security_group in iter_security_groups(ec2_client):
            sg = SecurityGroup.SecurityGroup(security_group_id=security_group.get("GroupId"))
            sg.set_security_group_name(security_group.get("GroupName"))
            sg.set_region_name(region)
            security_groups[security_group.get("GroupId")] = sg
        for network_interface in iter_network_interfaces(ec2_client):
            for network_interface_sg in network_interface.get("Groups"):
                for sg_key in security_groups.keys():
                    if sg_key == network_interface_sg.get("GroupId"):
                        security_groups.get(sg_key).add_attached_resource(resource_id = network_interface.get("NetworkInterfaceId"))
    output_csv(account_id, security_groups)
    return


if __name__ == "__main__":
    main()
