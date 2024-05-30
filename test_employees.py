import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from faker import Faker

fake = Faker()

class TestEmployeeEndpoints(unittest.TestCase):
    def setUp(self):
        app = create_app('TestingConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('services.employeeService.save')
    def test_create_employee(self, mock_save):
        name = fake.name()
        position = fake.job()
        mock_employee = MagicMock()
        mock_employee.id = 1
        mock_employee.name = name
        mock_employee.position = position
        mock_save.return_value = mock_employee

        payload = {
            "name": name,
            "position": position
        }
        response = self.app.post('/employees/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], mock_employee.id)

    @patch('services.employeeService.find_all')
    def test_get_all_employees(self, mock_find_all):
        mock_employees = [
            MagicMock(id=1, name=fake.name(), position=fake.job()),
            MagicMock(id=2, name=fake.name(), position=fake.job())
        ]
        mock_find_all.return_value = mock_employees

        response = self.app.get('/employees/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), len(mock_employees))

    @patch('services.employeeService.find_by_id')
    def test_get_employee_by_id(self, mock_find_by_id):
        employee_id = 1
        mock_employee = MagicMock(id=employee_id, name=fake.name(), position=fake.job())
        mock_find_by_id.return_value = mock_employee

        response = self.app.get(f'/employees/{employee_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], employee_id)

    @patch('services.employeeService.find_by_id')
    def test_get_nonexistent_employee(self, mock_find_by_id):
        employee_id = 999
        mock_find_by_id.return_value = None

        response = self.app.get(f'/employees/{employee_id}')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)