from abc import ABC, abstractmethod
import boto3


class EKSClientSingleton:
    _instances = {}

    @classmethod
    def get_client(cls, region):
        if region not in cls._instances:
            cls._instances[region] = boto3.client('eks', region_name=region)
        return cls._instances[region]

class EKSUsageChecker(ABC):

    @abstractmethod
    def get_usage(self, region, quota_name):
        pass

class ClustersChecker(EKSUsageChecker):
    def get_usage(self, region, quota_name):
        eks = EKSClientSingleton.get_client(region)
        clusters = []
        next_token = None

        while True:
            if next_token:
                response = eks.list_clusters(nextToken=next_token)
            else:
                response = eks.list_clusters()

            clusters.extend(response['clusters'])

            next_token = response.get('nextToken')
            if not next_token:
                break

        return len(clusters)

class NodesPerManagedNodeGroupChecker(EKSUsageChecker):
    def get_usage(self, region, quota_name):
        eks = EKSClientSingleton.get_client(region)
        max_nodes = 0

        # List all clusters
        clusters = []
        next_token = None
        while True:
            if next_token:
                response = eks.list_clusters(nextToken=next_token)
            else:
                response = eks.list_clusters()
            clusters.extend(response['clusters'])
            next_token = response.get('nextToken')
            if not next_token:
                break

        # For each cluster, check all managed node groups
        for cluster_name in clusters:
            nodegroups = []
            next_token = None
            while True:
                if next_token:
                    response = eks.list_nodegroups(clusterName=cluster_name, nextToken=next_token)
                else:
                    response = eks.list_nodegroups(clusterName=cluster_name)
                nodegroups.extend(response['nodegroups'])
                next_token = response.get('nextToken')
                if not next_token:
                    break

            for nodegroup_name in nodegroups:
                nodegroup = eks.describe_nodegroup(clusterName=cluster_name, nodegroupName=nodegroup_name)
                scaling_config = nodegroup['nodegroup']['scalingConfig']
                max_nodes = max(max_nodes, scaling_config['maxSize'])

        return max_nodes

class FargateProfilesPerClusterChecker(EKSUsageChecker):
    def get_usage(self, region, quota_name):
        eks = EKSClientSingleton.get_client(region)
        max_profiles = 0

        # List all clusters
        clusters = []
        next_token = None
        while True:
            if next_token:
                response = eks.list_clusters(nextToken=next_token)
            else:
                response = eks.list_clusters()
            clusters.extend(response['clusters'])
            next_token = response.get('nextToken')
            if not next_token:
                break

        # For each cluster, count Fargate profiles
        for cluster_name in clusters:
            profiles = []
            next_token = None
            while True:
                if next_token:
                    response = eks.list_fargate_profiles(clusterName=cluster_name, nextToken=next_token)
                else:
                    response = eks.list_fargate_profiles(clusterName=cluster_name)
                profiles.extend(response['fargateProfileNames'])
                next_token = response.get('nextToken')
                if not next_token:
                    break

            max_profiles = max(max_profiles, len(profiles))

        return max_profiles

class ManagedNodeGroupsPerClusterChecker(EKSUsageChecker):
    def get_usage(self, region, quota_name):
        eks = EKSClientSingleton.get_client(region)
        max_node_groups = 0

        # List all clusters
        clusters = []
        next_token = None
        while True:
            if next_token:
                response = eks.list_clusters(nextToken=next_token)
            else:
                response = eks.list_clusters()
            clusters.extend(response['clusters'])
            next_token = response.get('nextToken')
            if not next_token:
                break

        # For each cluster, count managed node groups
        for cluster_name in clusters:
            node_groups = []
            next_token = None
            while True:
                if next_token:
                    response = eks.list_nodegroups(clusterName=cluster_name, nextToken=next_token)
                else:
                    response = eks.list_nodegroups(clusterName=cluster_name)
                node_groups.extend(response['nodegroups'])
                next_token = response.get('nextToken')
                if not next_token:
                    break

            max_node_groups = max(max_node_groups, len(node_groups))

        return max_node_groups
