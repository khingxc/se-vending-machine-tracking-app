"""Running the whole application."""
import os

from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

from extensions import db
from routes import routes_stock, routes_vending_machine

load_dotenv()

app = Flask(__name__)
url = os.environ["URL"]
app.config["SQLALCHEMY_DATABASE_URI"] = url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
engine = create_engine(url)
if not database_exists(engine.url):
    create_database(engine.url)
db.init_app(app)
with app.app_context():
    db.create_all()
app.register_blueprint(routes_stock.routes_stock_bp)
app.register_blueprint(routes_vending_machine.routes_vending_machine_bp)

if __name__ == "__main__":
    app.run(debug=True)
