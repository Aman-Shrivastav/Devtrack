import time
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration_ms = (time.time() - start_time) * 1000
        method = request.method
        path = request.path
        status_code = response.status_code
        
        print(f"[{method}] {path} - {status_code} - {duration_ms:.2f}ms")
        
        return response
