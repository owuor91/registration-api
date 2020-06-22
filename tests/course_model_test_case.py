import unittest

from sqlalchemy.sql import text

from app import create_app, db
from config import TestingConfig
from utils.util import decode_response_to_json


class CourseModelTestCase(unittest.TestCase):
    """Test case for course model"""

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.course = {
            "course_name": "Operations Research 1",
            "course_code": "DIS 106",
            "description": "Operations research fundamentals",
            "instructor": "Canns Bean"
        }

        with self.app.app_context():
            db.create_all()
            db.session.execute(text('DELETE FROM courses'))
            db.session.commit()

    def test_creating_course(self):
        """Test creating course"""
        response = self.client.post('/courses', data=self.course)
        response_json = decode_response_to_json(response)
        self.assertEqual(response.status_code, 201)
        self.assertEqual('DIS 106', response_json['course']['course_code'])

    def test_fetching_all_courses(self):
        """Test fetching all courses"""
        self.client.post('/courses', data=self.course)
        self.course['course_code'] = 'DIS 304'
        self.client.post('/courses', data=self.course)
        response = self.client.get('/courses')
        response_json = decode_response_to_json(response)
        self.assertEqual(len(response_json['courses']), 2)

    def test_fetching_course_by_id(self):
        """Test fetching courses by id"""
        res = self.client.post('/courses', data=self.course)
        course_id = decode_response_to_json(res)['course']['course_id']
        rsp = self.client.get('/courses/{}'.format(course_id))
        rsp_json = decode_response_to_json(rsp)
        self.assertEqual(rsp_json['course']['instructor'], 'Canns Bean')

    def test_empty_params(self):
        """Test posting course with missing fields"""
        result = self.client.post('/courses', data={})
        json_result = decode_response_to_json(result)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(json_result['errors']['course_name'], 'course_name is required')

    def tearDown(self):
        """tear down initialized test vars"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
