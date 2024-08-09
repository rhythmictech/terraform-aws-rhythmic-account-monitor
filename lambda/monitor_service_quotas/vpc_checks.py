from abc import ABC, abstractmethod
import boto3
from datetime import datetime

class VPCClientSingleton:
    _instances = {}

    @classmethod
    def get_client(cls, region):
        if region not in cls._instances:
            cls._instances[region] = boto3.client('ec2', region_name=region)
        return cls._instances[region]

class VPCUsageChecker(ABC):

    @abstractmethod
    def get_usage(self, region, quota_name):
        pass

class VPCsPerRegionChecker(VPCUsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = VPCClientSingleton.get_client(region)
        vpc_count = 0
        next_token = None

        while True:
            if next_token:
                response = ec2.describe_vpcs(NextToken=next_token)
            else:
                response = ec2.describe_vpcs()

            vpc_count += len(response['Vpcs'])

            next_token = response.get('NextToken')
            if not next_token:
                break

        return vpc_count

class SubnetsPerVPCChecker(VPCUsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = VPCClientSingleton.get_client(region)
        max_subnets = 0
        next_token = None

        while True:
            if next_token:
                response = ec2.describe_vpcs(NextToken=next_token)
            else:
                response = ec2.describe_vpcs()

            for vpc in response['Vpcs']:
                subnet_count = 0
                subnet_token = None
                while True:
                    if subnet_token:
                        subnet_response = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc['VpcId']]}], NextToken=subnet_token)
                    else:
                        subnet_response = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc['VpcId']]}])

                    subnet_count += len(subnet_response['Subnets'])

                    subnet_token = subnet_response.get('NextToken')
                    if not subnet_token:
                        break

                max_subnets = max(max_subnets, subnet_count)

            next_token = response.get('NextToken')
            if not next_token:
                break

        return max_subnets

class NetworkInterfacesPerRegionChecker(VPCUsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = VPCClientSingleton.get_client(region)
        eni_count = 0
        next_token = None

        while True:
            if next_token:
                response = ec2.describe_network_interfaces(NextToken=next_token)
            else:
                response = ec2.describe_network_interfaces()

            eni_count += len(response['NetworkInterfaces'])

            next_token = response.get('NextToken')
            if not next_token:
                break

        return eni_count

class RouteTablesPerVPCChecker(VPCUsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = VPCClientSingleton.get_client(region)
        route_table_counts = {}
        next_token = None

        while True:
            if next_token:
                response = ec2.describe_route_tables(NextToken=next_token)
            else:
                response = ec2.describe_route_tables()

            for route_table in response['RouteTables']:
                vpc_id = route_table['VpcId']
                route_table_counts[vpc_id] = route_table_counts.get(vpc_id, 0) + 1

            next_token = response.get('NextToken')
            if not next_token:
                break

        return max(route_table_counts.values()) if route_table_counts else 0
