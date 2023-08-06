import yaml


class CreateYAML:
    template = {}
    parameters = {}
    resources = {}
    outputs = {}
    project = ''

    def __init__(
            self,
            project,
            region,
            environment_name,
            instance_type,
            platform,
            owner_arn,
            vpc,
            subnet,
    ):
        self.project = project
        self.region = region
        self.environment_name = environment_name
        self.instance_type = instance_type
        self.platform = platform
        self.owner_arn = owner_arn
        self.vpc = vpc
        self.subnet = subnet

        self.create_parameters()
        self.create_environment()
        self.create_outputs()

        self.create_yaml()

    def create_parameters(self):
        self.parameters = {
            'AutomaticStopTimeMinutes': {
                'Type': 'Number',
                'Description': '[REQUIRED] The number of minutes until the running instance is shut down after the environment was last used.',
                'Default': '30'
            },
            'ConnectionType': {
                'Type': 'String',
                'Description': '[REQUIRED] The connection type used for connecting to an Amazon EC2 environment.',
                'Default': 'CONNECT_SSM',
                'AllowedValues': ['CONNECT_SSH', 'CONNECT_SSM']
            },
            'ImageId': {
                'Type': 'String',
                'Description': '[REQUIRED] The identifier for the Amazon Machine Image (AMI) that\'s used to create the EC2 instance.',
                'Default': self.platform,
                'AllowedValues': ['amazonlinux-1-x86_64', 'amazonlinux-2-x86_64', 'ubuntu-18.04-x86_64']
            },
            'InstanceType': {
                'Type': 'String',
                'Description': '[REQUIRED] The type of instance to connect to the environment (for example, t2.micro).',
                'Default': self.instance_type
            },
            'Name': {
                'Type': 'String',
                'Description': '[REQUIRED] The name of the environment.',
                'Default': self.environment_name
            },
            'OwnerArn': {
                'Type': 'String',
                'Description': '[REQUIRED] The Amazon Resource Name (ARN) of the environment owner.',
                'Default': self.owner_arn
            },
            'SubnetId': {
                'Type': 'AWS::EC2::Subnet::Id',
                'Description': '[REQUIRED] The ID of the subnet in Amazon Virtual Private Cloud (Amazon VPC) that AWS Cloud9 will use to communicate with the Amazon Elastic Compute Cloud (Amazon EC2) instance.',
                'Default': self.subnet
            },
            'ProjectName': {
                'Type': 'String',
                'Description': '[REQUIRED] The name this project.',
                'Default': self.project
            },
        }

    def create_environment(self):
        self.resources['Environment'] = {
            'Type': 'AWS::Cloud9::EnvironmentEC2',
            'Properties': {
                'AutomaticStopTimeMinutes': {
                    'Ref': 'AutomaticStopTimeMinutes'
                },
                'ConnectionType': {
                    'Ref': 'ConnectionType'
                },
                'ImageId': {
                    'Ref': 'ImageId'
                },
                'InstanceType': {
                    'Ref': 'InstanceType'
                },
                'Name': {
                    'Ref': 'Name'
                },
                'OwnerArn': {
                    'Ref': 'OwnerArn'
                },
                'SubnetId': {
                    'Ref': 'SubnetId'
                },
                'Tags': [
                    {
                        'Key': 'project',
                        'Value': {
                            'Ref': 'ProjectName'
                        }
                    }
                ]
            }
        }

    def create_outputs(self):
        self.outputs = {
            'EnvironmentId': {
                'Value': {
                    'Ref': 'Environment'
                }
            },
            'EnvironmentArn': {
                'Value': {
                    'Fn::GetAtt': 'Environment.Arn'
                }
            },
            'EnvironmentUrl': {
                'Value': {
                    'Fn::Sub': 'https://${AWS::Region}.console.aws.amazon.com/cloud9/ide/${Environment}',
                }
            }
        }

    def create_yaml(self):
        template = {
            'AWSTemplateFormatVersion': '2010-09-09',
            'Description': 'Bastion Generator CLI',
            'Parameters': self.parameters,
            'Resources': self.resources,
            'Outputs': self.outputs
        }

        try:
            with open('cloud9.yaml', 'w') as f:
                yaml.dump(template, f)

            self.template = template

        except Exception as e:
            print(e)

    def get_template_body(self):
        return self.template
