from abc import ABC, abstractmethod
import boto3
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

class EC2ClientSingleton:
    _instances = {}

    @classmethod
    def get_client(cls, region):
        if region not in cls._instances:
            cls._instances[region] = boto3.client('ec2', region_name=region)
        return cls._instances[region]

class EC2UsageChecker(ABC):

    @abstractmethod
    def get_usage(self, region, quota_name):
        pass

class RunningOnDemandInstancesChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        return len([i for r in response['Reservations'] for i in r['Instances'] if i['InstanceType'][0] in 'ACDHIMRTZ'])

class ClientVPNEndpointsChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        response = ec2.describe_client_vpn_endpoints()
        return len(response['ClientVpnEndpoints'])

class AMIsChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        response = ec2.describe_images(Owners=['self'])
        return len(response['Images'])

class MulticastDomainAssociationsChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        response = ec2.describe_transit_gateway_multicast_domains()
        associations = [domain for domain in response['TransitGatewayMulticastDomains']
                        if domain['State'] == 'associated']
        return len(associations)

class MulticastNetworkInterfacesChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        response = ec2.describe_transit_gateways()
        max_interfaces = 0
        for tgw in response['TransitGateways']:
            tgw_id = tgw['TransitGatewayId']
            multicast_domains = ec2.describe_transit_gateway_multicast_domains(
                Filters=[{'Name': 'transit-gateway-id', 'Values': [tgw_id]}]
            )
            interfaces = sum(len(domain.get('TransitGatewayAttachmentIds', []))
                             for domain in multicast_domains['TransitGatewayMulticastDomains'])
            max_interfaces = max(max_interfaces, interfaces)
        return max_interfaces

class VerifiedAccessGroupsChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        response = ec2.describe_verified_access_groups()
        return len(response['VerifiedAccessGroups'])

class RunningDedicatedHostsChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        instance_family = quota_name.split("Running Dedicated ")[1].split(" Hosts")[0]
        response = ec2.describe_hosts(
            Filters=[
                {
                    'Name': 'instance-type',
                    'Values': [f'{instance_family}.*']
                },
                {
                    'Name': 'state',
                    'Values': ['available', 'under-assessment', 'permanent-failure']
                }
            ]
        )
        return len(response['Hosts'])

class NewReservedInstancesChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        # This is a little hacky as it isn't 100% accurate, but it is a close approximation
        now = datetime.utcnow()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        response = ec2.describe_reserved_instances(
            Filters=[
                {
                    'Name': 'state',
                    'Values': ['active']
                }
            ]
        )

        new_ri_count = sum(
            1 for ri in response['ReservedInstances']
            if start_of_month <= ri['Start'].replace(tzinfo=None) <= now
        )

        return new_ri_count

class AttachmentsPerTransitGatewayChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        response = ec2.describe_transit_gateways()
        max_attachments = 0
        for tgw in response['TransitGateways']:
            tgw_id = tgw['TransitGatewayId']
            attachments = ec2.describe_transit_gateway_attachments(
                Filters=[{'Name': 'transit-gateway-id', 'Values': [tgw_id]}]
            )
            attachment_count = len(attachments['TransitGatewayAttachments'])
            max_attachments = max(max_attachments, attachment_count)
        return max_attachments

class TransitGatewaysPerAccountChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        response = ec2.describe_transit_gateways()
        return len(response['TransitGateways'])

class VPNConnectionsPerVGWChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        response = ec2.describe_vpn_connections()

        vgw_connections = {}
        for vpn in response['VpnConnections']:
            vgw_id = vpn.get('VpnGatewayId')
            if vgw_id:
                vgw_connections[vgw_id] = vgw_connections.get(vgw_id, 0) + 1

        return max(vgw_connections.values()) if vgw_connections else 0

class VPNConnectionsPerRegionChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        response = ec2.describe_vpn_connections()
        return len(response['VpnConnections'])

class RoutesPerTransitGatewayChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        response = ec2.describe_transit_gateways()
        max_routes = 0

        for tgw in response['TransitGateways']:
            tgw_id = tgw['TransitGatewayId']
            route_tables = ec2.describe_transit_gateway_route_tables(
                Filters=[{'Name': 'transit-gateway-id', 'Values': [tgw_id]}]
            )

            for route_table in route_tables['TransitGatewayRouteTables']:
                route_table_id = route_table['TransitGatewayRouteTableId']
                routes = ec2.search_transit_gateway_routes(
                    TransitGatewayRouteTableId=route_table_id,
                    Filters=[{'Name': 'type', 'Values': ['static', 'propagated']}]
                )
                max_routes = max(max_routes, len(routes['Routes']))

        return max_routes

class AMISharingChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        response = ec2.describe_images(Owners=['self'])

        shared_ami_count = 0
        for image in response['Images']:
            launch_permissions = ec2.describe_image_attribute(
                ImageId=image['ImageId'],
                Attribute='launchPermission'
            )
            if 'LaunchPermissions' in launch_permissions:
                # Count AMIs shared with specific accounts or made public
                if launch_permissions['LaunchPermissions'] or 'all' in [perm.get('Group', '') for perm in launch_permissions['LaunchPermissions']]:
                    shared_ami_count += 1

        return shared_ami_count

class CustomerGatewaysPerRegionChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        response = ec2.describe_customer_gateways()
        return len(response['CustomerGateways'])

class RoutesPerClientVPNEndpointChecker(EC2UsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EC2ClientSingleton.get_client(region)
        response = ec2.describe_client_vpn_endpoints()

        max_routes = 0
        for endpoint in response['ClientVpnEndpoints']:
            endpoint_id = endpoint['ClientVpnEndpointId']
            routes = ec2.describe_client_vpn_routes(ClientVpnEndpointId=endpoint_id)
            route_count = len(routes['Routes'])
            max_routes = max(max_routes, route_count)

        return max_routes
