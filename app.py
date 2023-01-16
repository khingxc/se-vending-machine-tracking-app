import os
import json
import sqlalchemy
from flask import Flask, request, jsonify
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from models import VendingMachine
from dotenv import load_dotenv
from routes.view import view_bp

load_dotenv()

url = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@127.0.0.1:5432/{os.environ.get('POSTGRES_DB')}"

# conn = psycopg2.connect(
    #     database=f"{os.environ['POSTGRES_DB']}",
    #     user=f"{os.environ['POSTGRES_USER']}",
    #     password=f"{os.environ['POSTGRES_PASSWORD']}",
    # )

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.register_blueprint(view_bp)

with app.app_context():
    db = SQLAlchemy(app)
    db.create_all()

    from routes import view
    # @app.route("/", methods=['GET'])
    # def home():
    #     return "Hello, World!"
        # return jsonify({"greeting": "hello world"}), 200


    if __name__ == '__main__':
        app.run()
