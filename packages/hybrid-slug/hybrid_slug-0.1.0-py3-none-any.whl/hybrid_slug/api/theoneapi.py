import requests

from hybrid_slug.api.base import RateLimitedAPI


class TheOneAPIClient(RateLimitedAPI):
    def __init__(self, access_token, base_url='https://the-one-api.dev/v2/'):
        session = requests.Session()
        session.headers = {
            'Authorization': f'Bearer {access_token}'
        }
        super().__init__(
            base_url=base_url,
            session=session,
            window_size=600,
            request_limit=100,
        )

    def _build_list_request_params(self, page, limit, filters=None):
        params = {
            'page': page,
            'limit': limit,
        }
        if filters:
            for key, value in filters.items():
                params[key] = value

    def get_movie(self, movie_id):
        resp = self.get(f'/movie/{movie_id}')
        self._raise_error_if_necessary(resp)
        resp_json = resp.json()
        return resp_json

    def list_movies(self, page=0, limit=10, filters=None):
        params = self._build_list_request_params(page=page, limit=limit, filters=filters)
        resp = self.get('/movie', params=params)
        self._raise_error_if_necessary(resp)
        resp_json = resp.json()
        return resp_json

    def list_movie_quotes(self, movie_id, page=0, limit=10, filters=None):
        params = self._build_list_request_params(page=page, limit=limit, filters=filters)
        resp = self.get(f'/movie/{movie_id}/quote', params=params)
        self._raise_error_if_necessary(resp)
        resp_json = resp.json()
        return resp_json
