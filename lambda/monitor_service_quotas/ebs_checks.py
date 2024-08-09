from abc import ABC, abstractmethod
import boto3
from datetime import datetime

class EBSClientSingleton:
    _instances = {}

    @classmethod
    def get_client(cls, region):
        if region not in cls._instances:
            cls._instances[region] = boto3.client('ec2', region_name=region)
        return cls._instances[region]

class EBSUsageChecker(ABC):

    @abstractmethod
    def get_usage(self, region, quota_name):
        pass

class VolumeTypeStorageChecker(EBSUsageChecker):
    VOLUME_TYPE_MAP = {
        'Cold HDD (sc1)': 'sc1',
        'Throughput Optimized HDD (st1)': 'st1',
        'General Purpose SSD (gp2)': 'gp2',
        'General Purpose SSD (gp3)': 'gp3',
        'Provisioned IOPS SSD (io1)': 'io1',
        'Provisioned IOPS SSD (io2)': 'io2',
        'Magnetic (standard)': 'standard'
    }

    def get_usage(self, region, quota_name):
        ebs = EBSClientSingleton.get_client(region)
        total_storage = 0
        next_token = None

        volume_type = self.VOLUME_TYPE_MAP.get(quota_name.split(' volumes')[0].strip())
        if not volume_type:
            raise ValueError(f"Unknown volume type in quota: {quota_name}")

        while True:
            if next_token:
                response = ec2.describe_volumes(
                    Filters=[{'Name': 'volume-type', 'Values': [volume_type]}],
                    NextToken=next_token
                )
            else:
                response = ec2.describe_volumes(
                    Filters=[{'Name': 'volume-type', 'Values': [volume_type]}]
                )

            for volume in response['Volumes']:
                total_storage += volume['Size']

            next_token = response.get('NextToken')
            if not next_token:
                break

        return total_storage

class ProvisionedIOPSChecker(EBSUsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EBSClientSingleton.get_client(region)
        total_iops = 0
        next_token = None

        volume_type = quota_name.split('IOPS for Provisioned IOPS SSD (')[1].split(')')[0]
        while True:
            if next_token:
                response = ec2.describe_volumes(
                    Filters=[{'Name': 'volume-type', 'Values': ['io2']}],
                    NextToken=next_token
                )
            else:
                response = ec2.describe_volumes(
                    Filters=[{'Name': 'volume-type', 'Values': ['io2']}]
                )

            for volume in response['Volumes']:
                total_iops += volume['Iops']

            next_token = response.get('NextToken')
            if not next_token:
                break

        return total_iops

class ArchivedSnapshotsPerVolumeChecker(EBSUsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EBSClientSingleton.get_client(region)
        snapshot_counts = {}
        next_token = None

        while True:
            if next_token:
                response = ec2.describe_snapshots(
                    OwnerIds=['self'],
                    Filters=[{'Name': 'storage-tier', 'Values': ['archive']}],
                    NextToken=next_token
                )
            else:
                response = ec2.describe_snapshots(
                    OwnerIds=['self'],
                    Filters=[{'Name': 'storage-tier', 'Values': ['archive']}]
                )

            for snapshot in response['Snapshots']:
                volume_id = snapshot.get('VolumeId')
                if volume_id:
                    snapshot_counts[volume_id] = snapshot_counts.get(volume_id, 0) + 1

            next_token = response.get('NextToken')
            if not next_token:
                break

        return max(snapshot_counts.values()) if snapshot_counts else 0

class SnapshotsPerRegionChecker(EBSUsageChecker):
    def get_usage(self, region, quota_name):
        ec2 = EBSClientSingleton.get_client(region)
        total_snapshots = 0
        next_token = None

        while True:
            if next_token:
                response = ec2.describe_snapshots(
                    OwnerIds=['self'],
                    NextToken=next_token
                )
            else:
                response = ec2.describe_snapshots(
                    OwnerIds=['self']
                )

            total_snapshots += len(response['Snapshots'])

            next_token = response.get('NextToken')
            if not next_token:
                break

        return total_snapshots
