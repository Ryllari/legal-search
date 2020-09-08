from flask import url_for

from tests.base_test import BaseTestAPI


class TestIndex(BaseTestAPI):
    """
    Tests for Welcome endpoint
    """

    def test_index_return_200(self):
        response = self.client.get(url_for('index'))

        self.assertEqual(response.status_code, 200)
