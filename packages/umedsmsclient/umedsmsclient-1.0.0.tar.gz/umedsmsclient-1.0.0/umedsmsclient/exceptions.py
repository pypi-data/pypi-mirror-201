class BaseSmsClientException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidCredentialsException(BaseSmsClientException):
    def __init__(self, message: str):
        super().__init__(message)


class SmsFailedException(BaseSmsClientException):
    def __init__(self, reason: str, sender: str, receiver: str, sms_body: str, scheduled_time: str):
        message = "Failed to send the sms."
        super().__init__(message)
        self.message = message
        self.reason = reason
        self.sender = sender
        self.receiver = receiver
        self.sms_body = sms_body
        self.scheduled_time = scheduled_time


class FireTextException(BaseSmsClientException):
    def __init__(self, message: str, status_code: int = None, exception: Exception = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.exception = exception
