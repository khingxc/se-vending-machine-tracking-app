import os
from extensions import db
from dotenv import load_dotenv
from routes import view, create, delete
from sqlalchemy import create_engine
from flask import request, jsonify, Flask, Blueprint
from sqlalchemy_utils import database_exists, create_database


load_dotenv()

app = Flask(__name__)
url = os.environ['URL']
app.config['SQLALCHEMY_DATABASE_URI'] = url
engine = create_engine(url)
if not database_exists(engine.url):
    create_database(engine.url)

if __name__ == '__main__':
    db.init_app(app)
    with app.app_conext():
        db.create_all()
    app.register_blueprint(view.view_bp)
    app.register_blueprint(create.create_bp)
    app.register_blueprint(delete.delete_bp)
    app.run(debug=True)



