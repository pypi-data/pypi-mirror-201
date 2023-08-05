import logging
from aws_cost_optimization.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class cw:
    def logs_costing(self, data) -> dict:
        """
        :return: cost details for logs costing
        """
        logger.info(" ---Inside _cloudwatch_costing :: cw :: logs_costing--- ")

        region = data['Metadata']['Region']

        resolved_region = self.aws_region_map[region]

        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Storage Snapshot'},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region}
        ]
        price = get_pricing(self.session, region, 'AmazonCloudWatch', Filters=filters, service_name='cwlog')

        stored_bytes = data['Metadata']['storedBytes']

        stored_gb = int(stored_bytes)/(1024**3)

        # cost_gb = stored_gb - 5
        cost_gb = stored_gb
        current_cost = float(price['AmazonCloudWatch']) * cost_gb
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

