import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from faker import Faker
from datetime import datetime

fake = Faker()

class TestOrderEndpoints(unittest.TestCase):
    def setUp(self):
        app = create_app('TestingConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('services.orderService.save')
    @patch('auth.token_auth.current_user')
    def test_create_order(self, mock_current_user, mock_save):
        customer_id = fake.random_int(min=1)
        product_ids = [fake.random_int(min=1) for _ in range(3)]
        products = [{'id': pid, 'name': fake.word(), 'price': fake.pyfloat(positive=True)} for pid in product_ids]
        mock_order = MagicMock(id=fake.random_int(min=1), date=datetime.now().date(), customer_id=customer_id, products=products)
        mock_save.return_value = mock_order
        mock_current_user.return_value = MagicMock(id=customer_id)

        payload = {
            "products": products
        }
        response = self.app.post('/orders/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], mock_order.id)
        self.assertEqual(response.json['customer_id'], customer_id)

    @patch('services.orderService.find_all')
    def test_get_all_orders(self, mock_find_all):
        mock_orders = [
            MagicMock(id=fake.random_int(min=1), date=datetime.now().date(), customer_id=fake.random_int(min=1), products=[]),
            MagicMock(id=fake.random_int(min=1), date=datetime.now().date(), customer_id=fake.random_int(min=1), products=[])
        ]
        mock_find_all.return_value = mock_orders

        response = self.app.get('/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), len(mock_orders))

    @patch('services.orderService.save')
    @patch('auth.token_auth.current_user')
    def test_create_order_with_invalid_product(self, mock_current_user, mock_save):
        customer_id = fake.random_int(min=1)
        product_ids = [fake.random_int(min=1) for _ in range(3)]
        products = [{'id': pid, 'name': fake.word(), 'price': fake.pyfloat(positive=True)} for pid in product_ids]
        mock_current_user.return_value = MagicMock(id=customer_id)
        mock_save.side_effect = ValueError("One or more products do not exist")

        payload = {
            "products": products
        }
        response = self.app.post('/orders/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)