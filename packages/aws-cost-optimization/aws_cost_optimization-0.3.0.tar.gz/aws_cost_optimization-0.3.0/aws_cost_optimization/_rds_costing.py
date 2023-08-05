import logging
from aws_cost_optimization.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class rds:
    def rds_upgrades(self) -> list:
        """
        :return: list of cost saving recommendations
        """
        logger.info(" ---Inside aws_client :: rds_upgrades()--- ")

        recommendations = []

        rds_instances = list_rds_instances(self.session, self.regions)

        for region, rds_list in rds_instances.items():
            resolved_region = self.aws_region_map[region]
            for instance in rds_list:
                instance_type = instance['DBInstanceClass']
                instance_family = instance_type.split('.')[1]

                Filters = [
                    {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
                    {'Type': 'TERM_MATCH', 'Field': 'databaseEngine', 'Value': instance['Engine']},
                    {'Type': 'TERM_MATCH', 'Field': 'deploymentOption',
                     'Value': 'Single-AZ' if instance['MultiAZ'] else 'Multi-AZ'},
                    {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Database Instance'},
                    {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region}
                ]

                def evaluate(frm: str, to: str):
                    price_from = get_pricing(
                        self.session, region, 'AmazonRDS',
                        Filters,
                        service_name='instanceType'
                    )
                    print(price_from)
                    Filters[0]['Value'] = instance_type.replace(frm, to)
                    price_to = get_pricing(
                        self.session, region, 'AmazonRDS', Filters,
                        service_name='rds'
                    )
                    print(price_to)
                    current_cost = float(price_from[instance_type]) * 730
                    effective_cost = float(price_to[instance_type.replace(frm, to)]) * 730

                    recommendation = {
                        'Region': region,
                        'Instance Id': instance['DBInstanceIdentifier'],
                        'Instance Type': instance_type,
                        'Upgrade To': instance_type.replace(frm, to),
                        'Current Cost': current_cost,
                        'Effective Cost': effective_cost,
                        'Savings': current_cost - effective_cost,
                        'Savings %': ((current_cost - effective_cost) / current_cost) * 100
                    }
                    return recommendation

                match instance_family:
                    case 'm3':
                        recommendations.append(evaluate('m3', 'm5'))
                    case 'r3':
                        recommendations.append(evaluate('r3', 'r5'))
                    case 'm1':
                        recommendations.append(evaluate('m1', 't2'))

        return recommendations

    def delete_rds_costing(self, data: dict) -> dict:
        """
        :param data:
        :return:
        """
        logger.info(" ---Inside aws_client :: rds_costing()--- ")

        region = data['Metadata']['Region']

        resolved_region = self.aws_region_map[region]
        filters = [
            {
                'Type': 'TERM_MATCH',
                'Field': 'productFamily',
                'Value': 'Database Instance'
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'location',
                'Value': resolved_region
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'instanceType',
                'Value': data['Metadata']['DBInstanceClass']
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'databaseEngine',
                'Value': data['Metadata']['Engine']
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'deploymentOption',
                'Value': 'Multi-AZ' if data['Metadata']['MultiAZ'] else 'Single-AZ'
            }
        ]
        price = get_pricing(self.session, data['Metadata']['Region'], 'AmazonRDS', filters, service_name='rds')
        # print(price)

        current_cost = float(price[data['Metadata']['DBInstanceClass']]) * 730
        effective_cost = 0
        recommendation = {
            'Current Cost': current_cost,
            'Effective Cost': effective_cost,
            'Savings': current_cost - effective_cost,
            'Savings %': ((current_cost - effective_cost) / current_cost) * 100,
            'Exception': ''
        }
        return recommendation

    # returns the costing details of  rds general purpose ssd
    def rds_gp_ssd(self, data: dict) -> dict:
        """
        :param data:
        :return:
        """
        logger.info(" ---Inside aws_client :: rds_gp_ssd()--- ")

        region = data['Metadata']['Region']

        resolved_region = self.aws_region_map[region]

        filters = lambda family, vtype: [
            {
                'Type': 'TERM_MATCH',
                'Field': 'productFamily',
                'Value': family
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'location',
                'Value': resolved_region
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'volumeType',
                'Value': vtype
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'databaseEdition',
                'Value': 'Standard'
            }
        ]

        price_instance = get_pricing(self.session, region, 'AmazonRDS', filters('Database Storage', 'Provisioned IOPS (SSD)'), service_name='rds_storage')
        price_iops = get_pricing(self.session, region, 'AmazonRDS', filters('Provisioned IOPS', 'Provisioned IOPS (SSD)'), service_name='rds_storage')
        current_cost = float(price_instance['io1']) + float(price_iops['io1'])
        # print(current_cost)

        gp2_price = get_pricing(self.session, region, 'AmazonRDS', filters('Database Storage', 'General Purpose (SSD)'), service_name='rds_storage')

        # print(gp2_price)
        effective_cost = float(gp2_price['gp2'])

        recommendation = {
            'Current Cost': current_cost,
            'Effective Cost': effective_cost,
            'Savings': current_cost - effective_cost,
            'Savings %': ((current_cost - effective_cost) / current_cost) * 100,
            'Exception': ''
        }
        return recommendation

