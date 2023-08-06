from aws_recommendation.ec2 import *
from aws_recommendation.rds import *
from aws_recommendation.cost_estimations import *
from aws_recommendation.redshift import *
from aws_recommendation.ebs import *
from aws_recommendation.s3 import *
from aws_recommendation.elb import *
from aws_recommendation.cloudwatch import *
from aws_recommendation.dynamodb import *
from aws_recommendation.kms import *
from aws_recommendation.utils import *
from aws_recommendation.truted_advisor import *

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Generic Suggestions
def get_generic_suggestions(self) -> list:
    logger.info(" ---Inside get_generic_suggestions()")

    recommendations = []
    return recommendations


# Merge the recommendations and return the list
def get_recommendations(self) -> list:
    recommendations= []

    self.regions = get_regions(self.session)

    client = self.session.client('s3')
    try:
        response = client.list_buckets()
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidAccessKeyId':
            logger.info('---------S3 read access denied----------')
            temp = {
                'Service Name': 'AWS',
                'Id': 'InvalidAccessKeyId',
                'Recommendation': 'InvalidAccessKeyId',
                'Description': 'InvalidAccessKeyId',
                'Metadata': {
                    'InvalidAccessKeyId'
                },
                'Recommendation Reason': {
                    'InvalidAccessKeyId'
                },
                'Risk': 'Low',
                'Savings': None,
                'Source': 'Klera',
                'Category': 'Cost Optimization'
            }
            recommendations.append(temp)
            return recommendations

    recommendations += enable_s3_bucket_keys(self)

    recommendations += delete_or_downsize_instance_recommendation(self)
    recommendations += purge_unattached_vol_recommendation(self)
    recommendations += purge_8_weeks_older_snapshots(self)
    recommendations += reserved_instance_lease_expiration(self)
    recommendations += unassociated_elastic_ip_addresses(self)
    recommendations += unused_ami(self)

    recommendations += downsize_underutilized_rds_recommendation(self)
    recommendations += rds_idle_db_instances(self)
    recommendations += rds_general_purpose_ssd(self)

    recommendations += get_generic_suggestions(self)
    recommendations += estimated_savings(self)
    recommendations += under_utilized_redshift_cluster(self)

    recommendations += idle_ebs_volumes(self)
    recommendations += ebs_general_purpose_ssd(self)
    recommendations += gp2_to_gp3(self)
    recommendations += unused_ebs_volume(self)


    recommendations += s3_bucket_versioning_enabled(self)
    recommendations += s3_bucket_lifecycle_configuration(self)

    recommendations += idle_elastic_load_balancer(self)
    recommendations += unused_elb(self)

    recommendations += log_group_retention_period_check(self)

    recommendations += unused_dynamodb_tables(self)

    recommendations += unused_cmk(self)

    # under development
    # recommendations += get_trusted_advisor_recommendations(self)

    return recommendations