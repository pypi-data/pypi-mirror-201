import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_regions(session):
    """
    :session: aws session object
    :return: list of regions
    """
    logger.info(" ---Inside utils :: get_regions()--- ")
    client = session.client('ec2', region_name='us-east-1')
    region_response = client.describe_regions()

    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions


def list_volumes(session, regions: list) -> dict:
    """
    :param regions:
    :param session:
    :return:
    """
    logger.info(" ---Inside utils :: list_gp2_volumes()--- ")

    volume_list = {}

    for region in regions:
        client = session.client('ec2', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_volumes()
            else:
                response = client.describe_volumes(
                    NextToken=marker
                )
            volume_list.setdefault(region, []).extend(response['Volumes'])

            try:
                marker = response['NextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return volume_list


# returns the pricing of resource
def get_pricing(session, region: str, service_code: str, Filters: list, service_name: str) -> dict:
    """
    :param service_name:
    :param Filters:
    :param service_code:
    :param region: aws region
    :param session: aws session
    :return: pricing
    """
    logger.info(" ---Inside utils :: get_pricing()--- ")

    aws_pricing_region = region

    client = session.client('pricing', 'us-east-1')

    response = client.get_products(
        ServiceCode=service_code,
        Filters=Filters
    )
    print(response)
    prices = {}
    for price in response['PriceList']:
        price = json.loads(price)
        # print(json.dumps(price, indent=4))
        for key in price['terms']['OnDemand'].keys():
            for k in price['terms']['OnDemand'][key]['priceDimensions'].keys():
                temp = price['terms']['OnDemand'][key]['priceDimensions'][k]['pricePerUnit']['USD']

                if service_name == 'volume':
                    prices[price['product']['attributes']['volumeApiName']] = temp
                elif service_name == 'rds' or service_name == 'ec2_instance':
                    prices[price['product']['attributes']['instanceType']] = temp
                elif service_name == 'eip':
                    if price['terms']['OnDemand'][key]['priceDimensions'][k]['endRange'] == 'Inf':
                        prices[price['product']['attributes']['usagetype']] = temp
                elif service_name == 'snapshot':
                    prices[price['product']['attributes']['usagetype']] = temp
                elif service_name == 'rds_storage':
                    prices[price['product']['attributes']['volumeName']] = temp
                elif service_name == 'cmk':
                    prices[price['product']['attributes']['servicename']] = temp
                elif service_name == 'cwlog':
                    prices[price['product']['attributes']['servicename']] = temp
                elif service_name == 'elb':
                    prices[price['product']['attributes']['groupDescription']] = temp

    return prices


# returns the list of rds instances
def list_rds_instances(session, regions: list) -> dict:
    """
    :param regions:
    :param session:
    :return:
    """
    logger.info(" ---Inside utils :: list_rds_instances()--- ")
    rds_instance_lst = {}

    for region in regions:
        client = session.client('rds', region_name=region)

        marker = ''
        while True:
            response = client.describe_db_instances(
                MaxRecords=100,
                Marker=marker
            )
            rds_instance_lst.setdefault(region, []).extend(response['DBInstances'])

            try:
                marker = response['Marker']
                if marker == '':
                    break
            except KeyError:
                break
    return rds_instance_lst


# returns the list of ec2 instances
def list_ec2_instances(session, regions: list) -> dict:
    """
    :param session:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_ec2_instances()--- ")

    instances = {}
    print('Instances')
    for region in regions:
        client = session.client('ec2', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_instances()
            else:
                response = client.describe_instances(
                    NextToken=marker
                )
            instances.setdefault(region, []).extend(response['Reservations'])
            print(response)

            try:
                marker = response['NextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return instances


# returns the list eip
def list_eip(session, regions: list) -> dict:
    """
    :param session:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_eip()--- ")

    eip_list = {}

    for region in regions:
        client = session.client('ec2', region_name=region)
        response = client.describe_addresses()
        eip_list.setdefault(region, []).extend(response['Addresses'])

    return eip_list
