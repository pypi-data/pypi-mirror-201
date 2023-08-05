"""
Provides the recommendations for purchasing the savings plan
"""
import logging
import pandas as pd

logger = logging.getLogger()


class sp:
    def sp_recommendations(self) -> list:
        """
        :return: list of savings plan recommendations
        """
        logger.info(" ---Inside _savings_plan :: sp :: sp_recommendations()--- ")

        # response recommendations list
        res_recommendations = []

        # creation of aws client for cost explorer
        client = self.session.client('ce')

        savings_plan_type = ['COMPUTE_SP', 'EC2_INSTANCE_SP', 'SAGEMAKER_SP']
        terms = ['ONE_YEAR', 'THREE_YEARS']
        payment_options = ['NO_UPFRONT', 'PARTIAL_UPFRONT', 'ALL_UPFRONT']

        lookback_period = 'SIXTY_DAYS'
        uid = 1
        for sp_type in savings_plan_type:
            logger.info('Savings Plan type: ' + sp_type)
            for term in terms:
                logger.info('term: ' + term)
                for payment_option in payment_options:
                    logger.info('PaymentOption: ' + payment_option)
                    marker = ''
                    while True:
                        if marker == '':
                            response = client.get_savings_plans_purchase_recommendation(
                                SavingsPlansType=sp_type,
                                TermInYears=term,
                                PaymentOption=payment_option,
                                LookbackPeriodInDays=lookback_period
                            )
                        else:
                            response = client.get_savings_plan_purchase_recommendation(
                                SavingsPlansType=sp_type,
                                TermInYears=term,
                                PaymentOption=payment_option,
                                LookbackPeriodInDays=lookback_period,
                                NextPageToken=marker
                            )
                        if 'SavingsPlansPurchaseRecommendationDetails' in response[
                            'SavingsPlansPurchaseRecommendation']:
                            for recommendation in response['SavingsPlansPurchaseRecommendation']['SavingsPlansPurchaseRecommendationDetails']:
                                temp = {
                                    'AccountScope': response['SavingsPlansPurchaseRecommendation']['AccountScope'],
                                    'SavingsPlansType': response['SavingsPlansPurchaseRecommendation']['SavingsPlansType'],
                                    'TermInYears': response['SavingsPlansPurchaseRecommendation']['TermInYears'],
                                    'PaymentOption': response['SavingsPlansPurchaseRecommendation']['PaymentOption'],
                                    'LookbackPeriodInDays': response['SavingsPlansPurchaseRecommendation']['LookbackPeriodInDays'],
                                    'SavingsPlansDetails': recommendation['SavingsPlansDetails'],
                                    'AccountId': recommendation['AccountId'],
                                    'UpfrontCost': recommendation['UpfrontCost'],
                                    'EstimatedROI': recommendation['EstimatedROI'],
                                    'CurrencyCode': recommendation['CurrencyCode'],
                                    'EstimatedSPCost': recommendation['EstimatedSPCost'],
                                    'EstimatedOnDemandCost': recommendation['EstimatedOnDemandCost'],
                                    'EstimatedOnDemandCostWithCurrentCommitment': recommendation['EstimatedOnDemandCostWithCurrentCommitment'],
                                    'EstimatedSavingsAmount': recommendation['EstimatedSavingsAmount'],
                                    'EstimatedSavingsPercentage': recommendation['EstimatedSavingsPercentage'],
                                    'HourlyCommitmentToPurchase': recommendation['HourlyCommitmentToPurchase'],
                                    'EstimatedAverageUtilization': recommendation['EstimatedAverageUtilization'],
                                    'EstimatedMonthlySavingsAmount': recommendation['EstimatedMonthlySavingsAmount'],
                                    'CurrentMinimumHourlyOnDemandSpend': recommendation['CurrentMinimumHourlyOnDemandSpend'],
                                    'CurrentMaximumHourlyOnDemandSpend': recommendation['CurrentMaximumHourlyOnDemandSpend'],
                                    'CurrentAverageHourlyOnDemandSpend': recommendation['CurrentAverageHourlyOnDemandSpend']
                                }
                                res_recommendations.append(temp)

                        try:
                            marker = response['NextPageToken']
                            if marker == '' or marker is None:
                                break
                        except KeyError:
                            break

        return res_recommendations
