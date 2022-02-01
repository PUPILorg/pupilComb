import functools

from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN


def professor_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if args[1].user.professor:
                return func(*args, **kwargs)
        except:
            return Response(status=HTTP_403_FORBIDDEN)
    return wrapper

def student_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if args[1].user.student:
                return func(*args, **kwargs)
        except:
            return Response(status=HTTP_403_FORBIDDEN)
    return wrapper