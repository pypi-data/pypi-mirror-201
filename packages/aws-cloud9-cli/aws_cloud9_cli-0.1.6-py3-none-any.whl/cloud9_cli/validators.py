import re
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

INSTANCE_LIST = [
    't2.micro',
    't3.small',
    'm5.large',
    't3.nano',
    't2.nano',
    't3.micro',
    't2.small',
    't3.medium',
    't2.medium',
    't3.large',
    'c5.large',
    't2.large',
    'm4.large',
    'c4.large',
    't3.xlarge',
    'm5.xlarge',
    'c5.xlarge',
    't2.xlarge',
    'm4.xlarge',
    'c4.xlarge',
    't3.2xlarge',
    'm5.2xlarge',
    'c5.2xlarge',
    't2.2xlarge',
    'm4.2xlarge',
    'c4.2xlarge',
    'trn1.2xlarge',
    'm5.4xlarge',
    'c5.4xlarge',
    'm4.4xlarge',
    'c4.4xlarge',
    'm5.8xlarge',
    'c4.8xlarge',
    'c5.9xlarge',
    'm4.10xlarge',
    'm5.12xlarge',
    'c5.12xlarge',
    'm5.16xlarge',
    'm4.16xlarge',
    'c5.18xlarge',
    'm5.24xlarge',
    'm5.metal',
    'c5.24xlarge',
    'c5.metal',
    'trn1.32xlarge'
]


def name_validator(text):
    return len(text) > 0


def instance_type_validator(text):
    return text in INSTANCE_LIST


def owner_arn_validator(text):
    return re.match(
        pattern=r'^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):(iam|sts)::\d+:(root|(user\/[\w+=/:,.@-]{1,64}|federated-user\/[\w+=/:,.@-]{2,32}|assumed-role\/[\w+=:,.@-]{1,64}\/[\w+=,.@-]{1,64}))$',
        string=text)


def stack_name_validator(text, region):
    if not re.match(pattern=r'^[a-zA-Z][-a-zA-Z0-9]*$', string=text):
        return False

    else:
        try:
            boto3.client('cloudformation', config=Config(region_name=region)).describe_stacks(StackName=text)

        except ClientError:  # stack doest
            return True

        except Exception as e:
            print(e)

            return False
