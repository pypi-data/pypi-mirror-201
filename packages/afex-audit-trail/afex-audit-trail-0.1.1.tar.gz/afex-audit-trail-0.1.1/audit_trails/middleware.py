import time
from re import sub

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken

from audit_trails.logger import Logger
from audit_trails.models import ActivityLog
from utils.encryption import DataEncryption


class ActivityLoggingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.start_time = time.time()

    def process_view(self, request, view_func, view_args, view_kwargs):
        host = request.META.get('REMOTE_HOST')
        ip_address = request.META.get('REMOTE_ADDR')
        remote_address = host if host else ip_address
        request_method = request.META.get('REQUEST_METHOD')
        request_body = str(request.body) if request_method in ('POST', 'PUT', 'PATCH',) else None
        endpoint = request.build_absolute_uri()
        if not request.user.is_anonymous:
            user = request.user
        else:
            try:
                request_token = request.META.get('HTTP_AUTHORIZATION')
                token = request_token.split()[1] if request_token else None
                token_obj = AccessToken(token)
                UserModel = get_user_model()
                user_obj = UserModel.objects.filter(
                    id=token_obj.get('user_id')
                ).first()
                user = user_obj

            except:
                user = None

            if hasattr(settings, 'LOG_STORAGE') and 'database' == settings.LOG_STORAGE.lower():
                self.activity_log = ActivityLog(
                    endpoint=endpoint,
                    request_method=request_method,
                    remote_address=remote_address,
                    request_body=request_body,
                    user=user
                )
            else:
                self.activity_log = Logger(
                    endpoint=endpoint,
                    request_method=request_method,
                    remote_address=remote_address,
                    request_body=request_body,
                    user=user
                )

    def process_response(self, request, response):
        # try:
        #     if settings.DATA_ENCRYPTION:
        #         self.activity_log.response_body = DataEncryption.decrypt(response.data)
        #     else:
        #         self.activity_log.response_body = response.data.get('data')
        #
        # except:
        #     self.activity_log.response_body = response.data
        try:
            self.activity_log.response_body = str(response.data.get('message'))
        except AttributeError:
            pass
        exec_time = f'{int((time.time() - request.start_time) * 1000)}ms'
        self.activity_log.response_code = response.status_code
        self.activity_log.exec_time = exec_time
        self.activity_log.save()
        return response

    def process_exception(self, request, exception):
        self.activity_log.error_message = str(exception.__class__.__name__)
        self.activity_log.save()

