from flask import url_for
from unittest import mock

from tests.base_test import BaseTestAPI
from tests.mock import mocked_requests_get


class TestSearch(BaseTestAPI):
    """
    Tests for Search Process endpoint
    """

    def test_search_with_invalid_json_return_400(self):
        response = self.client.post(url_for('search'))

        self.assertEqual(response.status_code, 400)

    def test_search_missing_process_number_return_400(self):
        response = self.client.post(url_for('search'), json={'process_number': ''})

        self.assertEqual(response.status_code, 400)

    def test_search_with_invalid_process_number_format_return_400(self):
        response = self.client.post(url_for('search'), json={'process_number': '0710802-55.208.02.0001'})

        self.assertEqual(response.status_code, 400)

    def test_search_with_invalid_process_number_j_return_400(self):
        response = self.client.post(url_for('search'), json={'process_number': '0710802-55.2018.9.02.0001'})

        self.assertEqual(response.status_code, 400)

    def test_search_with_unavailable_process_number_tr_return_400(self):
        response = self.client.post(url_for('search'), json={'process_number': '0710802-55.2018.8.32.0001'})

        self.assertEqual(response.status_code, 400)

    @mock.patch('crawlers.base_crawler.requests.get', side_effect=mocked_requests_get)
    def test_search_process_without_data_return_404(self, mock_get):
        response = self.client.post(url_for('search'), json={'process_number': '0710802-55.2020.8.02.0001'})

        self.assertEqual(response.status_code, 404)

    @mock.patch('crawlers.base_crawler.requests.get', side_effect=mocked_requests_get)
    def test_search_tjal_return_200(self, mock_get):
        response = self.client.post(url_for('search'), json={'process_number': '0710802-55.2018.8.02.0001'})

        self.assertEqual(response.status_code, 200)

    @mock.patch('crawlers.base_crawler.requests.get', side_effect=mocked_requests_get)
    def test_search_tjms_return_200(self, mock_get):
        response = self.client.post(url_for('search'), json={'process_number': '0821901-51.2018.8.12.0001'})

        self.assertEqual(response.status_code, 200)
