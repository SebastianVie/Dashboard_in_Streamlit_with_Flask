
# Import the necessary libraries and modules.
from flask import Flask, jsonify, current_app, request
from sqlalchemy import create_engine
from flask_restx import Api, Namespace, Resource


# Define the database access credentials.
host = "34.175.193.108"
user = "root"
passw = "78QsZ!63eB"
database = "HM"

# Initialize Flask.
app = Flask(__name__)
# Defining an API key for authentication
api_key = "Capstone2023"

# Defining a  decorator for checking the API key
def require_api_key(func):
    def wrapper(*args, **kwargs):
        provided_key = request.headers.get('X-API-KEY')
        if provided_key == api_key:
            return func(*args, **kwargs)
        else:
            return {'message': 'Invalid API key'}, 401
    return wrapper

app.config["SQLALCHEMY_DATABASE_URI"] = host

# Create the API Documentation general description.
api = Api(app, version = '1.0',
    title = 'H&M Business Data API',
    description = """
        Using Flask and Flask-Restx this API requests and receives data from H&M MySQL database.
        """,
    contact = "sebastian.viehhofer@student.ie.edu",
    endpoint = "/api/v1"
)

# Establish the connection with the MySQL database using the provided credentials.
def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn
def disconnect(conn):
    conn.close()

# Create a namespace for Customers
customers = Namespace('customers',
    description = 'All operations related to customer informations.',
    path='/api/v1')
api.add_namespace(customers)

# Create an API endpoint for accessing a limited 10000 customer rows.
@customers.route("/customers")
class get_all_users(Resource):
    @require_api_key
    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM customers
            LIMIT 10000;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

# Create a namespace for Transactions
transactions = Namespace('transactions',
    description = 'All operations related to performed transactions.',
    path='/api/v1')
api.add_namespace(transactions)

# access all transaction rows (limited to 10000).
@transactions.route("/transactions")
class get_all_transactions(Resource):
    @require_api_key
    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM transactions
            LIMIT 10000;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

# Create a namespace for Articles in order to isolate its endpoint groups.
articles = Namespace('articles',
    description = 'All operations related to article informations.',
    path='/api/v1')
api.add_namespace(articles)

# Access 10000 article rows.
@articles.route("/articles")
class get_all_articles(Resource):
    @require_api_key
    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM articles
            LIMIT 10000;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

# Create a namespace for Merged Data in order to isolate its endpoint groups.
merged = Namespace('merged',
    description = 'All operations related to article informations.',
    path='/api/v1')
api.add_namespace(merged)

# Access 10000 article rows.
@articles.route("/merged")
class get_all_articles(Resource):
    @require_api_key
    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM merged
            LIMIT 10000;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})
    
# Run the Flask application when the Python script is executed.
if __name__ == '__main__':
    app.run(debug=True)