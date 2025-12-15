from abc import ABC, abstractmethod
import boto3
from datetime import datetime

class ESClientSingleton:
    _instances = {}

    @classmethod
    def get_client(cls, region):
        if region not in cls._instances:
            cls._instances[region] = boto3.client('es', region_name=region)
        return cls._instances[region]

class ESUsageChecker(ABC):

    @abstractmethod
    def get_usage(self, region, quota_name):
        pass

class InstancesPerDomainChecker(ESUsageChecker):
    def get_usage(self, region, quota_name):
        es = ESClientSingleton.get_client(region)
        max_instances = 0
        next_token = None

        while True:
            if next_token:
                response = es.list_domain_names(NextToken=next_token)
            else:
                response = es.list_domain_names()

            for domain in response['DomainNames']:
                domain_name = domain['DomainName']
                domain_config = es.describe_elasticsearch_domain_config(DomainName=domain_name)
                instance_count = domain_config['DomainConfig']['ElasticsearchClusterConfig'].get('InstanceCount', 0)
                max_instances = max(max_instances, instance_count)

            next_token = response.get('NextToken')
            if not next_token:
                break

        return max_instances

class DomainsPerRegionChecker(ESUsageChecker):
    def get_usage(self, region, quota_name):
        es = ESClientSingleton.get_client(region)
        domain_count = 0
        next_token = None

        while True:
            if next_token:
                response = es.list_domain_names(NextToken=next_token)
            else:
                response = es.list_domain_names()

            domain_count += len(response['DomainNames'])

            next_token = response.get('NextToken')
            if not next_token:
                break

        return domain_count
