import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.role_name = "beijiayu"
        self.database_path = "postgres://{}@{}/{}".format(self.role_name, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):

        self.db.session.remove()
        """Executed after reach test"""
        pass

        

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']) == 6)

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('categories', data)
        self.assertIn('questions', data)
        self.assertIn('current_category', data)
        self.assertIsNone(data['current_category'])
        self.assertTrue(data['total_questions'] == 19)

    def test_404_response_beyond_valid_page_get_questions(self):
        res = self.client().get("/questions?page=100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')

    # uncomment the following test case when doing final testing
    # def test_delete_question(self):

    #     app = create_app()
    #     client = app.test_client

    #     question = Question.query.first()

    #     res = client().delete("/questions/{}".format(question.id))
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])

    def test_422_response_invalid_question_id_delete_question(self):

        app = create_app()
        client = app.test_client

        res = client().delete("/questions/100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_search_question(self):

        res = self.client().post("/questions", json={'searchTerm': 'Cassius'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('categories', data)
        self.assertIn('questions', data)
        self.assertIn('current_category', data)
        self.assertEqual(data['total_questions'], 1)

    def test_no_result_found_search_question(self):

        res = self.client().post("/questions", json={'searchTerm': 'Cassius1'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('categories', data)
        self.assertIn('questions', data)
        self.assertIn('current_category', data)
        self.assertEqual(data['total_questions'], 0)

    def test_400_response_no_parameters_save_new_question(self):

        res = self.client().post("/questions", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_400_response_no_question_provided_save_new_question(self):

        res = self.client().post("/questions", json={'answer': 'Yes'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_400_response_no_answer_provided_save_new_question(self):

        res = self.client().post("/questions", json={'question': '?'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_422_response_no_difficulty_and_category_provided_save_new_question(self):

        res = self.client().post("/questions", json={'question': '?', 'answer': 'Yes'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    # uncomment the following test case when doing final testing
    # def test_save_new_question(self):

    #     app = create_app()
    #     client = app.test_client

    #     res = client().post( \
    #         "/questions", \
    #         json={ \
    #             'question': '?', \
    #             'answer': 'Yes', \
    #             'category': 1, \
    #             'difficulty': 1 \
    #             })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()