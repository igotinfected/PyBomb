"""Tests for the PyBomb.Response module."""
from unittest.mock import MagicMock

import pytest
from requests.models import Response as RequestsResponse

from pybomb.response import Response


class TestResponse:
    """Tests for the Response."""

    @pytest.fixture
    def mock_response(self) -> MagicMock:
        """Mock response fixture."""
        mock_response = MagicMock(RequestsResponse)
        mock_response.url = "https://fake.com"

        mock_response.json.return_value = {
            "status_code": 1,
            "number_of_page_results": 1,
            "number_of_total_results": 1,
            "results": [{"id": 1, "description": "Great Game"}],
        }

        return mock_response

    def test_response_factory(self, mock_response: MagicMock) -> None:
        """Test the from_response_data factory.

        Make sure the supplied raw response is used to create a Response object.
        """
        res = Response.from_response_data(mock_response)

        assert res.uri == mock_response.url

        mock_res_json = mock_response.json()
        assert res.num_page_results == mock_res_json["number_of_page_results"]
        assert res.results == mock_res_json["results"]
        assert res.num_total_results == mock_res_json["number_of_total_results"]
