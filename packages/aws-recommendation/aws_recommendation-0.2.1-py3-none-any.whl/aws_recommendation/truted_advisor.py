import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Generates recommendation from trusted advisor
def get_trusted_advisor_recommendations(self) -> list:
    """
    :param self:
    :return: list of
    """
    logger.info(" ---Inside get_trusted_advisor_recommendations")

    recommendation = []
    client = self.session.client('support')
    try:
        response = client.describe_trusted_advisor_checks(
            language='en'
        )
        for check in response['checks']:
            check_description = client.describe_trusted_advisor_check_result(
                checkId=check['id'],
                language='en'
            )
            print(check_description)

    except ClientError as e:
        logger.info('Exception caught: ' + (e.response['Error']['Code']))
        if e.response['Error']['Code'] == 'SubscriptionRequiredException':
            return [{
                    'Service Name': 'CloudWatch',
                    'Id': 'Subscription Required',
                    'Recommendation': 'Access Denied',
                    'Description': 'Amazon Web Services Premium Support Subscription is required to use this service.',
                    'Metadata': {},
                    'Recommendation Reason': {},
                    'Risk': 'Medium',
                    'Savings': None,
                    'Source': 'AWS',
                    'Category': ''
                }]

    return recommendation