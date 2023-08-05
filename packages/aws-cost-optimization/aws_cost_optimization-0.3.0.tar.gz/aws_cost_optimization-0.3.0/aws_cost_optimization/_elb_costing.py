import logging
from aws_cost_optimization.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class elb:
    def elb_costing(self, data: dict) -> dict:
        """
        :param data:
        :return:
        """
        logger.info(" ---Inside _elb_costing :: elb :: elb_costing()--- ")

        region = data['Metadata']['Region']

        resolved_region = self.aws_region_map[region]

        # client = self.session.client('elbv2', region_name=region)
        # response = client.describe_load_balancers(
        #     Names=[data['Id']]
        # )

        filters = lambda elb_type: [
            {
                'Type': 'TERM_MATCH',
                'Field': 'productFamily',
                'Value': elb_type
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'location',
                'Value': resolved_region
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'locationType',
                'Value': 'AWS Region'
            }
        ]
        elbtype = data['Metadata']['Type']
        if elbtype == 'application':
            filter_elb_type = filters('Load Balancer-Application')
        elif elbtype == filters('network'):
            filter_elb_type = 'Load Balancer-Network'
        elif elbtype == 'gateway':
            filter_elb_type = filters('Load Balancer-Gateway')
        else:
            return {
                'Current Cost': 0,
                'Effective Cost': 0,
                'Savings': 0,
                'Savings %': 0
            }

        price = get_pricing(self.session, region, 'AWSELB', filter_elb_type, service_name='elb')
        current_cost = (float(price['Used Application Load Balancer capacity units-hr']) +
                        float(price['LoadBalancer hourly usage by Application Load Balancer'])) * 24 * 30
        print(price)
        effective_cost = 0
        try:
            savings_p = ((current_cost - effective_cost) / current_cost) * 100
        except ZeroDivisionError:
            savings_p = 0

        return {
            'Current Cost': current_cost,
            'Effective Cost': effective_cost,
            'Savings': current_cost - effective_cost,
            'Savings %': savings_p,
            'Exception': ''
        }
