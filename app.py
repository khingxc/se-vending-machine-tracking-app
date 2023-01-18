import os
from flask import Flask
from extensions import db
from dotenv import load_dotenv
from sqlalchemy import create_engine
from routes import routes_vending_machine, routes_stock
from sqlalchemy_utils import database_exists, create_database


load_dotenv()

app = Flask(__name__)
url = os.environ['URL']
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine(url)
if not database_exists(engine.url):
    create_database(engine.url)

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(routes_stock.routes_stock_bp)
    app.register_blueprint(routes_vending_machine.routes_vending_machine_bp)
    app.run(debug=True)



