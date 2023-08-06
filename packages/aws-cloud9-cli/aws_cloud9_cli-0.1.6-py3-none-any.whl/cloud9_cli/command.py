from inquirer import prompt, List, Text

import boto3
from botocore.config import Config
from botocore import session

from cloud9_cli.create_yaml import CreateYAML
from cloud9_cli.utils import print_figlet
from cloud9_cli.validators import name_validator, instance_type_validator, owner_arn_validator
from cloud9_cli.deploy_cfn import DeployCfn


class Command:
    # variables
    project = None
    region = None
    environment_name = None
    instance_type = None
    platform = None
    owner_arn = None
    vpc = None
    subnet = None

    def __init__(self):
        print_figlet()

        self.set_project_name()
        self.choose_region()
        self.set_environment_name()

        self.get_instance_type()
        if not self.instance_type:
            return

        self.choose_platform()

        self.set_owner_arn()

        self.choose_vpc()
        if not self.vpc:  # no vpc found in that region
            return

        self.choose_subnet()
        if not self.subnet:
            return

        # create template yaml file
        yaml_file = CreateYAML(
            project=self.project,
            region=self.region,
            environment_name=self.environment_name,
            instance_type=self.instance_type,
            platform=self.platform,
            owner_arn=self.owner_arn,
            vpc=self.vpc,
            subnet=self.subnet,
        )
        yaml_file.create_yaml()

        DeployCfn(region=self.region, project=self.project)

    def set_project_name(self):
        questions = [
            Text(
                name='name',
                message='Project name',
                validate=lambda _, x: name_validator(x)
            )
        ]

        answer = prompt(questions=questions, raise_keyboard_interrupt=True)
        self.project = answer['name']

    def choose_region(self):
        questions = [
            List(
                name='region',
                message='Choose region',
                choices=[
                    ('us-east-1      (N. Virginia)', 'us-east-1'),
                    ('us-east-2      (Ohio)', 'us-east-2'),
                    ('us-west-1      (N. California)', 'us-west-1'),
                    ('us-west-2      (Oregon)', 'us-west-2'),
                    ('ap-south-1     (Mumbai)', 'ap-south-1'),
                    ('ap-northeast-3 (Osaka)', 'ap-northeast-3'),
                    ('ap-northeast-2 (Seoul)', 'ap-northeast-2'),
                    ('ap-southeast-1 (Singapore)', 'ap-southeast-1'),
                    ('ap-southeast-2 (Sydney)', 'ap-southeast-2'),
                    ('ap-northeast-1 (Tokyo)', 'ap-northeast-1'),
                    ('ca-central-1   (Canada Central)', 'ca-central-1'),
                    ('eu-central-1   (Frankfurt)', 'eu-central-1'),
                    ('eu-west-1      (Ireland)', 'eu-west-1'),
                    ('eu-west-2      (London)', 'eu-west-2'),
                    ('eu-west-3      (Paris)', 'eu-west-3'),
                    ('eu-north-1     (Stockholm)', 'eu-north-1'),
                    ('sa-east-1      (Sao Paulo)', 'sa-east-1')
                ]
            )
        ]

        answer = prompt(questions=questions, raise_keyboard_interrupt=True)
        self.region = answer.get('region')

    def set_environment_name(self):
        questions = [
            Text(
                name='name',
                message='Enter the environment name',
                validate=lambda _, x: name_validator(x)
            )
        ]

        answer = prompt(questions=questions, raise_keyboard_interrupt=True)
        self.environment_name = answer.get('name')

    def get_instance_type(self):
        questions = [
            List(
                name='type',
                message='Choose the instance type',
                choices=[
                    ('t2.micro (1 GiB RAM + 1 vCPU)', 't2.micro'),
                    ('t3.small (2 GiB RAM + 2 vCPU)', 't3.small'),
                    ('m5.large (8 GiB RAM + 2 vCPU)', 'm5.large'),
                ],
                other=True,
                validate=lambda _, x: instance_type_validator(x)
            )
        ]

        answer = prompt(questions=questions, raise_keyboard_interrupt=True)
        instance_type = answer.get('type')

        self.instance_type = instance_type

    def choose_platform(self):
        questions = [
            List(
                name='platform',
                message='Choose region',
                choices=[
                    ('Amazon Linux 2', 'amazonlinux-2-x86_64'),
                    ('Amazon Linux 1', 'amazonlinux-1-x86_64'),
                    ('Ubuntu 18.04', 'ubuntu-18.04-x86_64'),
                ]
            )
        ]

        answer = prompt(questions=questions, raise_keyboard_interrupt=True)
        self.platform = answer.get('platform')

    def set_owner_arn(self):
        questions = [
            Text(
                name='arn',
                message='Enter the owner ARN',
                validate=lambda _, x: owner_arn_validator(x),
                default=boto3.client('sts').get_caller_identity()['Arn']
            )
        ]

        answer = prompt(questions=questions, raise_keyboard_interrupt=True)
        self.owner_arn = answer.get('arn')

    def choose_vpc(self):
        response = session.get_session().create_client('ec2', config=Config(region_name=self.region)).describe_vpcs()

        if not response['Vpcs']:  # no vpc found in that region
            print('There\'s no any vpcs. Try another region.')

            return

        else:
            vpc_list = []

            for vpc in response['Vpcs']:
                vpc_id = vpc['VpcId']
                cidr = vpc['CidrBlock']
                name = next((item['Value'] for item in vpc.get('Tags', {}) if item['Key'] == 'Name'), None)

                vpc_show_data = f'{vpc_id} ({cidr}{f", {name}" if name else ""})'
                vpc_list.append((vpc_show_data, vpc_id))

            questions = [
                List(
                    name='vpc',
                    message='Choose vpc',
                    choices=vpc_list
                )
            ]

            answer = prompt(questions=questions, raise_keyboard_interrupt=True)
            self.vpc = answer.get('vpc')

    def choose_subnet(self):
        response = session.get_session().create_client('ec2', config=Config(region_name=self.region)).describe_subnets(
            Filters=[{'Name': 'vpc-id', 'Values': [self.vpc]}]
        )

        if not response['Subnets']:  # no vpc found in that region
            print('There\'s no any subnets. Try another vpc.')

            return

        else:
            subnet_list = []

            for subnet in response['Subnets']:
                subnet_id = subnet['SubnetId']
                az = subnet['AvailabilityZone']
                cidr = subnet['CidrBlock']
                name = next((item['Value'] for item in subnet.get('Tags', {}) if item['Key'] == 'Name'), None)

                subnet_show_data = f'{subnet_id} ({cidr}, {az}{f", {name}" if name else ""})'
                subnet_list.append((subnet_show_data, (subnet_id, az)))

            questions = [
                List(
                    name='subnet',
                    message='Choose subnet',
                    choices=subnet_list
                )
            ]

            answer = prompt(questions=questions, raise_keyboard_interrupt=True)
            self.subnet = answer.get('subnet')[0]
