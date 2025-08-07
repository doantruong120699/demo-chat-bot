import logging
import uuid
from threading import local
import asyncio

from django.conf import settings

from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import cached_property

USER_ATTR_NAME = getattr(settings, "LOCAL_USER_ATTR_NAME", "_current_user")
REQ_UUID_ATTR_NAME = getattr(settings, "LOCAL_REQ_UUID_ATTR_NAME", "_req_uuid")
REQ_IP_ATTR_NAME = getattr(settings, "LOCAL_REQ_IP_ATTR_NAME", "_req_ip")
REQ_USER_AGENT_ATTR_NAME = getattr(
    settings, "LOCAL_REQ_USER_AGENT_ATTR_NAME", "_req_user_agent"
)


logger = logging.getLogger(__name__)

_thread_locals = local()


def _do_set_current_user(user_fun):
    setattr(_thread_locals, USER_ATTR_NAME, user_fun.__get__(user_fun, local))


def _do_del_current_user():
    delattr(_thread_locals, USER_ATTR_NAME)


def _do_set_req_uuid(request_uuid):
    setattr(_thread_locals, REQ_UUID_ATTR_NAME, request_uuid)


def _do_set_req_ip(request_ip):
    setattr(_thread_locals, REQ_IP_ATTR_NAME, request_ip)


def _do_del_req_uuid():
    req_uuid = getattr(_thread_locals, REQ_UUID_ATTR_NAME, None)

    if req_uuid is not None:
        delattr(_thread_locals, REQ_UUID_ATTR_NAME)


def _do_del_req_ip():
    req_ip = getattr(_thread_locals, REQ_IP_ATTR_NAME, None)

    if req_ip is not None:
        delattr(_thread_locals, REQ_IP_ATTR_NAME)


def _do_set_req_user_agent(request_user_agent):
    setattr(_thread_locals, REQ_USER_AGENT_ATTR_NAME, request_user_agent)


def _do_del_req_user_agent():
    delattr(_thread_locals, REQ_USER_AGENT_ATTR_NAME)


def get_current_user():
    current_user = getattr(_thread_locals, USER_ATTR_NAME, None)
    if callable(current_user):
        return current_user()
    return current_user


def get_req_uuid():
    req_uuid = getattr(_thread_locals, REQ_UUID_ATTR_NAME, None)
    return req_uuid


def get_request_ip():
    req_ip = getattr(_thread_locals, REQ_IP_ATTR_NAME, None)
    return req_ip


def get_req_user_agent():
    req_user_agent = getattr(_thread_locals, REQ_USER_AGENT_ATTR_NAME, None)
    return req_user_agent


class CorrelationMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__(get_response)

    @classmethod
    def get_model_class(cls):
        from django.contrib.sessions.models import Session

        return Session

    @cached_property
    def model(self):
        return self.get_model_class()

    @classmethod
    def get_user_model_class(cls):
        from django.contrib.auth import get_user_model

        return get_user_model()

    @cached_property
    def user_model(self):
        return self.get_user_model_class()

    def _get_admin(self, request):
        session_key = request.session.session_key
        if session_key:
            session = self.model.objects.get(session_key=session_key)
            uid = session.get_decoded().get("_auth_user_id")
            user = self.user_model.objects.get(pk=uid)
            return user
        return None

    def __get_client_info_from_request(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        user_agent = request.META.get("HTTP_USER_AGENT", "")

        return ip, user_agent

    def process_request(self, request):
        req_uuid = uuid.uuid4()
        req_ip, req_user_agent = self.__get_client_info_from_request(request)
        _do_set_req_uuid(req_uuid)
        _do_set_req_ip(req_ip)
        _do_set_req_user_agent(req_user_agent)
        logger.info(f'START "{request.path} {request.method}"')
        _do_set_current_user(lambda self: getattr(request, "user", None))

    def process_response(self, request, response):
        current_user = request.user
        logger.info(
            f'END "{request.path} {response.status_code}" user_logged={current_user}'
        )
        _do_del_current_user()
        _do_del_req_uuid()
        _do_del_req_ip()
        _do_del_req_user_agent()
        return response


class RequestUuidFilter(logging.Filter):
    def filter(self, record):
        req_uuid = getattr(_thread_locals, REQ_UUID_ATTR_NAME, "")
        record.req_uuid = req_uuid
        return True


class RequestIPFilter(logging.Filter):
    def filter(self, record):
        req_ip = getattr(_thread_locals, REQ_IP_ATTR_NAME, "")
        record.req_ip = req_ip
        return True
