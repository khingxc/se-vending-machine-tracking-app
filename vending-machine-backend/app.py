import os
import json
import sqlalchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from sqlalchemy import Text
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

uri = f"mariadb+mariadbconnector://root:hardpass@127.0.0.1:3307/vending-machines-backend"

app = Flask(__name__)
engine = sqlalchemy.create_engine(uri)

Base = declarative_base()

class VendingMachine(Base):
    __tablename__ = 'vendingmachine'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    location = sqlalchemy.Column(sqlalchemy.String(length=100))
    created_date = sqlalchemy.Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

def view_all_vending_machines():
    machines = session.query(VendingMachine).order_by(VendingMachine.created_date.desc())
    machines_list = []
    for machine in machines:
        machines_list.append({"id": machine.id,
                              "location": machine.location,
                              "created_date": str(machine.created_date)})
    return machines_list

@app.route("/machine/create", methods=['POST'])
def create_vending_machine():
    location = request.form.get("location")
    print(location)
    if (location is None):
        return jsonify(error={"name": "this field is required"}), 400
    new_machine = VendingMachine(location=location)
    session.add(new_machine)
    session.commit()
    return jsonify({"location": location, "id": new_machine.id}), 200

@app.route("/machine/<ID>", methods=['GET'])
def search_machine_from_id(ID):
    response = session.query(VendingMachine).get(ID)
    if response is None:
        return jsonify({}), 404
    else:
        return jsonify({"id": response.id,
                        "location": response.location,
                        "created_date": str(response.created_date)}), 200

@app.route("/machine/view", methods=['POST'])
def view_machines():
    return json.dumps(view_all_vending_machines())

@app.route("/machine/delete/<ID>", methods=['DELETE'])
def delete_machine(ID):
    response = session.query(VendingMachine).get(ID)
    if response is None:
        return jsonify({}), 404
    session.delete(response)
    session.commit()
    return "", 201

if __name__ == '__main__':
    app.run()
