"""
Returns the recommendation for purchasing the Reserved instance
"""
import logging

import pandas as pd

logger = logging.getLogger()


class ri:
    def ri_recommendations(self) -> list:
        """
        :return: list of recommendations for purchasing the savings plan
        """
        logger.info(" ---Inside _ri_recommendations:: ri :: ri_recommendations()--- ")

        client = self.session.client('ce')

        res_recommendations = []

        service_map = {
            'Amazon Elastic Compute Cloud - Compute': 'EC2InstanceDetails',
            'Amazon Relational Database Service': 'RDSInstanceDetails',
            'Amazon Redshift': 'RedshiftInstanceDetails',
            'Amazon ElastiCache': 'ElastiCacheInstanceDetails',
            'Amazon Elasticsearch Service': 'ESInstanceDetails',
            'Amazon OpenSearch Service': ''
        }
        for service in service_map:
            logger.info("Service: "+service)
            marker = ''
            while True:
                if marker == '':
                    response = client.get_reservation_purchase_recommendation(
                        Service=service,
                        LookbackPeriodInDays='SIXTY_DAYS'
                    )
                else:
                    response = client.get_reservation_purchase_recommendation(
                        Service=service,
                        LookbackPeriodInDays='SIXTY_DAYS',
                        NextPageToken=marker
                    )
                for recommendation in response['Recommendations']:
                    logger.info(len(recommendation['RecommendationDetails']))
                    for recommendation_details in recommendation['RecommendationDetails']:
                        instance_detail = recommendation_details['InstanceDetails'][service_map[service]] \
                            if not service == 'Amazon OpenSearch Service' else ''

                        temp = {
                            'AccountScope':recommendation['AccountScope'],
                            'LookbackPeriodInDays': recommendation['LookbackPeriodInDays'],
                            'TermInYears': recommendation['TermInYears'],
                            'PaymentOption': recommendation['PaymentOption'],
                            'ServiceSpecification': recommendation['ServiceSpecification'] if service == 'Amazon Elastic Compute Cloud - Compute' else '',
                            'AccountId': recommendation_details['AccountId'],
                            'Details': instance_detail,
                            'RecommendedNumberOfInstancesToPurchase': recommendation_details['RecommendedNumberOfInstancesToPurchase'],
                            'RecommendedNormalizedUnitsToPurchase': recommendation_details['RecommendedNormalizedUnitsToPurchase'],
                            'MinimumNumberOfInstancesUsedPerHour': recommendation_details['MinimumNumberOfInstancesUsedPerHour'],
                            'MinimumNormalizedUnitsUsedPerHour': recommendation_details['MinimumNormalizedUnitsUsedPerHour'],
                            'MaximumNumberOfInstancesUsedPerHour': recommendation_details['MaximumNumberOfInstancesUsedPerHour'],
                            'MaximumNormalizedUnitsUsedPerHour': recommendation_details['MaximumNormalizedUnitsUsedPerHour'],
                            'AverageNumberOfInstancesUsedPerHour': recommendation_details['AverageNumberOfInstancesUsedPerHour'],
                            'AverageNormalizedUnitsUsedPerHour': recommendation_details['AverageNormalizedUnitsUsedPerHour'],
                            'AverageUtilization': recommendation_details['AverageUtilization'],
                            'EstimatedBreakEvenInMonths': recommendation_details['EstimatedBreakEvenInMonths'],
                            'CurrencyCode': recommendation_details['CurrencyCode'],
                            'EstimatedMonthlySavingsAmount': recommendation_details['EstimatedMonthlySavingsAmount'],
                            'EstimatedMonthlySavingsPercentage': recommendation_details['EstimatedMonthlySavingsPercentage'],
                            'EstimatedMonthlyOnDemandCost': recommendation_details['EstimatedMonthlyOnDemandCost'],
                            'EstimatedReservationCostForLookbackPeriod': recommendation_details['EstimatedReservationCostForLookbackPeriod'],
                            'UpfrontCost': recommendation_details['UpfrontCost'],
                            'RecurringStandardMonthlyCost': recommendation_details['RecurringStandardMonthlyCost']
                        }
                        res_recommendations.append(temp)

                try:
                    marker = response['NextPageToken']
                    if marker is None or marker == '':
                        break
                except KeyError:
                    break

        return res_recommendations


