from abc import ABC, abstractmethod
import boto3
from datetime import datetime

class RDSClientSingleton:
    _instances = {}

    @classmethod
    def get_client(cls, region):
        if region not in cls._instances:
            cls._instances[region] = boto3.client('rds', region_name=region)
        return cls._instances[region]

class RDSUsageChecker(ABC):

    @abstractmethod
    def get_usage(self, region, quota_name):
        pass

# This doesn't include aurora. not sure if the service limit does or not.
class TotalStorageForAllDBInstancesChecker(RDSUsageChecker):
    def get_usage(self, region, quota_name):
        rds = RDSClientSingleton.get_client(region)
        total_storage = 0
        marker = None

        while True:
            if marker:
                response = rds.describe_db_instances(Marker=marker)
            else:
                response = rds.describe_db_instances()

            for db_instance in response['DBInstances']:
                total_storage += db_instance['AllocatedStorage']

            marker = response.get('Marker')
            if not marker:
                break

        return total_storage  # This is in GiB

class ManualDBClusterSnapshotsChecker(RDSUsageChecker):
    def get_usage(self, region, quota_name):
        rds = RDSClientSingleton.get_client(region)
        manual_snapshot_count = 0
        marker = None

        while True:
            if marker:
                response = rds.describe_db_cluster_snapshots(
                    SnapshotType='manual',
                    Marker=marker
                )
            else:
                response = rds.describe_db_cluster_snapshots(
                    SnapshotType='manual'
                )

            manual_snapshot_count += len(response['DBClusterSnapshots'])

            marker = response.get('Marker')
            if not marker:
                break

        return manual_snapshot_count

class ParameterGroupsChecker(RDSUsageChecker):
    def get_usage(self, region, quota_name):
        rds = RDSClientSingleton.get_client(region)
        parameter_group_count = 0
        marker = None

        while True:
            if marker:
                response = rds.describe_db_parameter_groups(Marker=marker)
            else:
                response = rds.describe_db_parameter_groups()

            parameter_group_count += len(response['DBParameterGroups'])

            marker = response.get('Marker')
            if not marker:
                break

        return parameter_group_count

class ManualDBInstanceSnapshotsChecker(RDSUsageChecker):
    def get_usage(self, region, quota_name):
        rds = RDSClientSingleton.get_client(region)
        manual_snapshot_count = 0
        marker = None

        while True:
            if marker:
                response = rds.describe_db_snapshots(
                    SnapshotType='manual',
                    Marker=marker
                )
            else:
                response = rds.describe_db_snapshots(
                    SnapshotType='manual'
                )

            manual_snapshot_count += len(response['DBSnapshots'])

            marker = response.get('Marker')
            if not marker:
                break

        return manual_snapshot_count

class DBClustersChecker(RDSUsageChecker):
    def get_usage(self, region, quota_name):
        rds = RDSClientSingleton.get_client(region)
        cluster_count = 0
        marker = None

        while True:
            if marker:
                response = rds.describe_db_clusters(Marker=marker)
            else:
                response = rds.describe_db_clusters()

            cluster_count += len(response['DBClusters'])

            marker = response.get('Marker')
            if not marker:
                break

        return cluster_count

class DBInstancesChecker(RDSUsageChecker):
    def get_usage(self, region, quota_name):
        rds = RDSClientSingleton.get_client(region)
        instance_count = 0
        marker = None

        while True:
            if marker:
                response = rds.describe_db_instances(Marker=marker)
            else:
                response = rds.describe_db_instances()

            instance_count += len(response['DBInstances'])

            marker = response.get('Marker')
            if not marker:
                break

        return instance_count
