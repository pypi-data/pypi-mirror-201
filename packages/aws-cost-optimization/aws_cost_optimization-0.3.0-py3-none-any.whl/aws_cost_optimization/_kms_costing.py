"""
Contains the methods which provides the costing details of AWS KMS service
"""

from aws_cost_optimization.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class kms:
    def cmk_cost(self, data: dict) -> dict:
        """
        :param data: recommendations data
        :return: cost details for kms cmk
        """
        logger.info(" ---Inside _kms_costing.kms :: cmk_cost")

        region = data['Metadata']['Region']
        resolved_region = self.aws_region_map[region]

        Filters = [
            {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Encryption Key'},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region}
        ]
        price = get_pricing(self.session, region, 'awskms', Filters=Filters, service_name='cmk')

        current_cost = float(price['AWS Key Management Service'])
        effective_cost = 0

        return {
            'Current Cost': current_cost,
            'Effective Cost': effective_cost,
            'Savings': current_cost - effective_cost,
            'Savings %': ((current_cost - effective_cost) / current_cost) * 100,
            'Exception': ''
        }




