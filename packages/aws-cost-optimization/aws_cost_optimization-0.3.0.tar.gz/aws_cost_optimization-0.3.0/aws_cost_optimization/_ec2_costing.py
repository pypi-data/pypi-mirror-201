import logging
from aws_cost_optimization.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class ec2:
    # returns the costing details of delete idle compute instance
    def remove_ec2_costing(self, data: dict) -> dict:
        """
        :param data:
        :return:
        """
        logger.info(" --- Inside aws_client :: remove_ec2_costing()--- ")

        region = data['Metadata']['Region']

        client = self.session.client('ec2', region)
        response = client.describe_instances(
            InstanceIds=[data['Id']]
        )
        tenancy = None
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['InstanceId'] == data['Id']:
                    tenancy = instance['Placement']['Tenancy']

        if tenancy == 'host':
            tenancy_filter = 'Host'
        elif tenancy == 'dedicated':
            tenancy_filter = 'Dedicated'
        else:
            tenancy_filter = 'NA'

        byol = False

        resolved_region = self.aws_region_map[region]
        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'termType', 'Value': 'OnDemand'},
            {'Type': 'TERM_MATCH', 'Field': 'capacitystatus',
             'Value': 'AllocatedHost' if tenancy == 'host' else 'Used'},
            {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': tenancy_filter},
            {
                'Type': 'TERM_MATCH',
                'Field': 'productFamily',
                'Value': 'Compute Instance'
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'location',
                'Value': resolved_region
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'instanceType',
                'Value': data['Metadata']['Instance Type']
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'licenseModel',
                'Value': 'Bring your own license' if byol else 'No License required'
            }
        ]
        if data['Metadata']['Platform'] is not None:
            filters.append({
                'Type': 'TERM_MATCH',
                'Field': 'operatingSystem',
                'Value': data['Metadata']['Platform']
            })
        price = get_pricing(self.session, data['Metadata']['Region'], 'AmazonEC2', filters, service_name='ec2_instance')

        print(price)

    def gp2_to_gp3(self, data: dict) -> dict:
        """
        :param data: recommendations data
        :return: cost saving recommendations
        """
        logger.info(" ---Inside aws_client :: gp2_to_gp3()--- ")

        region = data['Metadata']['Region']
        resolved_region = self.aws_region_map[region]

        Filters = [
            {'Type': 'TERM_MATCH', 'Field': 'volumeType', 'Value': 'General Purpose'},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region}
        ]
        price = get_pricing(self.session, region, 'AmazonEC2', Filters=Filters, service_name='volume')

        client = self.session.client('ec2', region_name=region)
        response = client.describe_volumes(
            VolumeIds=[
                data['Id']
            ]
        )
        size = 1
        for volume in response['Volumes']:
            if volume['VolumeId'] == data['Id']:
                size = volume['Size']

        current_cost = float(price['gp2']) * float(size)
        effective_cost = float(price['gp3']) * float(size)
        recommendation = {
            'Current Cost': current_cost,
            'Effective Cost': effective_cost,
            'Savings': current_cost - effective_cost,
            'Savings %': ((current_cost - effective_cost) / current_cost) * 100,
            'Exception': ''
        }

        return recommendation

    def unallocated_eip(self, data) -> dict:
        """
        :return: this list the potential savings
        """
        logger.info(" ---Inside aws_client :: unallocated_eip()--- ")

        region = data['Metadata']['Region']

        resolved_region = self.aws_region_map[region]

        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'IP Address'},
            # {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region},
            # {'Type': 'TERM_MATCH', 'Field': 'usagetype', 'Value': 'APS3-ElasticIP:IdleAddress'}
            {'Type': 'TERM_MATCH', 'Field': 'usagetype', 'Value': 'ElasticIP:IdleAddress'}
        ]
        price = get_pricing(self.session, region, 'AmazonEC2', filters, service_name='eip')
        current_cost = float(price['ElasticIP:IdleAddress']) * 730
        effective_cost = 0
        recommendation = {
            'Current Cost': current_cost,
            'Effective Cost': effective_cost,
            'Savings': current_cost - effective_cost,
            'Savings %': ((current_cost - effective_cost) / current_cost) * 100,
            'Exception': ''
        }

        return recommendation

    #   Provides cost details for recommendation unused_ebs
    def unused_ebs_costing(self, data: dict) -> dict:
        """
        :param data:
        :return:
        """
        logger.info(" ---Inside _ec2_costing.ec2 :: unused_ebs_costing()--- ")

        region = data['Metadata']['Region']

        if data['Metadata']['Instance Type'].startswith('gp'):
            volume_type = 'General Purpose'
        else:
            volume_type = "Provisioned IOPS"

        resolved_region = self.aws_region_map[region]
        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'volumeType', 'Value': volume_type},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region}
        ]

        price = get_pricing(self.session, data['Metadata']['Region'], 'AmazonEC2', filters, service_name='volume')

        client = self.session.client('ec2', region_name=region)
        response = client.describe_volumes(
            VolumeIds=[
                data['Id']
            ]
        )
        size = 1
        for volume in response['Volumes']:
            if volume['VolumeId'] == data['Id']:
                size = volume['Size']

        current_cost = float(price['gp2']) * float(size)
        effective_cost = 0
        recommendation = {
            'Current Cost': current_cost,
            'Effective Cost': effective_cost,
            'Savings': current_cost - effective_cost,
            'Savings %': ((current_cost - effective_cost) / current_cost) * 100,
            'Exception': ''
        }

        return recommendation

    # InComplete ******************************************
    # returns the recommendations for ec2_upgrades
    # def ec2_upgrades(self) -> list:
    #     """
    #     :return:
    #     """
    #     logger.info(" ---Inside aws_client :: rds_upgrades()--- ")
    #
    #     recommendations = []
    #
    #     ec2_instances = list_ec2_instances(self.session, self.regions)
    #
    #     for region, reservations in ec2_instances.items():
    #         resolved_region = self.aws_region_map[region]
    #         for reservation in reservations:
    #             for instance in reservation['Instances']:
    #                 instance_type = instance['InstanceType']
    #                 instance_family = instance_type.split('.')[0]
    #                 print(instance['InstanceId'])
    #                 print(instance_type)
    #
    #                 Filters = [
    #                     {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
    #                     {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region},
    #                     {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Red Hat Enterprise Linux with HA'},
    #                     {'Type': 'TERM_MATCH', 'Field': 'marketoption', 'Value': 'OnDemand'}
    #                 ]
    #                 print(get_pricing(
    #                     self.session, region, 'AmazonEC2', Filters ,
    #                         service_name = 'ec2_instance
    #                 ))
    #
    #     return recommendations

    #  Provides the cost details for delete older snapshot recommendations
    def older_snapshot_costing(self, data: dict) -> dict:
        """
        :param data: recommendations details
        :return: cost and savings information
        """
        logger.info(" ---Inside _ec2_costing.ec2 :: older_snapshot_costing()--- ")

        region = data['Metadata']['Region']
        resolved_region = self.aws_region_map[region]

        client = self.session.client('ec2', region_name=region)
        response = client.describe_snapshots(
            SnapshotIds=[data['Id']]
        )

        try:
            if response['Snapshots'][0]['StorageTier'] == 'archive':
                usage_type = 'EBS:SnapshotArchiveStorage'
            else:
                usage_type = 'EBS:SnapshotUsage'
        except KeyError:
            usage_type = 'EBS:SnapshotUsage'

        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Storage Snapshot'},
            {'Type': 'TERM_MATCH', 'Field': 'usagetype', 'Value': usage_type},
            # {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region}
        ]
        price = get_pricing(self.session, region, 'AmazonEC2', Filters=filters, service_name='snapshot')
        print(price)
        size = response['Snapshots'][0]['VolumeSize']
        current_cost = float(price['EBS:SnapshotUsage']) * float(size)
        effective_cost = 0

        recommendation = {
            'Current Cost': current_cost,
            'Effective Cost': effective_cost,
            'Savings': current_cost - effective_cost,
            'Savings %': ((current_cost - effective_cost) / current_cost) * 100,
            'Exception': ''
        }

        return recommendation

    # returns the costing details for upgrading the volume type to GP
    def upgrade_ebs_costing(self, data: dict) -> dict:
        """
        :param data: recommendation details
        :return: cost details for ebs
        """
        logger.info(" ---Inside _ec2_costing :: ec2 :: upgrading_ebs_costing()--- ")

        region = data['Metadata']['Region']
        resolved_region = self.aws_region_map[region]

        filters = lambda v_type: [
            {'Type': 'TERM_MATCH', 'Field': 'volumeType', 'Value': v_type},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region}
        ]

        price_provisioned = get_pricing(self.session, region, 'AmazonEC2', filters('Provisioned IOPS'), service_name='volume')

        # print(price_provisioned)
        current_cost = float(price_provisioned[data['Metadata']['Instance Type']]) * data['Metadata']['size']

        price_gp3 = get_pricing(self.session, region, 'AmazonEC2', filters('General Purpose'), service_name='volume')

        # print(price_gp3)
        effective_cost = float(price_gp3['gp3']) * data['Metadata']['size']
        savings = current_cost - effective_cost
        try:
            savings_p = ((current_cost - effective_cost) / current_cost) * 100
        except ZeroDivisionError:
            savings_p = 0

        recommendation = {
            'Current Cost': current_cost,
            'Effective Cost': effective_cost,
            'Savings': savings,
            'Savings %': savings_p,
            'Exception': ''
        }
        return recommendation


