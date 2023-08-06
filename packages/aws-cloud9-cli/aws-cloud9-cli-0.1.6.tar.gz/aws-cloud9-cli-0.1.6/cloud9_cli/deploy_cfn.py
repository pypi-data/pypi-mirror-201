import json
import boto3
from botocore.config import Config
from inquirer import prompt, Confirm, Text
from prettytable import PrettyTable
from cfn_visualizer import visualizer

from cloud9_cli.validators import stack_name_validator


class DeployCfn:
    client = None
    deploy = False
    name = ''
    region = ''
    project = ''

    def __init__(
            self,
            region,
            project,
    ):
        self.region = region
        self.project = project
        self.ask_deployment()
        self.input_stack_name()
        self.create_iam_roles()
        self.deployment(self.name, region)

    def ask_deployment(self):
        questions = [
            Confirm(
                name='required',
                message='Do you want to deploy using CloudFormation in here?',
                default=True
            )
        ]

        self.deploy = prompt(questions=questions, raise_keyboard_interrupt=True)['required']

    def input_stack_name(self):
        questions = [
            Text(
                name='name',
                message='Type CloudFormation Stack name',
                validate=lambda _, x: stack_name_validator(x, self.region),
            )
        ]

        self.name = prompt(questions=questions, raise_keyboard_interrupt=True)['name']

    def create_iam_roles(self):
        print('Create the Cloud9 SSM role...')

        client = boto3.client('iam')

        # create `AWSCloud9SSMAccessRole`
        try:
            assume_role_policy = {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Effect': 'Allow',
                        'Principal': {
                            'Service': [
                                'cloud9.amazonaws.com',
                                'ec2.amazonaws.com'
                            ]
                        },
                        'Action': 'sts:AssumeRole'
                    }
                ]
            }
            client.create_role(
                Path='/service-role/',
                RoleName='AWSCloud9SSMAccessRole',
                AssumeRolePolicyDocument=json.dumps(assume_role_policy),
            )

        except client.exceptions.EntityAlreadyExistsException:
            pass

        # attach managed policy to `AWSCloud9SSMAccessRole`
        try:
            client.attach_role_policy(
                RoleName='AWSCloud9SSMAccessRole',
                PolicyArn='arn:aws:iam::aws:policy/AWSCloud9SSMInstanceProfile',
            )
        except client.exceptions.UnmodifiableEntityException:
            pass

        # create `AWSCloud9SSMInstanceProfile`
        try:
            client.create_instance_profile(
                InstanceProfileName='AWSCloud9SSMInstanceProfile',
                Path='/cloud9/'
            )

        except client.exceptions.EntityAlreadyExistsException:
            pass

        # add `AWSCloud9SSMAccessRole` to `AWSCloud9SSMInstanceProfile`
        try:
            client.add_role_to_instance_profile(
                InstanceProfileName='AWSCloud9SSMInstanceProfile',
                RoleName='AWSCloud9SSMAccessRole',
            )
        except client.exceptions.LimitExceededException:
            pass

    def deployment(self, name, region):
        if self.deploy:  # deploy using cloudformation
            self.client = boto3.client('cloudformation', config=Config(region_name=region))
            response = self.client.create_stack(
                StackName=name,
                TemplateBody=self.get_template(),
                TimeoutInMinutes=15,
                Capabilities=['CAPABILITY_NAMED_IAM'],
                Tags=[{'Key': 'Name', 'Value': name}, {'Key': 'project', 'Value': self.project}],
            )
            stack_id = response['StackId']

            while True:
                # 1. get stack status
                response = self.client.describe_stacks(
                    StackName=name
                )
                stack_status = response['Stacks'][0]['StackStatus']

                if stack_status in ['CREATE_FAILED', 'ROLLBACK_FAILED',
                                    'ROLLBACK_COMPLETE']:  # create failed
                    print()
                    print('\x1b[31m' + 'Failed!' + '\x1b[0m')
                    print()
                    print('\x1b[31m' + 'Please check CloudFormation at here:' + '\x1b[0m')
                    print()
                    print(
                        '\x1b[31m' +
                        'https://{0}.console.aws.amazon.com/cloudformation/home?region={0}#/stacks/stackinfo?stackId={1}'.format(
                            region, stack_id) +
                        '\x1b[0m')
                    break

                elif stack_status == 'CREATE_COMPLETE':  # create complete successful
                    print()
                    self.print_table()
                    print('\x1b[32m' + 'Success!' + '\x1b[0m')
                    print()
                    print('\x1b[32m' + 'You can access IDE in here:' + '\x1b[0m')
                    print()
                    url = next((item['OutputValue'] for item in
                                boto3.client('cloudformation', config=Config(region_name=region)).describe_stacks(
                                    StackName=name)['Stacks'][0]['Outputs'] if item['OutputKey'] == 'EnvironmentUrl'),
                               False)
                    print('\x1b[32m' + url + '\x1b[0m')

                    break

                else:
                    visualizer(self.client, self.name)

        else:
            print('Done!\n\n')
            print('You can deploy Bastion EC2 using AWS CLI\n\n\n')
            print(
                'aws cloudformation deploy --stack-name {} --region {} --template-file ./cloud9.yaml'.format(
                    name, region))

    def get_template(self):
        with open('cloud9.yaml', 'r') as f:
            content = f.read()

        return content

    def print_table(self):
        table = PrettyTable()
        table.set_style(15)
        table.field_names = ['Logical ID', 'Physical ID', 'Type']
        table.vrules = 0
        table.hrules = 1
        table.align = 'l'
        rows = []

        response = self.client.describe_stack_resources(StackName=self.name)['StackResources']

        for resource in response:
            rows.append([resource['LogicalResourceId'], resource['PhysicalResourceId'], resource['ResourceType']])

        rows = sorted(rows, key=lambda x: (x[2], x[0]))
        table.add_rows(rows)
        print(table)
