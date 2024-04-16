import boto3
import json
import os
import re

# Initialize the clients
autoscaling = boto3.client('autoscaling')
batch = boto3.client('batch')
beanstalk = boto3.client('elasticbeanstalk')
cloudformation = boto3.client('cloudformation')
ec2 = boto3.client('ec2')
eks = boto3.client('eks')
sns = boto3.client('sns')
workspaces = boto3.client('workspaces')

def lambda_handler(event, context):

    # Check AMIs used in EC2 instances
    unavailable_amis = {}

    instances = ec2.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            ami_id = instance['ImageId']
            ami_response = ec2.describe_images(ImageIds=[ami_id])
            if not ami_response['Images']:
                if ami_id not in unavailable_amis:
                    unavailable_amis[ami_id] = []
                unavailable_amis[ami_id].append(f"instance:{instance['InstanceId']}")

    # Check AMIs used in Auto Scaling groups
    as_groups = autoscaling.describe_auto_scaling_groups()
    for group in as_groups['AutoScalingGroups']:
        launch_config_name = group.get('LaunchConfigurationName')
        if launch_config_name:
            launch_config = autoscaling.describe_launch_configurations(LaunchConfigurationNames=[launch_config_name])
            if launch_config['LaunchConfigurations']:
                ami_id = launch_config['LaunchConfigurations'][0]['ImageId']
                ami_response = ec2.describe_images(ImageIds=[ami_id])
                if not ami_response['Images']:
                    if ami_id not in unavailable_amis:
                        unavailable_amis[ami_id] = []
                    unavailable_amis[ami_id].append(f"asg:{group['AutoScalingGroupName']}")

    # Check AMIs used in Elastic Beanstalk environments
    environments = beanstalk.describe_environments()
    for env in environments['Environments']:
        resources = beanstalk.describe_environment_resources(EnvironmentId=env['EnvironmentId'])
        for instance in resources['EnvironmentResources']['Instances']:
            instance_details = ec2.describe_instances(InstanceIds=[instance['Id']])
            ami_id = instance_details['Reservations'][0]['Instances'][0]['ImageId']
            ami_response = ec2.describe_images(ImageIds=[ami_id])
            if not ami_response['Images']:
                if ami_id not in unavailable_amis:
                    unavailable_amis[ami_id] = []
                unavailable_amis[ami_id].append(f"beanstalk:{env['EnvironmentName']}")

    # Check AMIs used in AWS Batch compute environments
    response = batch.describe_compute_environments()
    for compute_env in response['computeEnvironments']:
        # Retrieve the compute environment details
        if 'computeResources' in compute_env:
            ami_id = compute_env['computeResources'].get('imageId')
            if ami_id:
                ami_response = ec2.describe_images(ImageIds=[ami_id])
                if not ami_response['Images']:
                    if ami_id not in unavailable_amis:
                        unavailable_amis[ami_id] = []
                    unavailable_amis[ami_id].append(f"batch:{compute_env['computeEnvironmentName']}")

    # Get all EKS clusters
    clusters_response = eks.list_clusters()
    clusters = clusters_response['clusters']
    for cluster_name in clusters:
        node_groups_response = eks.list_nodegroups(clusterName=cluster_name)
        node_groups = node_groups_response['nodegroups']

        # Iterate over each node group
        for node_group_name in node_groups:
            node_group_response = eks.describe_nodegroup(clusterName=cluster_name, nodegroupName=node_group_name)
            node_group = node_group_response['nodegroup']

            ami_id = node_group['launchTemplate']['id']
            ami_response = ec2.describe_images(ImageIds=[ami_id])
            if not ami_response['Images']:
                if ami_id not in unavailable_amis:
                    unavailable_amis[ami_id] = []
                unavailable_amis[ami_id].append(f"eks_node_group:{cluster_name}/{node_group_name}")

    ami_regex = re.compile(r"ami-[a-f0-9]{8,17}")

    # Checks parameters in CloudFormation stacks for AMI IDs. This check isn't perfect.
    # It's possible that the AMI ID is not in a parameter, but is hardcoded in the template.
    stacks = cloudformation.describe_stacks()['Stacks']

    for stack in stacks:
        parameters = stack.get('Parameters', [])
        for param in parameters:
            if ami_regex.match(param['ParameterValue']):
                ami_id = param['ParameterValue']
                ami_response = ec2.describe_images(ImageIds=[ami_id])
            if not ami_response['Images']:
                if ami_id not in unavailable_amis:
                    unavailable_amis[ami_id] = []
                unavailable_amis[ami_id].append(f"cloudformation_stack:{stack['StackName']}")

    if unavailable_amis:

        sns_topic_arn = os.environ['SNS_TOPIC_ARN']  # SNS Topic ARN from environment variable
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=json.dumps(unavailable_amis),
            Subject="Unavailable or deleted AMIs detected"
        )
