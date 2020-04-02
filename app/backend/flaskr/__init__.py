import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db

from helpers import \
  get_formatted_categories, \
  get_categories_in_tuples, \
  get_start_and_end_nums, \
  get_formatted_questions_in_page, \
  get_category_by_id, \
  get_questions_by_category_id, \
  delete_question_by_question_id, \
  save_question

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=["GET"])
  def get_all_categories():

    categories = get_categories_in_tuples()

    if len(categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': categories
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=["GET"])
  def get_questions():

    page = request.args.get('page', 1, type=int)

    # get paginated questions
    result = get_formatted_questions_in_page(page, None)

    total_num_of_questions = result['total_num']

    if total_num_of_questions == 0:
      abort(404)

    res = {
      'questions': result['questions'],
      'total_questions': total_num_of_questions,
      'categories': get_categories_in_tuples(),
      'current_category': None
    }

    return jsonify(res)


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=["DELETE"])
  def delete_question_by_id(question_id):

    try:
      
      delete_question_by_question_id(question_id)

      return jsonify({
        'success': True
      })

    except Exception as e:
      
      print(e)

      abort(422)


  
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 

  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=["POST"])
  def search_questions_or_save_new_question():

    request_data = json.loads(request.data)

    if 'searchTerm' in request_data: ## search questions by user input

      search_term = request_data['searchTerm']

      result = get_formatted_questions_in_page(None, search_term)

      total_num_of_question = result['total_num']

      if total_num_of_question == 0:
        abort(404)

      res = {
        'questions': result['questions'],
        'total_questions': total_num_of_question,
        'categories': get_categories_in_tuples(),
        'current_category': None
      }

      return jsonify(res)

    else: ## insert new question

      if not('question' in request_data and 'answer' in request_data):
        abort(400)

      question_dict = request_data

      try:
        
        save_question(question_dict)

        return jsonify({
          'success': True
        })

      except Exception as e:
        
        print(e)

        abort(422)

      

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=["GET"])
  def get_questions_by_category(category_id):

    category = get_category_by_id(category_id + 1)

    if category is None:
      abort(404)

    questions = get_questions_by_category_id(category_id)

    res = {
      'current_category': category.type,
      'questions': questions,
      'total_questions': len(questions)
    }

    return jsonify(res)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Resource not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Unprocessable entity'
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad request'
    }), 400
  
  return app

    