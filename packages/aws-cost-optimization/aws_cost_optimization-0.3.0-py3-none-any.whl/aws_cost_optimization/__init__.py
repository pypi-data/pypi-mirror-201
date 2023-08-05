import time
import traceback

from boto3 import session
import logging

from aws_cost_optimization import _savings_plan, _ri_recommendations, _ec2_costing, _rds_costing, _kms_costing, \
    _cloudwatch_costing, _elb_costing
from aws_cost_optimization.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

__author__ = "Dheeraj Banodha"
__version__ = '0.3.0'


class aws_client(_ri_recommendations.ri, _savings_plan.sp, _ec2_costing.ec2, _rds_costing.rds, _kms_costing.kms, _cloudwatch_costing.cw, _elb_costing.elb):
    def __init__(self, **kwargs):
        if 'aws_access_key_id' in kwargs.keys() and 'aws_secret_access_key' in kwargs.keys():
            self.session = session.Session(
                aws_access_key_id=kwargs['aws_access_key_id'],
                aws_secret_access_key=kwargs['aws_secret_access_key'],
            )
        elif 'profile_name' in kwargs.keys():
            self.session = session.Session(profile_name=kwargs['profile_name'])

        self.regions = get_regions(self.session)
        self.aws_region_map = {
            'us-west-2': 'US West (Oregon)',
            'us-west-1': 'US West (N. California)',
            'us-east-2': 'US East (Ohio)',
            'us-east-1': 'US East (N. Virginia)',
            'sa-east-1': 'South America (Sao Paulo)',
            'eu-west-1': 'EU (Ireland)',
            'eu-west-3': 'EU (Paris)',
            'eu-west-2': 'EU (London)',
            'eu-central-1': 'EU (Frankfurt)',
            'eu-north-1': 'EU (Stockholm)',
            'ca-central-1': 'Canada (Central)',
            'ap-south-1': 'Asia Pacific (Mumbai)',
            'ap-southeast-2': 'Asia Pacific (Sydney)',
            'ap-southeast-1': 'Asia Pacific (Singapore)',
            'ap-northeast-3': 'Asia Pacific (Osaka)',
            'ap-northeast-2': 'Asia Pacific (Seoul)',
            'ap-northeast-1': 'Asia Pacific (Tokyo)',
            'me-south-1': 'Middle East (Bahrain)',
            'me-central-1': 'Middle East (UAE)',
            'eu-south-2': 'Europe (Spain)',
            'eu-south-1': 'Europe (Milan)',
            'eu-central-2': 'Europe (Zurich)',
            'ap-southeast-4': 'Asia Pacific (Melbourne)',
            'ap-southeast-3': 'Asia Pacific (Jakarta)',
            'ap-south-2': 'Asia Pacific (Hyderabad)',
            'ap-east-1': 'Asia Pacific (Hong Kong)',
            'af-south-1': 'Africa (Cape Town)',
            'us-gov-west-1': 'AWS GovCloud (US)',
        }

    # returns the cost details of recommendations
    def cost_details(self, data: dict) -> dict:
        """
        :param data:
        :return:
        """
        available_cost_details = {
            'Delete idle EBS volume': self.unused_ebs_costing,
            'Associate the EIP with a running active instance, or release the unassociated EIP': self.unallocated_eip,
            'Migrate GP2 volume to GP3': self.gp2_to_gp3,
            'Remove unused EBS volume': self.unused_ebs_costing,
            'Purge unattached volume': self.unused_ebs_costing,
            'Purge 8 week older snapshot': self.older_snapshot_costing,
            # 'Remove AMI': None,
            # 'Remove Unused ELB': None,
            'Remove Customer Master Key': self.cmk_cost,
            'Delete idle rds instance': self.delete_rds_costing,
            'Upgrade to General Purpose SSD': self.rds_gp_ssd,
            # 'Delete idle compute instance': self.remove_ec2_costing,
            'Add retention period in log group': self.logs_costing,
            'Upgrade Storage Type': self.upgrade_ebs_costing,
            'Terminate Elastic Load Balancer': self.elb_costing
        }
        if data['Recommendation'] in available_cost_details.keys():
            try:
                logger.info(data)
                response = available_cost_details[data['Recommendation']](data)
            except Exception as e:
                logger.info('-------------Exception-------------')
                logger.info(e)
                response = {
                    'Current Cost': 0,
                    'Effective Cost': 0,
                    'Savings': 0,
                    'Savings %': 0,
                    'Exception': str(traceback.format_exc())
                }
        else:
            logger.info('cost details not included in '+data['Recommendation'])
            response = {
                'Current Cost': 0,
                'Effective Cost': 0,
                'Savings': 0,
                'Savings %': 0,
                'Exception': 'Not included'
            }

        return response
