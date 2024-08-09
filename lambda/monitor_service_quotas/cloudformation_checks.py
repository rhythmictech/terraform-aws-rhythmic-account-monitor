from abc import ABC, abstractmethod
import boto3
from datetime import datetime

class CloudFormationClientSingleton:
    _instances = {}

    @classmethod
    def get_client(cls, region):
        if region not in cls._instances:
            cls._instances[region] = boto3.client('cloudformation', region_name=region)
        return cls._instances[region]

class CloudFormationUsageChecker(ABC):

    @abstractmethod
    def get_usage(self, region, quota_name):
        pass

class StackInstancesPerStackSetChecker(CloudFormationUsageChecker):
    def get_usage(self, region, quota_name):
        cfn_client = CloudFormationClientSingleton.get_client(region)
        paginator = cfn_client.get_paginator('list_stack_sets')
        max_instances = 0

        for page in paginator.paginate():
            for stack_set in page['Summaries']:
                stack_set_name = stack_set['StackSetName']
                instances = cfn_client.list_stack_instances(StackSetName=stack_set_name)['Summaries']
                instance_count = len(instances)
                max_instances = max(max_instances, instance_count)
        return max_instances


class StackCountChecker(CloudFormationUsageChecker):
    def get_usage(self, region, quota_name):
        cfn_client = CloudFormationClientSingleton.get_client(region)
        paginator = cfn_client.get_paginator('list_stacks')
        stack_count = 0

        for page in paginator.paginate(StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE']):
            stack_count += len(page['StackSummaries'])

        return stack_count
