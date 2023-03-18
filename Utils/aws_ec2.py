import boto3
import logging


class AwsEc2Instance:

    def __init__(self):
        self.instanceIds = ['i-07f97a9a9713ea883']
        self.ec2 = boto3.client('ec2', region_name='eu-west-2')
        self.id = 0

    def start_aws_ec2_instance(self):
        self.id = self.ec2.start_instances(InstanceIds=self.instanceIds)
        print('started your instances: ' + str(self.instanceIds))

    def stop_aws_ec2_instance(self):
        # my_id = boto.utils.get_instance_metadata()['instance-id']
        self.ec2.stop_instances(InstanceIds=self.instanceIds)
        logging.info(' stopping EC2 :' + str(self.instanceIds))
