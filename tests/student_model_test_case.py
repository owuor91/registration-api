import json
import unittest

from sqlalchemy.sql import text

from app import create_app, db
from config import TestingConfig


class StudentModelTestCase(unittest.TestCase):
    """Test case for student model"""

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.student = {
            'first_name': 'Anastacia',
            'last_name': 'Amagoro',
            'email': 'amagoro@gmail.com',
            'phone_number': '0700000002',
            'date_of_birth': '1997-10-24',
            'sex': 'female'
        }

        with self.app.app_context():
            db.create_all()
            db.engine.execute(text('DELETE FROM students'))

    def test_student_creation(self):
        """Test API can create student"""
        response = self.client.post('/students', data=self.student)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Anastacia', str(response.data))

    def test_duplicate_student_creation(self):
        """Test creating duplicate student"""
        self.client.post('/students', data=self.student)
        response = self.client.post('/students', data=self.student)
        self.assertEqual(response.status_code, 400)
        self.assertIn('a student with the number 0700000002 already exists', str(response.data))

    def test_fetch_all_students(self):
        """Test fetching all students"""
        self.client.post('/students', data=self.student)
        response = self.client.get('/students')
        json_response = self.decode_response_to_json(response)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(json_response['students']) == 1)

    def test_fetch_student_by_id(self):
        """test fetching student by id"""
        result = self.client.post('/students', data=self.student)
        json_result = self.decode_response_to_json(result)
        response = self.client.get('/students/{}'.format(json_result['student']['student_id']))
        self.assertEqual(response.status_code, 200)

    def test_deleting_student(self):
        """test deleting student"""
        result = self.client.post('/students', data=self.student)
        json_result = self.decode_response_to_json(result)
        student_id = json_result['student']['student_id']
        response = self.client.delete('/students/{}'.format(student_id))
        self.assertEqual(response.status_code, 204)
        fetch_response = self.client.get('/students/{}'.format(student_id))
        self.assertEqual(fetch_response.status_code, 404)

    def test_editing_student(self):
        """test editing student"""
        result = self.client.post('/students', data=self.student)
        json_result = self.decode_response_to_json(result)
        student_id = json_result['student']['student_id']
        response = self.client.put('/students/{}'.format(student_id), data={'first_name': 'Wanjala'})
        fetch_response = self.client.get('/students/{}'.format(student_id))
        json_fetch_response = self.decode_response_to_json(fetch_response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_fetch_response['student']['first_name'], 'Wanjala')

    def test_missing_fields(self):
        result = self.client.post('/students', data={})
        json_result = self.decode_response_to_json(result)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(json_result['errors']['first_name'], 'First name is required')

    def tearDown(self):
        """tear down initialized test vars"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def decode_response_to_json(self, response):
        return json.loads(response.data.decode('utf-8').replace("'", "\""))


if __name__ == '__main__':
    unittest.main()
