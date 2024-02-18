from functools import partial

from starlette import status
from starlette.testclient import TestClient

from main import web_app
from source.acetl_web.service import ProductService


class TestDataReadRouter:

    def setup_method(self):
        self.client = partial(TestClient, web_app)

        self.uri = '/read/first-chunk'

        self.mock_product_data_list = {
            "data": [
                {
                    "id": "1e58cc41-5a35-4d0c-bc23-043b2b798073",
                    "name": "size",
                    "code": "89262fa3-d7b0-4d01-9a13-3a93fa8352a6",
                    "price": 39,
                    "quantity": 1,
                    "category": "similar",
                    "creation_date": "2024-02-18T18:39:57.967874"
                }, ]
        }

    def test_get_data_overview_success(self, mocker):
        mocked_service_result = mocker.patch.object(
            ProductService, 'get_data_overview', return_value=self.mock_product_data_list
        )

        result = self.client().get(self.uri)

        assert mocked_service_result.call_count == 1
        assert result.status_code == status.HTTP_200_OK
        assert result.json() == self.mock_product_data_list
