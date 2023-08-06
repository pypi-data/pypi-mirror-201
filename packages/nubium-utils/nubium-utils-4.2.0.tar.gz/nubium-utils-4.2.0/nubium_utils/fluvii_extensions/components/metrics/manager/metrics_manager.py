from fluvii.components.metrics.manager import MetricsManager
from nubium_utils.fluvii_extensions.components.metrics.pusher import NubiumMetricsPusherConfig


class NubiumMetricsManager(MetricsManager):
    pusher_config_cls = NubiumMetricsPusherConfig

    def register_custom_metric(self, name, description):
        """ Register a custom metric to be used with inc_custom_metric later. """
        self.new_metric(name, description=description)

    def inc_custom_metric(self, name, amount=1):
        """
        Increases a registered custom metric by the amount specified (defaults to 1).

        `name`'s value must be registered in advance by calling register_custom_metric.
        """
        if name not in self._metrics:
            raise ValueError(f"'{name}' was not registered via register_custom_metric.")
        self.inc_metric(name, number=amount)

    def inc_messages_consumed(self, number_of_messages, topic):
        """
        Increases the messages_consumed gauge with default labels
        """
        self.inc_metric('messages_consumed', number=number_of_messages, label_dict={'topic': topic})

    def inc_messages_produced(self, number_of_messages, topic):
        """
        Increases the messages_consumed gauge with default labels
        """
        self.inc_metric('messages_produced', number=number_of_messages, label_dict={'topic': topic})

    def inc_message_errors(self, exception):
        """
        Increases the error gauge with default label and label of the exception
        """
        self.inc_metric('message_errors', label_dict={'exception': exception.__class__.__name__})

    def inc_external_requests(self, request_to=None, request_endpoint=None, request_type=None, is_bulk=0, status_code=200):
        """
        Increases the external requests gauge.
        """
        self.inc_metric(
            'external_requests',
            label_dict={
                "request_to": request_to,
                "request_endpoint": request_endpoint,
                "request_type": request_type,
                "is_bulk": is_bulk,
                "status_code": status_code})

    def set_seconds_behind(self, seconds_behind):
        """
        Sets the seconds_behind gauge with default labels
        """
        self.set_metric('seconds_behind', seconds_behind)
