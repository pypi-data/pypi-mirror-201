from nubium_utils.general_utils import write_kubernetes_healthcheck_file, del_kubernetes_healthcheck_file
from fluvii.apps.fluvii_app import FluviiApp, FluviiAppFactory
from .config import NubiumAppConfig
from nubium_utils.fluvii_extensions.apps.transactions.transaction import NubiumTransaction
from nubium_utils.fluvii_extensions.components.metrics import NubiumMetricsManager, NubiumMetricsManagerConfig


class NubiumApp(FluviiApp):
    def __init__(self, *args, transaction_cls=NubiumTransaction, **kwargs):
        super().__init__(*args, transaction_cls=transaction_cls, **kwargs)

    def run(self):
        write_kubernetes_healthcheck_file()
        super().run()
        del_kubernetes_healthcheck_file()


class NubiumAppFactory(FluviiAppFactory):
    fluvii_app_cls = NubiumApp
    fluvii_app_config_cls = NubiumAppConfig
    metrics_cls = NubiumMetricsManager
    metrics_config_cls = NubiumMetricsManagerConfig
