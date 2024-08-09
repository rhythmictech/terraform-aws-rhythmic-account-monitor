from abc import ABC, abstractmethod
import boto3
from datetime import datetime
import logging
logger = logging.getLogger(__name__)


class WorkspacesClientSingleton:
    _instances = {}

    @classmethod
    def get_client(cls, region):
        if region not in cls._instances:
            cls._instances[region] = boto3.client('workspaces', region_name=region)
        return cls._instances[region]

class WorkspacesUsageChecker(ABC):

    @abstractmethod
    def get_usage(self, region, quota_name):
        pass

class WorkspacesChecker(WorkspacesUsageChecker):
    def get_usage(self, region, quota_name):
        workspaces = WorkspacesClientSingleton.get_client(region)
        count = 0
        next_token = None

        target_type = None
        if "Standby" in quota_name:
            target_type = "STANDBY"
        elif "GraphicsPro" in quota_name:
            target_type = "GRAPHICS_PRO"

        while True:
            if next_token:
                response = workspaces.describe_workspaces(NextToken=next_token)
            else:
                response = workspaces.describe_workspaces()

            for workspace in response['Workspaces']:
                if target_type == "STANDBY":
                    if workspace['State'] == 'STOPPED':
                        count += 1
                elif target_type == "GRAPHICS_PRO":
                    if workspace['WorkspaceProperties']['ComputeTypeName'].startswith('GRAPHICS_PRO'):
                        count += 1
                else:
                    count += 1

            next_token = response.get('NextToken')
            if not next_token:
                break

        return count

class WorkspacesImagesChecker(WorkspacesUsageChecker):
    def get_usage(self, region, quota_name):
        workspaces = WorkspacesClientSingleton.get_client(region)
        count = 0
        next_token = None

        while True:
            if next_token:
                response = workspaces.describe_workspace_images(NextToken=next_token)
            else:
                response = workspaces.describe_workspace_images()

            for image in response['Images']:
                if image['OwnerAccountId'] == workspaces.meta.client.meta.partition_data['accountId']:
                    count += 1

            next_token = response.get('NextToken')
            if not next_token:
                break

        return count
