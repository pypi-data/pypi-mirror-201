import time
from collections import deque

from hybrid_slug.api.exceptions import RateLimitExceededError


class BaseAPI(object):
    DEFAULT_TIMEOUT = 30

    def __init__(self, base_url, session):
        self.base_url = base_url
        self.session = session

    def _raise_error_if_necessary(self, response):
        response.raise_for_status()

    def request(self, method, uri, **kwargs):
        kwargs.setdefault('timeout', self.DEFAULT_TIMEOUT)
        full_url = f'{self.base_url}{uri}'
        response = self.session.request(method, full_url, **kwargs)
        return response

    def get(self, uri, **kwargs):
        return self.request('GET', uri, **kwargs)

    def post(self, uri, **kwargs):
        return self.request('POST', uri, **kwargs)

    def put(self, uri, **kwargs):
        return self.request('PUT', uri, **kwargs)

    def patch(self, uri, **kwargs):
        return self.request('PATCH', uri, **kwargs)

    def delete(self, uri, **kwargs):
        return self.request('DELETE', uri, **kwargs)


class RateLimitedAPI(BaseAPI):
    def __init__(self, base_url, session, window_size, request_limit):
        self._window_size = window_size
        self._request_limit = request_limit
        self._request_timestamps = deque()
        super().__init__(base_url=base_url, session=session)

    def _check_rate_limit(self):
        now = time.time()
        while self._request_timestamps and self._request_timestamps[0] < now - self._window_size:
            self._request_timestamps.popleft()

        if len(self._request_timestamps) >= self._request_limit:
            raise RateLimitExceededError(
                f'Rate limit of {self._request_limit} requests per {self._window_size} seconds exceeded.'
            )

    def request(self, method, uri, **kwargs):
        self._check_rate_limit()
        return super().request(method, uri, **kwargs)
