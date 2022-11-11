import logging

from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger('django')

def exception_response(exception):
    '''
    Takes an exception and returns a JSON Response containing error details
    '''
    response = {}
    response['status_code'] = 500

    if settings.DEBUG or 1:
        response['data'] = {
            'exception_type': exception.__class__.__name__,
            'exception_message': str(exception),
            'exception_description': exception.__doc__
        }
    else:
        response['data'] = 'Error occured during execution.'

    logger.exception(response['data'])
    return response


def regularize_response(response):
    '''
    Regularise different types of data returned under the common key data of a JSON Response
    '''

    ALLOWED_DATA_TYPES = (int, str, list, tuple, float,)

    if isinstance(response, ALLOWED_DATA_TYPES):
        response = {'data': response}

    if isinstance(response, dict):
        if 'status_code' not in response:
            if 'data' not in response:
                response = {'data': response}
            response['status_code'] = 200
    else:
        try:
            err_msg = "View returned %s, which is not convertable to JSON"
            assert isinstance(response, dict), err_msg % type(
                response).__name__
        except Exception as e:
            response = exception_response(e)

    return response

def JsonResponseDec(view):
    '''
    Converts any data returned by a function into a JSON Response format.
    '''

    def wrapper(*args, **kwargs):

        try:
            response = view(*args, **kwargs)
        except Exception as e:
            logger.error("JsonResponseDecorator: {}".format(e))
            response = exception_response(e)

        response = regularize_response(response)
        return JsonResponse(response)
    # logger.info('JsonResponseDecorator: Successful')
    return wrapper