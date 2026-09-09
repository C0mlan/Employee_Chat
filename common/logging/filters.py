import logging

from request_id.logging import get_current_request_id


class RequestIdFilter(logging.Filter):
    
    def filter(self, record):
        record.request_id = get_current_request_id() or "-"
        return True