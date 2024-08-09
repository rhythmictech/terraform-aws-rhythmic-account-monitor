from abc import ABC, abstractmethod
import boto3
from datetime import datetime

class EFSClientSingleton:
    _instances = {}

    @classmethod
    def get_client(cls, region):
        if region not in cls._instances:
            cls._instances[region] = boto3.client('elasticfilesystem', region_name=region)
        return cls._instances[region]

class EFSUsageChecker(ABC):

    @abstractmethod
    def get_usage(self, region, quota_name):
        pass

class FileSystemsPerAccountChecker(EFSUsageChecker):
    def get_usage(self, region, quota_name):
        efs = EFSClientSingleton.get_client(region)
        file_system_count = 0
        next_token = None

        while True:
            if next_token:
                response = efs.describe_file_systems(MaxItems=100, Marker=next_token)
            else:
                response = efs.describe_file_systems(MaxItems=100)

            file_system_count += len(response['FileSystems'])

            next_token = response.get('NextMarker')
            if not next_token:
                break

        return file_system_count
