#coding=utf8

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


DOESNOTEXIST_MESSAGE = 'Id dose not exist'
UNKNOWN_MESSAGE = 'Unknown error'


class APIErrorResponse(Response):
    """
    API 错误回复基类
    """
    def __init__(self, message=None, data=None, **kwargs):
        super(APIErrorResponse, self).__init__(data={'message': message}, status=HTTP_400_BAD_REQUEST)


class DoesNotExistResponse(APIErrorResponse):
	def __init__(self):
		super(DoesNotExistResponse, self).__init__(message=DOESNOTEXIST_MESSAGE)


class UnKnownResponse(APIErrorResponse):
	def __init__(self):
		super(UnKnownResponse, self).__init__(message=UNKNOWN_MESSAGE)
