import requests
import re
from datetime import datetime
import logging
from umedsmsclient.exceptions import InvalidCredentialsException, SmsFailedException, FireTextException


class FireTextApiClient:
    """
    This class is a wrapper for FireText API.
    """

    def __init__(self, api_key=None, username=None, password=None):
        """
        This method initializes the FireTextApiClient class object.

        :param api_key: str, Api Key of FireText account.
        :param username: str, Username of FireText account.
        :param password: str, Password of FireText account.

        :raises InvalidCredentialsException: if either `api_key` or `username` and `password` are not provided.
        """

        if not api_key and (not username or not password):
            raise InvalidCredentialsException("At least 'api key' or 'username' and 'password' must be provided.")

        self.api_key = api_key
        self.username = username
        self.password = password
        self.base_url = "https://www.firetext.co.uk/api"
        self.logger = self.__create_logger()

    def send_sms(self, sender: str, receiver: str, message: str, scheduled_time: str = None):
        """
        This method sends a sms via FireText SMS API.

        :param sender: str, Sender ID or name. Should be alphanumeric and of length 3 to 11.
        :param receiver: str, Recipient phone number. Should be in UK format starting with '07' or '447'.
        :param message: str, Text message to be sent.
        :param scheduled_time: str, (Optional) Scheduled time for the SMS in 'YYYY-MM-DD HH:MM' format.

        :raises SmsFailedException: if SMS sending fails.
        :raises FireTextException: if Timeout exception or HTTPError exception occurs while calling the API.

        :return: None
        """

        # Validate input parameters : sender, receiver, message and scheduled_time
        self.__validate_input_params(sender, receiver, message, scheduled_time)

        try:
            # Set the url parameters
            url_params = self.__set_url_params(sender, receiver, message, scheduled_time)

            # Set headers
            headers = {"Content-Type": "application/json"}

            # Construct Send Sms Url for Fire Text API
            url = f"{self.base_url}/sendsms/json"

            # Send sms request
            response = requests.post(url, params=url_params, headers=headers, verify=True, timeout=30)

            # Raises Http Error if the response doesn't indicate success
            response.raise_for_status()

            data = response.json()
            if data.get("code") != 0:
                # log the error msg
                self.logger.error(
                    self.__sms_failed_error(data.get("description"), sender, receiver, message, scheduled_time))
                raise SmsFailedException(data.get("description"), sender, receiver, message, scheduled_time)

        except SmsFailedException:
            raise
        except requests.exceptions.Timeout as e:
            # log the exception
            error_msg = "Time out exception from Fire Text API"
            self.logger.error(f"{error_msg}. exception : {e}")
            raise FireTextException(error_msg, exception=e)

        except requests.exceptions.HTTPError as e:
            # log the exception
            error_msg = "Unsuccessful response received from Fire Text API"
            self.logger.error(f"{error_msg}. status code : {e.response.status_code}, exception : {e}")
            raise FireTextException(error_msg, e.response.status_code, e)

        except Exception as e:
            # log the exception
            error_msg = f"An unknown error occurred. exception : {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

    def __validate_input_params(self, sender: str, receiver: str, message: str, scheduled_time: str):

        # Validate all required input parameters
        self.__validate_sender(sender)
        self.__validate_receiver(receiver)
        self.__validate_message(message)

        # Validate optional input parameters scheduled_time
        self.__validate_scheduled_time(scheduled_time)

    @staticmethod
    def __validate_sender(sender: str):
        if not sender:
            raise ValueError("Please provide a valid value for 'sender' parameter. "
                             "The value should not be null or empty.")
        elif not re.match("^[a-zA-Z0-9]{3,11}$", sender):
            raise ValueError("Please provide a valid value for 'sender' parameter. "
                             "The value should only contain alpha numeric characters and "
                             "have a length between 3 to 11 characters.")

    @staticmethod
    def __validate_receiver(receiver: str):
        if not receiver:
            raise ValueError("Please provide a valid value for 'receiver' parameter. "
                             "The value should not be null or empty.")
        elif not re.match(r"^(07|447)[0-9]{9}$", receiver):
            raise ValueError("Please provide a valid value for 'receiver' parameter. "
                             "The value should be a valid UK number starts with '07' or '447'.")

    @staticmethod
    def __validate_message(message: str):
        if not message:
            raise ValueError("Please provide a valid value for 'message' parameter. "
                             "The value should not be null or empty.")
        try:
            message.encode('utf-8')
        except UnicodeEncodeError:
            raise ValueError("Please provide a valid value for 'message' parameter. "
                             "The value should be in utf-8.")

    @staticmethod
    def __validate_scheduled_time(scheduled_time: str):
        if scheduled_time is not None and scheduled_time.strip() != "":
            try:
                datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M')
            except ValueError:
                raise ValueError("Please provide a valid value for 'scheduled_time' parameter. "
                                 "The value should be in the format 'YYYY-MM-DD HH:MM'.")

    def __set_url_params(self, sender: str, receiver: str, message: str, scheduled_time: str = None):
        params = dict()

        # Set authentication parameters
        if self.api_key is not None:
            params['api_key'] = self.api_key
        else:
            params['username'] = self.username
            params['password'] = self.password

        # Set other required parameters
        params['from'] = sender
        params['to'] = receiver
        params['message'] = message

        # Set a scheduled time for a scheduled sms message
        if scheduled_time is not None:
            params['schedule'] = scheduled_time

        return params

    @staticmethod
    def __sms_failed_error(reason: str, sender: str, receiver: str, message: str, scheduled_time: str):
        return f"Failed to send the sms. reason : {reason}, sender : {sender}, receiver : {receiver}, " \
               f"message : {message}, scheduled_time : {scheduled_time}"

    @staticmethod
    def __create_logger(logger_name: str = None):
        if logger_name is None:
            logger_name = "umed_sms_client_logger"
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger
