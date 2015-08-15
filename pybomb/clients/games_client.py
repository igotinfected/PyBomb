"""
Client for the Games resource of GiantBomb
http://www.giantbomb.com/api/documentation#toc-0-15
"""
from pybomb.clients.base_client import BaseClient


class GamesClient(BaseClient):
    """
    Client for the 'games' API resource
    """

    RESOURCE_NAME = 'games'

    RESPONSE_FIELD_MAP = {
        'aliases': (True, False),
        'api_detail_url': (False, False),
        'date_added': (True, True),
        'date_last_updated': (True, True),
        'deck': (False, False),
        'description': (False, False),
        'expected_release_month': (True, False),
        'expected_release_quarter': (True, False),
        'expected_release_year': (True, False),
        'id': (True, True),
        'image': (False, False),
        'name': (True, True),
        'number_of_user_reviews': (True, True),
        'original_game_rating': (False, True),
        'original_release_date': (True, True),
        'platforms': (True, False),
        'site_detail_url': (False, False),
    }

    def search(self, filter_by, return_fields, sort_by, desc=True, limit=None, offset=None):
        """
        Full search of games resource, supporting all search fields available in API
        http://www.giantbomb.com/api/documentation#toc-0-15

        :param filter_by: dict
        :param return_fields: tuple
        :param sort_by: string
        :param desc: bool
        :param limit: int
        :param offset: int
        :return: pybomb.clients.Response
        """
        self._validate_filter_fields(filter_by)
        self._validate_return_fields(return_fields)
        self._validate_sort_field(sort_by)

        search_filter = self._create_search_filter(filter_by)
        field_list = ','.join(return_fields)

        if desc:
            direction = self.SORT_ORDER_DESCENDING
        else:
            direction = self.SORT_ORDER_ASCENDING

        search_params = {
            'filter': search_filter,
            'field_list': field_list,
            'sort': '{}:{}'.format(sort_by, direction),
            'limit': int(limit),
            'offset': int(offset)
        }

        response = self._query(search_params)

        return response

    def quick_search(self, name, platform=None, sort_by=None, desc=True):
        """
        Quick search method that allows you to search for a game using only the
        title and the platform

        :param name: string
        :param platform: int
        :param sort_by: string
        :param desc: bool
        :return: pybomb.clients.Response
        """
        if platform is None:
            query_filter = 'name:{}'.format(name)
        else:
            query_filter = 'name:{},platforms:{}'.format(name, platform)

        search_params = {'filter': query_filter}

        if sort_by is not None:
            if desc:
                direction = self.SORT_ORDER_DESCENDING
            else:
                direction = self.SORT_ORDER_ASCENDING

            search_params['sort'] = '{}:{}'.format(sort_by, direction),

        response = self._query(search_params)

        return response