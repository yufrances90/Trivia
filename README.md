# Trivia



## Full Stack Trivia API Backend


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```


#### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```


#### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


#### Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```



## Full Stack Trivia API Frontend


#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**


#### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```



## API Reference


#### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, ``` http://127.0.0.1:5000 ```, which is set as proxy in the frontend configuration
- Authentication: This version of the application does not require authentication or API keys


#### Error Handling

Errors are returned as JSON objects in the following format:
```
    {
        "success": False,
        "error": 400,
        "message": "Bad request"
    }
```
The API will return three error types when requests fail:
- 400: Bad request
- 404: Not found
- 422: Unprocessable entity


#### Endpoints

GET '/categories'
- Fetches all available categories 
- Request Arguments: None
- Returns: A list of category tuple with its id and type 
    [
        ('1', "Science"),
        ('2', "Art"),
        ('3', "Geography"),
        ('4', "History"),
        ('5', "Entertainment"),
        ('6', "Sports")
    ]

GET '/questions'
- Fetches paginated questions 
- Request Arguments: 
    - page: current page number
- Returns: 
    - questions: A limited list of question object with its question, answer, category, difficulty
    - total_questons: The total number of questions
    - cateogories: A list of category tuple with its id and type
    - current_category: (None for now)
    - success: True 
    {
        'questions': [],
        'total_questions': total_num_of_questions,
        'categories': 
            [
                ('1', "Science"),
                ('2', "Art"),
                ('3', "Geography"),
                ('4', "History"),
                ('5', "Entertainment"),
                ('6', "Sports")
            ],
        'current_category': None,
        'success': True
    }

DELETE '/questions/<int:question_id>'
- Deletes question using a question ID
- Request Arguments: 
    - question_id: a question ID of integer type
- Returns: 
    - success: True

POST '/questions'
- Gets questions based on a search term OR Posts a new question
- 
    - Request Data: 
        - searchTerm: a substring of the question
    - Returns:
        - questions: A limited list of question object with its  question, answer, category, difficulty
        - total_questons: The total number of questions
        - cateogories: A list of category tuple with its id and type
        - current_category: (None for now)
        - success: True
        {
            'questions': [],
            'total_questions': total_num_of_questions,
            'categories': 
                [
                    ('1', "Science"),
                    ('2', "Art"),
                    ('3', "Geography"),
                    ('4', "History"),
                    ('5', "Entertainment"),
                    ('6', "Sports")
                ],
            'current_category': None,
            'success': True
        }
- 
    - Request Data: 
        - a question object
        {
            'question': '',
            'answer': '',
            'category': 'Science',
            'difficulty': 3
        }
    - Returns:
        - success: True

GET '/categories/<int:category_id>/questions'
- Gets questions based on category
- Request Arguments: 
    - category_id: The id of a category
- Returns:
    An object contains the following:
        - questions: A limited list of question object with its  question, answer, category, difficulty
        - total_questons: The total number of questions
        - current_category: The category with id as category_id
        - success: True
        {
            'questions': [],
            'total_questions': total_num_of_questions,
            'current_category': None,
            'success': True
        }

POST '/quizzes'
- Gets next question to play the quiz
- Request Data:
    - quiz_category: selected category
    - previous_questions: a list of previous question ids
- Returns:
    - question: A question object with its cateogry the same as selected category but never returns before