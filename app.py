"""Running the whole application."""
import os

from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

from extensions import db
from routes.routes_stock import routes_stock_bp
from routes.routes_vending_machine import routes_vending_machine_bp

load_dotenv()

app = Flask(__name__)
user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
pg = os.environ["POSTGRES_DB"]
url = f"postgresql://{user}:{password}@localhost:5432/{pg}"
app.config["SQLALCHEMY_DATABASE_URI"] = url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
engine = create_engine(url)
if not database_exists(engine.url):
    create_database(engine.url)
db.init_app(app)
with app.app_context():
    db.create_all()
app.register_blueprint(routes_stock_bp)
app.register_blueprint(routes_vending_machine_bp)

if __name__ == "__main__":
    app.run(debug=True)
