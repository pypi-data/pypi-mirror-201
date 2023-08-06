class NetworkError(Exception):
    """
    Generic handler for non-breaking, network-related external call failure.
    """
    def __init__(self, *args, req_status_code=None):
        self.req_status_code = 500
        if req_status_code:
            self.req_status_code = req_status_code
        if not args:
            default_message = f'Encountered a network-related external call failure, status code {self.req_status_code})'
            args = (default_message,)
        super().__init__(*args)
