
from models import Question, Category

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

    return formatted_questions[pageObj['start']:pageObj['end']] if page is not None \
        else formatted_questions

def get_category_by_id(category_id):
    return Category.query.filter_by(id = category_id).first()

def get_questions_by_category_id(category_id):
    
    questions = Question.query.filter_by(category = category_id)

    return [question.format() for question in questions]