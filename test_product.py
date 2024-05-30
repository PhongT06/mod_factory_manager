import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from faker import Faker

fake = Faker()

class TestProductEndpoints(unittest.TestCase):
    def setUp(self):
        app = create_app('TestingConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('services.productService.save')
    def test_create_product(self, mock_save):
        name = fake.word()
        price = fake.pyfloat(positive=True)
        mock_product = MagicMock()
        mock_product.id = 1
        mock_product.name = name
        mock_product.price = price
        mock_save.return_value = mock_product

        payload = {
            "name": name,
            "price": price
        }
        response = self.app.post('/products/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], mock_product.id)

    @patch('services.productService.find_all')
    def test_get_all_products(self, mock_find_all):
        mock_products = [
            MagicMock(id=1, name=fake.word(), price=fake.pyfloat(positive=True)),
            MagicMock(id=2, name=fake.word(), price=fake.pyfloat(positive=True))
        ]
        mock_find_all.return_value = mock_products

        response = self.app.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), len(mock_products))

    @patch('services.productService.find_all')
    def test_get_products_with_search_term(self, mock_find_all):
        search_term = 'example'
        mock_products = [
            MagicMock(id=1, name=f"{search_term} product", price=fake.pyfloat(positive=True)),
            MagicMock(id=2, name=f"another {search_term} product", price=fake.pyfloat(positive=True))
        ]
        mock_find_all.return_value = mock_products

        response = self.app.get(f'/products/?search={search_term}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), len(mock_products))
        for product in response.json:
            self.assertIn(search_term, product['name'].lower())