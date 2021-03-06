from json import JSONDecodeError

from django.utils.deprecation import MiddlewareMixin
from django.http.response import HttpResponse
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from main.one import RestJsonResponse
import json


class AuthMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        if 'application/json' in request.META['CONTENT_TYPE']:
            try:
                request.info = json.loads(request.body)
            except JSONDecodeError:
                return HttpResponse(status=400)
        
        ignore_paths = ['/login', '/create_admin', '/register', '/prometheus/metrics']
        if request.path in ignore_paths:
            return
        if not request.user.is_authenticated:
            return JsonResponse(status=403, data={
                'code': 403,
                'msg': 'auth failure',
                'data': None,
            })

    @staticmethod
    def process_response(request, response):
        return response

    @staticmethod
    def process_exception(request, exception):
        return
        if isinstance(exception, ObjectDoesNotExist):
            pass
            # return RestJsonResponse(msg='not found', code='404')
        elif isinstance(exception, KeyError):
            return RestJsonResponse(msg='property not found: ' + str(exception), code='404')
        elif isinstance(exception, AttributeError) and 'Request\' object has no attribute \'info\'' in str(exception):
            return RestJsonResponse(msg='request content type must be application/json', code='400', status=400)

