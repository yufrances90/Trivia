
from models import db, Question, Category

QUESTIONS_PER_PAGE = 10

def get_formatted_categories():

    res = Category.query.all()

    categories = {}

    for category in res:
      categories[category.type] = category.format()

    return categories


def get_categories_in_tuples():

    res = Category.query.all()

    categories = []

    for category in res:
      categories.append((category.id, category.type))

    return categories

def get_start_and_end_nums(page):

    if page is None:
        return None

    start = (page - 1) * 10
    end = start + 10

    return {
        'start': start,
        'end': end
    }

def get_or_search_questions(search_term):
    
    return  Question.query.all() if search_term is None else \
        Question.query.filter(Question.question.contains(search_term)).all()


def get_formatted_questions_in_page(page, search_term):

    pageObj = get_start_and_end_nums(page)

    questions = get_or_search_questions(search_term)

    formatted_questions = [question.format() for question in questions]

    return {
        'questions': formatted_questions[pageObj['start']:pageObj['end']] if page is not None \
        else formatted_questions,
        'total_num': len(formatted_questions)
    }
     

def get_category_by_id(category_id):
    return Category.query.filter_by(id = category_id).first()

def get_questions_by_category_id(category_id):
    
    questions = Question.query.filter_by(category = category_id)

    return [question.format() for question in questions]

def delete_question_by_question_id(question_id):

    question = Question.query.filter(Question.id == question_id).first()

    question.delete()

def save_question(question_dict):

    question = Question(
        question = question_dict['question'], 
        answer = question_dict['answer'], 
        category = question_dict['category'], 
        difficulty = question_dict['difficulty']
    )

    question.insert()

def retrieve_next_question(category_id, previous_questions):

    question = None

    if category_id == 0: ## when selected category is all

        question = db.session.query(Question) \
            .filter(Question.id.notin_(previous_questions)) \
            .first()
    else: ## when selected category is not all

        question = db.session.query(Question) \
            .filter(Question.category == category_id) \
            .filter(Question.id.notin_(previous_questions)) \
            .first()

    return question