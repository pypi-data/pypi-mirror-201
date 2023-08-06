import logging

AUTH_ENDPOINT = "/api-token-auth/"
TEAM_ENDPOINT = "/account/teams/"
VALIDATE_CONSUMER_SUBMISSION_ENDPOINT = "/orcabase/consumer/submissions/validate/"
SUBMIT_CONSUMER_SUBMISSION_ENDPOINT = "/orcabase/consumer/submissions/submit/"
VALIDATE_SERVICEOWNER_SUBMISSION_ENDPOINT = "/orcabase/serviceowner/services/validate/"
SUBMIT_SERVICEOWNER_SUBMISSION_ENDPOINT = "/orcabase/serviceowner/services/"
SUBMIT_SERVICEOWNER_SUBMISSION_DOCS_ENDPOINT = "/orcabase/serviceowner/services/$uuid/docs/"
SERVICE_ITEMS_ENDPOINT = "/orcabase/serviceowner/service_items/"
CHANGE_INSTANCES_ENDPOINT = "/orcabase/serviceowner/change_instances/"
DEPLOYED_ITEMS_ENDPOINT = "/orcabase/serviceowner/deployed_items/"
SERVICE_CONFIG_ENDPOINT = "/orcabase/serviceowner/service_configs/"

RETRY_TIMES = 1  # number of times request will be retried

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
LOG_LEVEL = logging.INFO

logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger("netorca_sdk")
