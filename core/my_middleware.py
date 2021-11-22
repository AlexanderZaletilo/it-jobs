import logging

logger = logging.getLogger(__name__)


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        logger.info(f"request:{request}, response: {response}")
        return response

    def process_exception(self, request, exception):
        logger.error(f"Messages form middleware: Excpetion is {exception}")
