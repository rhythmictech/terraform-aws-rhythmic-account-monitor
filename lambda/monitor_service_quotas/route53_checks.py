from abc import ABC, abstractmethod
import boto3


class Route53ClientSingleton:
    _instances = {}

    @classmethod
    def get_client(cls, region):
        if region not in cls._instances:
            cls._instances[region] = boto3.client('route53', region_name=region)
        return cls._instances[region]

class Route53UsageChecker(ABC):

    @abstractmethod
    def get_usage(self, region, quota_name):
        pass

class HostedZonesChecker(Route53UsageChecker):
    def get_usage(self, region, quota_name):
        route53 = Route53ClientSingleton.get_client(region)
        count = 0
        next_marker = None

        while True:
            if next_marker:
                response = route53.list_hosted_zones(Marker=next_marker)
            else:
                response = route53.list_hosted_zones()

            count += len(response['HostedZones'])

            if response['IsTruncated']:
                next_marker = response['NextMarker']
            else:
                break

        return count

class HealthChecksChecker(Route53UsageChecker):
    def get_usage(self, region, quota_name):
        route53 = Route53ClientSingleton.get_client(region)
        count = 0
        next_marker = None

        while True:
            if next_marker:
                response = route53.list_health_checks(Marker=next_marker)
            else:
                response = route53.list_health_checks()

            count += len(response['HealthChecks'])

            if 'NextMarker' in response:
                next_marker = response['NextMarker']
            else:
                break

        return count
