import os
import json
import sqlalchemy
from dotenv import load_dotenv
from routes.view import view_bp
from models import VendingMachine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify

load_dotenv()

url = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@127.0.0.1:5432/{os.environ.get('POSTGRES_DB')}"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.register_blueprint(view_bp)

with app.app_context():
    db = SQLAlchemy(app)
    db.create_all()

    if __name__ == '__main__':
        app.run()
