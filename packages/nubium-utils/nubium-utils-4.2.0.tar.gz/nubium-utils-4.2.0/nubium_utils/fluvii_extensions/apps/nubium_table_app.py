from nubium_utils.fluvii_extensions.apps.transactions.transaction import NubiumTableTransaction
from .nubium_app import NubiumAppFactory, NubiumApp
from fluvii.apps.fluvii_table_app import FluviiTableApp, FluviiTableAppFactory


class NubiumTableApp(NubiumApp, FluviiTableApp):
    def __init__(self, *args, transaction_cls=NubiumTableTransaction, **kwargs):
        super().__init__(*args, transaction_cls=transaction_cls, **kwargs)


class NubiumTableAppFactory(NubiumAppFactory, FluviiTableAppFactory):
    fluvii_app_cls = NubiumTableApp
