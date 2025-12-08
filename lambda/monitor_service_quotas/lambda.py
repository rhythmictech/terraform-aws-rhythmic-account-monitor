import os
import boto3
import json
import time
from datetime import datetime, timedelta
from botocore.config import Config
import checker
import cloudformation_checks
import ebs_checks
import ec2_checks
import efs_checks
import eks_checks
import es_checks
import rds_checks
import route53_checks
import workspaces_checks
import vpc_checks
import logging

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOG_LEVEL', logging.INFO))
ch = logging.StreamHandler()
ch.setLevel(os.environ.get('LOG_LEVEL', logging.INFO))
logger.addHandler(ch)

sns = boto3.client('sns')

# generally skip rates - this is meant to capture service limits
quota_name_exclusions = [
    'concurrently running',
    'queries',
    'rate quota',
    'rate of'
]

# these servers don't have meaningful service specific usage
skip_services = [
    'app-integrations',
    'acm-pca',
    'amplify',
    'amplifyuibuilder',
    'aoss',
    'appconfig',
    'appfabric',
    'appflow',
    'appintegrations',
    'application-autoscaling',
    'application-cost-profiler',
    'application-signals',
    'b2bi',
    'bcm-data-exports',
    'billingconductor',
    'braket',
    'bugbust',
    'cases',
    'chime',
    'cleanrooms',
    'cleanrooms-ml',
    'cloud9',
    'cloudsearch',
    'codeartifact',
    'codecommit',
    'codeguru-reviewer',
    'codeguruprofiler',
    'codestar',
    'codestar-connections',
    'codestar-notifications',
    'comprehend',
    'comprehendmedical',
    'compute-optimizer',
    'connect',
    'connect-campaigns',
    'crowdscale-usagelimitservice',
    'databrew',
    'datapipeline',
    'datasync',
    'datazone',
    'dax',
    'deadline',
    'deepracer',
    'discovery',
    'evidently',
    'finspace',
    'fis',
    'fms',
    'forecast',
    'frauddetector',
    'gamelift',
    'geo',
    'globalaccelerator',
    'greengrass',
    'groundstation',
    'internetmonitor',
    'iot',
    'iot1click',
    'iotanalytics',
    'iotcore',
    'iotdeviceadvisor',
    'iotevents',
    'iotfleethub',
    'iotfleetwise',
    'iotsitewise',
    'iotthingsgraph',
    'iottwinmaker',
    'iotwireless',
    'ivs',
    'ivschat',
    'kafkaconnect',
    'kendra',
    'kendra-ranking',
    'launchwizard',
    'lex',
    'license-manager',
    'license-manager-linux-subscriptions',
    'license-manager-user-subscriptions',
    'lightsail',
    'lookoutequipment',
    'lookoutmetrics',
    'lookoutvision',
    'm2',
    'machinelearning',
    'managedblockchain',
    'managedblockchain-query',
    'mediaconnect',
    'mediaconvert',
    'medialive',
    'mediapackage',
    'mediapackagev2',
    'mediastore',
    'mediatailor',
    'medical-imaging',
    'mgn',
    'migrationhuborchestrator',
    'migrationhubstrategy',
    'networkinsights',
    'nimble',
    'oam',
    'omics',
    'opsworks',
    'opsworks-cm',
    'organizations',
    'outposts',
    'panorama',
    'payment-cryptography',
    'pca-connector-ad',
    'pca-connector-scep',
    'personalize',
    'pinpoint',
    'private-networks',
    'profile',
    'proton',
    'qapps',
    'qbusiness',
    'qldb',
    'rbin',
    'refactor-spaces',
    'rekognition',
    'resiliencehub',
    'resource-explorer-2',
    'robomaker',
    'rolesanywhere',
    'rum',
    'schemas',
    'scn',
    'sdb',
    'serverlessrepo',
    'signer',
    'simspaceweaver',
    'sms',
    'snow-device-management',
    'snowball',
    'supportapp',
    'swf',
    'tnb',
    'ts',
    'vendor-insights',
    'verifiedpermissions',
    'vmimportexport',
    'voiceid',
    'wam',
    'wellarchitected'
    ]

cloudformation_registry = checker.CheckerRegistry()
cloudformation_registry.register(r'^Stack instances per stack set$', cloudformation_checks.StackInstancesPerStackSetChecker)
cloudformation_registry.register(r'^Stack count$', cloudformation_checks.StackCountChecker)

ebs_registry = checker.CheckerRegistry()
ebs_registry.register(r'^IOPS for Provisioned IOPS SSD \(io1\) volumes$', ebs_checks.ProvisionedIOPSChecker)
ebs_registry.register(r'^IOPS for Provisioned IOPS SSD \(io2\) volumes$', ebs_checks.ProvisionedIOPSChecker)
ebs_registry.register(r'^Snapshots per Region$', ebs_checks.SnapshotsPerRegionChecker)
ebs_registry.register(r'^Archived snapshots per volume$', ebs_checks.ArchivedSnapshotsPerVolumeChecker)

for volume_type in ebs_checks.VolumeTypeStorageChecker.VOLUME_TYPE_MAP.keys():
    ebs_registry.register(f'^Storage for {volume_type} volumes, in TiB$', ebs_checks.VolumeTypeStorageChecker)

ec2_registry = checker.CheckerRegistry()
ec2_registry.register(r'^Running On-Demand Standard \(A, C, D, H, I, M, R, T, Z\) instances$', ec2_checks.RunningOnDemandInstancesChecker)
ec2_registry.register(r'^Client VPN endpoints per Region$', ec2_checks.ClientVPNEndpointsChecker)
ec2_registry.register(r'^AMIs$', ec2_checks.AMIsChecker)
ec2_registry.register(r'^Multicast domain associations per VPC$', ec2_checks.MulticastDomainAssociationsChecker)
ec2_registry.register(r'^Multicast Network Interfaces per transit gateway$', ec2_checks.MulticastNetworkInterfacesChecker)
ec2_registry.register(r'^New Reserved Instances per month', ec2_checks.NewReservedInstancesChecker)
ec2_registry.register(r'^Running Dedicated ([A-Za-z0-9-]+) Hosts', ec2_checks.RunningDedicatedHostsChecker)
ec2_registry.register(r'^Attachments per transit gateway', ec2_checks.AttachmentsPerTransitGatewayChecker)
ec2_registry.register(r'^Transit gateways per account', ec2_checks.TransitGatewaysPerAccountChecker)
ec2_registry.register(r'^VPN connections per VGW$', ec2_checks.VPNConnectionsPerVGWChecker)
ec2_registry.register(r'^VPN connections per region$', ec2_checks.VPNConnectionsPerRegionChecker)
ec2_registry.register(r'^Routes per transit gateway$', ec2_checks.RoutesPerTransitGatewayChecker)
ec2_registry.register(r'^Customer gateways per region$', ec2_checks.CustomerGatewaysPerRegionChecker)
ec2_registry.register(r'^AMI sharing$', ec2_checks.AMISharingChecker)
ec2_registry.register(r'^Routes per Client VPN endpoint$', ec2_checks.RoutesPerClientVPNEndpointChecker)
ec2_registry.register(r'^EC2-VPC Elastic IPs$', ec2_checks.EC2VPCElasticIPsChecker)

efs_registry = checker.CheckerRegistry()
efs_registry.register(r'^File systems per account$', efs_checks.FileSystemsPerAccountChecker)

eks_registry = checker.CheckerRegistry()
eks_registry.register(r'^Clusters$', eks_checks.ClustersChecker)
eks_registry.register(r'^Nodes per managed node group$', eks_checks.NodesPerManagedNodeGroupChecker)
eks_registry.register(r'^Fargate profiles per cluster$', eks_checks.FargateProfilesPerClusterChecker)
eks_registry.register(r'^Managed node groups per cluster$', eks_checks.ManagedNodeGroupsPerClusterChecker)

es_registry = checker.CheckerRegistry()
es_registry.register(r'^Instances per domain$', es_checks.InstancesPerDomainChecker)
es_registry.register(r'^Domains per region$', es_checks.DomainsPerRegionChecker)

rds_registry = checker.CheckerRegistry()
rds_registry.register(r'^Total storage for all DB instances$', rds_checks.TotalStorageForAllDBInstancesChecker)
rds_registry.register(r'^Manual DB cluster snapshots$', rds_checks.ManualDBClusterSnapshotsChecker)
rds_registry.register(r'^Parameter groups$', rds_checks.ParameterGroupsChecker)
rds_registry.register(r'^Manual DB instance snapshots$', rds_checks.ManualDBInstanceSnapshotsChecker)
rds_registry.register(r'^DB clusters$', rds_checks.DBClustersChecker)
rds_registry.register(r'^DB Instances$', rds_checks.DBInstancesChecker)

vpc_registry = checker.CheckerRegistry()
vpc_registry.register(r'^VPCs per Region$', vpc_checks.VPCsPerRegionChecker)
vpc_registry.register(r'^Subnets per VPC$', vpc_checks.SubnetsPerVPCChecker)
vpc_registry.register(r'^Network interfaces per Region$', vpc_checks.NetworkInterfacesPerRegionChecker)
vpc_registry.register(r'^Route tables per VPC$', vpc_checks.RouteTablesPerVPCChecker)

workspaces_registry = checker.CheckerRegistry()
workspaces_registry.register(r'^GraphicsPro WorkSpaces$', workspaces_checks.WorkspacesChecker)
workspaces_registry.register(r'^Standby WorkSpaces$', workspaces_checks.WorkspacesChecker)
workspaces_registry.register(r'^WorkSpaces$', workspaces_checks.WorkspacesChecker)
workspaces_registry.register(r'^Images$', workspaces_checks.WorkspacesImagesChecker)

route53_registry = checker.CheckerRegistry()
route53_registry.register(r'^Hosted zones$', route53_checks.HostedZonesChecker)
route53_registry.register(r'^Health checks$', route53_checks.HealthChecksChecker)

# Configure boto3 client with adaptive retries for throttling
BOTO_CONFIG = Config(
    retries={
        'max_attempts': 5,
        'mode': 'adaptive'  # Automatically handles throttling with exponential backoff
    }
)

# Rate limiting delay between API calls (in seconds)
# ~6-7 requests/second, safely under AWS rate limits
API_RATE_LIMIT_DELAY = 0.15

def handler(event, context):
    regions = os.environ['SERVICE_QUOTA_REGION_LIST'].split(',')

    results = {}
    for region in regions:
        region_results = check_quotas_in_region(region)
        if region_results:
            results[region] = region_results

    if results:
        sns_topic_arn = os.environ['SNS_TOPIC_ARN']
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=json.dumps(results),
            Subject="Service quotas approaching limits"
        )

    return

def check_quotas_in_region(region):
    quota_client = boto3.client('service-quotas', region_name=region, config=BOTO_CONFIG)
    ec2_client = boto3.client('ec2', region_name=region, config=BOTO_CONFIG)

    threshold = float(os.environ['SERVICE_QUOTA_THRESHOLD']) / 100

    results = []

    try:
        for service in list_all_services(quota_client):
            service_code = service['ServiceCode']

            logger.debug(f"Checking service {service_code} in {region}")
            for quota in list_all_service_quotas(quota_client, service_code):

                if service_code == 's3':
                    logger.debug(f"Checking quota {quota['QuotaName']} for service {service_code} in {region}")

                # Skip hard limits here, we may want to manually check key hard limits separately
                # But there are too many for meaningful querying
                if quota['Adjustable'] == True and not any(exclusion in quota['QuotaName'].lower() for exclusion in quota_name_exclusions):
                    usage = get_quota_usage(quota, service_code, region)
                    limit = quota['Value']

                    if usage and limit > 0 and usage / limit >= threshold:
                        logger.info(f"Service {service['ServiceName']} has {usage} of {limit} ({usage / limit * 100}%) which is approaching the limit")
                        results.append({
                            'ServiceName': service['ServiceName'],
                            'QuotaName': quota['QuotaName'],
                            'Usage': usage,
                            'Limit': limit,
                            'Percentage': (usage / limit) * 100
                        })
    except Exception as e:
        logger.error(f"Error checking {region}: {str(e)}")
        results.append({
            'Error': f"Error checking {region}: {str(e)}"
        })

    return results

def list_all_services(client):
    services = []
    paginator = client.get_paginator('list_services')
    for page in paginator.paginate():
        for service in page['Services']:
            if service['ServiceCode'] not in skip_services:
                services.append(service)
        time.sleep(API_RATE_LIMIT_DELAY)
    return services

def list_all_service_quotas(client, service_code):
    quotas = []
    paginator = client.get_paginator('list_service_quotas')
    for page in paginator.paginate(ServiceCode=service_code):
        quotas.extend(page['Quotas'])
        time.sleep(API_RATE_LIMIT_DELAY)
    return quotas

def get_quota_usage(quota, service_code, region):
    if 'UsageMetric' in quota:
        value = get_cloudwatch_metric_value(boto3.client('cloudwatch', region_name=region), quota['UsageMetric'])
        return value
    else:
        return get_service_specific_usage(service_code, quota, region)

def get_cloudwatch_metric_value(cloudwatch_client, usage_metric):
    try:
        dimensions = []
        if 'MetricDimensions' in usage_metric and isinstance(usage_metric['MetricDimensions'], list):
            for dim in usage_metric['MetricDimensions']:
                if isinstance(dim, dict) and 'Name' in dim and 'Value' in dim:
                    dimensions.append({'Name': dim['Name'], 'Value': dim['Value']})

        response = cloudwatch_client.get_metric_statistics(
            Namespace=usage_metric['MetricNamespace'],
            MetricName=usage_metric['MetricName'],
            Dimensions=dimensions,
            StartTime=datetime.utcnow() - timedelta(minutes=10),
            EndTime=datetime.utcnow(),
            Period=300,
            Statistics=[usage_metric.get('MetricStatisticRecommendation', 'Maximum')]
        )

        # this will typically be no data
        if response['Datapoints']:
            logger.debug(f"Getting cloudwatch metric value for {usage_metric['MetricNamespace']} - {usage_metric['MetricName']}")
            return response['Datapoints'][0]['Maximum']
        else:
            return None
    except Exception as e:
        print(f"Error getting metric value: {str(e)}")
        return None

def get_service_specific_usage(service_code, quota, region):

    if service_code == 'cloudformation':
        logger.debug(f"Getting service specific usage for {quota['QuotaName']} - {service_code}")
        return get_service_usage(cloudformation_registry, quota['QuotaName'], region)
    elif service_code == 'ebs':
        logger.debug(f"Getting service specific usage for {quota['QuotaName']} - {service_code}")
        return get_service_usage(ebs_registry, quota['QuotaName'], region)
    elif service_code == 'ec2':
        logger.debug(f"Getting service specific usage for {quota['QuotaName']} - {service_code}")
        return get_service_usage(ec2_registry, quota['QuotaName'], region)
    elif service_code == 'efs':
        logger.debug(f"Getting service specific usage for {quota['QuotaName']} - {service_code}")
        return get_service_usage(efs_registry, quota['QuotaName'], region)
    elif service_code == 'eks':
        logger.debug(f"Getting service specific usage for {quota['QuotaName']} - {service_code}")
        return get_service_usage(eks_registry, quota['QuotaName'], region)
    elif service_code == 'es':
        logger.debug(f"Getting service specific usage for {quota['QuotaName']} - {service_code}")
        return get_service_usage(es_registry, quota['QuotaName'], region)
    elif service_code == 'rds':
        logger.debug(f"Getting service specific usage for {quota['QuotaName']} - {service_code}")
        return get_service_usage(rds_registry, quota['QuotaName'], region)
    elif service_code == 'route53':
        logger.debug(f"Getting service specific usage for {quota['QuotaName']} - {service_code}")
        return get_service_usage(route53_registry, quota['QuotaName'], region)
    elif service_code == 'vpc':
        logger.debug(f"Getting service specific usage for {quota['QuotaName']} - {service_code}")
        return get_service_usage(vpc_registry, quota['QuotaName'], region)
    elif service_code == 'workspaces':
        logger.debug(f"Getting service specific usage for {quota['QuotaName']} - {service_code}")
        return get_service_usage(workspaces_registry, quota['QuotaName'], region)
    else:
        logger.debug(f"Unsupported service - {quota['QuotaName']} - {service_code}")
        return None

def get_service_usage(registry, quota_name, region):

    try:
        checker = registry.get_checker(quota_name)
        if checker:
            return checker.get_usage(region, quota_name)
        else:
            logger.debug(f"No checker found for {quota_name}")
            return None
    except Exception as e:
        logger.error(f"Error getting usage: {str(e)}")
        return None
# For local testing
if __name__ == "__main__":
    os.environ['SERVICE_QUOTA_REGION_LIST'] = 'us-east-1'
    os.environ['SERVICE_QUOTA_THRESHOLD'] = '20'
    print(handler({}, None))
    print(handler({}, None))
    print(handler({}, None))
