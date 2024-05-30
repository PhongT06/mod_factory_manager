import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from faker import Faker
from datetime import datetime

fake = Faker()

class TestProductionEndpoints(unittest.TestCase):
    def setUp(self):
        app = create_app('TestingConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('services.productionService.save')
    def test_create_production(self, mock_save):
        product_id = fake.random_int(min=1)
        quantity_produced = fake.random_int(min=1)
        date_produced = datetime.now().date()
        mock_production = MagicMock(
            id=fake.random_int(min=1),
            product_id=product_id,
            quantity_produced=quantity_produced,
            date_produced=date_produced
        )
        mock_save.return_value = mock_production

        payload = {
            "product_id": product_id,
            "quantity_produced": quantity_produced,
            "date_produced": date_produced.isoformat()
        }
        response = self.app.post('/production/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], mock_production.id)
        self.assertEqual(response.json['product_id'], product_id)
        self.assertEqual(response.json['quantity_produced'], quantity_produced)

    @patch('services.productionService.find_all')
    def test_get_all_production_records(self, mock_find_all):
        mock_records = [
            MagicMock(id=fake.random_int(min=1), product_id=fake.random_int(min=1), quantity_produced=fake.random_int(min=1), date_produced=datetime.now().date()),
            MagicMock(id=fake.random_int(min=1), product_id=fake.random_int(min=1), quantity_produced=fake.random_int(min=1), date_produced=datetime.now().date())
        ]
        mock_find_all.return_value = mock_records

        response = self.app.get('/production/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), len(mock_records))

    @patch('services.productionService.find_by_id')
    def test_get_production_record_by_id(self, mock_find_by_id):
        production_id = fake.random_int(min=1)
        mock_record = MagicMock(
            id=production_id,
            product_id=fake.random_int(min=1),
            quantity_produced=fake.random_int(min=1),
            date_produced=datetime.now().date()
        )
        mock_find_by_id.return_value = mock_record

        response = self.app.get(f'/production/{production_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], production_id)