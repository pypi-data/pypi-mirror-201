from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_certificatemanager as certificatemanager
from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route53_targets
from constructs import Construct

from .branch_config import BranchConfig


class WebappLambda(Construct):
    """Assumes a local folder called "webapp-backend" with a Dockerfile in it."""

    def __init__(
        self,
        scope: "Construct",
        _id: str,
        branch_config: BranchConfig,
        lambda_runtime_environment=None,
    ):
        super().__init__(scope, _id)
        if lambda_runtime_environment is None:
            lambda_runtime_environment = {}

        self.webapp_lambda_func = _lambda.DockerImageFunction(
            scope,
            "FlaskLambda",
            code=_lambda.DockerImageCode.from_image_asset(directory="webapp-backend"),
            environment=lambda_runtime_environment,
        )

        cloudwatch.Alarm(
            scope,
            "FlaskLambdaThrottles",
            metric=self.webapp_lambda_func.metric_throttles(),
            evaluation_periods=1,
            threshold=0,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
        )

        root_hosted_zone = branch_config.get_hosted_zone(scope)
        if root_hosted_zone is not None:
            backend_domain_name = "api." + branch_config.domain_name

            backend_certificate = certificatemanager.Certificate(
                scope,
                "apiCert",
                domain_name=backend_domain_name,
                validation=certificatemanager.CertificateValidation.from_dns(
                    root_hosted_zone
                ),
            )

            # noinspection PyTypeChecker
            cors_options = apigateway.CorsOptions(
                # Code analysis is glitching here, this is the correct way to pass this param.
                allow_origins=apigateway.Cors.ALL_ORIGINS
            )

            lambda_gateway = apigateway.LambdaRestApi(
                scope,
                branch_config.construct_id("WebappBackendApi"),
                handler=self.webapp_lambda_func,
                domain_name=apigateway.DomainNameOptions(
                    domain_name=backend_domain_name, certificate=backend_certificate
                ),
                disable_execute_api_endpoint=True,
                default_cors_preflight_options=cors_options,
            )

            route53.ARecord(
                scope,
                "BackendApiARecord",
                zone=root_hosted_zone,
                target=route53.RecordTarget.from_alias(
                    route53_targets.ApiGateway(lambda_gateway)
                ),
                record_name=backend_domain_name,
            )
