class VkError(Exception):
    def __init__(self, error:dict):
        self.error_code = error['error_code']
        self.error_msg = error['error_msg']
        self.error_params = error['request_params']

    def __str__(self):
        return f"{self.error_code}. {self.error_msg}\nrequest_params: {self.error_params}"

__all__ = ('VkError')