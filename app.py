from flask import Flask, jsonify, request
import _json
import pandas as pd
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import create_engine 



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/housing_data.json'
db = SQLAlchemy(app)

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50))
    sale_price = db.Column(db.Float)

    def __init__(self, location, sale_price):
        self.location = location
        self.sale_price = sale_price


@app.route('/api/houses', methods=['POST'])
def add_house():
    data = request.get_json()
    for house_data in data:
        new_house = House(location=house_data['location'], sale_price=house_data['sale_price'])
        db.session.add(new_house)
    db.session.commit()
    return {"message": "Data added successfully"}, 201


from sqlalchemy.sql import func

@app.route('/api/houses/average_price', methods=['GET'])
def get_average_price():
    result = db.session.query(func.avg(House.sale_price)).scalar()
    return {"average_sale_price": result}

@app.route('/api/houses/average_price_per_location', methods=['GET'])
def get_average_price_per_location():
    result = db.session.query(House.location, func.avg(House.sale_price)).group_by(House.location).all()
    return {location: avg_price for location, avg_price in result}

@app.route('/api/houses/max_price', methods=['GET'])
def get_max_price():
    result = db.session.query(func.max(House.sale_price)).scalar()
    return {"max_sale_price": result}

@app.route('/api/houses/min_price', methods=['GET'])
def get_min_price():
    result = db.session.query(func.min(House.sale_price)).scalar()
    return {"min_sale_price": result}

if __name__ == "__main__":
    app.run(debug = True)

engine = create_engine('postgresql://postgres:@localhost:5432/') 

db.to_sql('housing_data.json_from_python', engine, if_exists='replace')
