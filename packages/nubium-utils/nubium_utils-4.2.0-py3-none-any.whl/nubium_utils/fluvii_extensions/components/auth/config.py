from fluvii.components.auth.config import AuthKafkaConfig
from typing import Optional


class NubiumAuthKafkaConfig(AuthKafkaConfig):
    oauth_url: Optional[str] = 'https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token'
    oauth_scope: Optional[str] = 'api.iam.service_accounts'
