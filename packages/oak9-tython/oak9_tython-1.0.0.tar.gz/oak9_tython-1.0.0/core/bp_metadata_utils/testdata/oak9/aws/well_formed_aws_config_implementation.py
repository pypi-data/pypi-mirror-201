class AwsApiGateway():

    def check_logging_aws_apigateway(apigateway, context):
        """
        Checks that methods in an Amazon API Gateway stage for deployed APIs have 'loggingLevel'
        as one of the values specified in the rule parameter 'loggingLevel'.
        The rule returns NON_COMPLIANT if any method in a stage has 'loggingLevel' set to a
        value not matching any of the logging levels specified in the rule parameter.

        Implements:
            AWS_CONFIG_POLICY: https://github.com/awslabs/aws-config-rules/blob/master/python/API_GW_EXECUTION_LOGGING_ENABLED/API_GW_EXECUTION_LOGGING_ENABLED.py
        Coverage: Full
        """
        violations = []
