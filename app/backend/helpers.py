
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

    start = (page - 1) * 10
    end = start + 10

    return {
        'start': start,
        'end': end
    }

def get_formatted_questions_in_page(page):

    pageObj = get_start_and_end_nums(page)

    questions = Question.query.limit(QUESTIONS_PER_PAGE).all()

    formatted_questions = [question.format() for question in questions]

    return formatted_questions[pageObj['start']:pageObj['end']]

