from django.utils import timezone


class Logger:

    def __init__(
            self, endpoint, request_method, remote_address, exec_time=None,
            request_body=None, response_body=None, error_message=None, user=None,
            response_code=None
    ):
        self.endpoint = endpoint
        self.request_method = request_method
        self.exec_time = exec_time
        self.remote_address = remote_address
        self.request_body = request_body
        self.response_code = response_code
        self.response_body = response_body
        self.error_message = error_message
        self.user = user

    def save(self):
        with open('activity.log', 'a+') as file:
            file.write(
                f"time:{timezone.now()}, method:{self.request_method}, "
                f"remote_address:{self.remote_address}, user:{self.user}, "
                f"request_body:{self.request_body}, "
                f"request_code:{self.response_code}, "
                f"response_body:'{self.response_body}', "
            )
            if self.error_message:
                file.write(
                    f"error_message: {self.error_message}, "
                )
            file.write(
                f"exec_time:{self.exec_time}, "
                f"endpoint:{self.endpoint}\n"
            )
