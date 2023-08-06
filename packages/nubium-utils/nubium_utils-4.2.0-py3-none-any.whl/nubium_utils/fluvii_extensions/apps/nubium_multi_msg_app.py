from .nubium_app import NubiumAppFactory, NubiumApp
from fluvii.apps.fluvii_multi_msg_app import FluviiMultiMessageApp, FluviiMultiMessageAppFactory


class NubiumMultiMessageApp(NubiumApp, FluviiMultiMessageApp):
    pass


class NubiumMultiMessageAppFactory(NubiumAppFactory, FluviiMultiMessageAppFactory):
    fluvii_app_cls = NubiumMultiMessageApp
