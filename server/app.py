#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/plants')
def get_plants():
    plants_list=[]
    for plant in Plant.query.all():
        plants_dict={
            "id":plant.id,
            "name":plant.name,
            "image":plant.image,
            "price":plant.price            
        }
        plants_list.append(plants_dict)
        response=make_response(jsonify(plants_list), 200)
        response.headers['Content-type']='application/json'
        return response
@app.route('/plants/<int:id>')
def get_plants_by_id(id):
    plant_item=[]
    plant=Plant.query.filter_by(id=id).first()
    if plant:
        plant_dict={
            "id":plant.id,
            "name":plant.name,
            "image":plant.image,
            "price":plant.price            
        }
        plant_item.append(plant_dict)
        response=make_response(jsonify(plant_dict), 200)
        response.headers['Content-Type']='application/json'
        return response
    else:
        response_body={'error':'Plant not found'}
        response=make_response(jsonify(response_body), 404)
        response.headers['Content-Type']='application.json'
        return response
    
@app.route('/plants', methods=['GET', 'POST'])
def create_plant():
    if request.method == 'GET':
        plants = [plant.to_dict() for plant in Plant.query.all()]
        response = make_response(jsonify(plants), 200)
    elif request.method == 'POST':
            new_plant = Plant(
                name=request.form.get('name'),
                image=request.form.get('image'),
                price=request.form.get('price')
            )
            db.session.add(new_plant)
            db.session.commit()
            plant_dict = new_plant.to_dict()
            response = make_response(jsonify(plant_dict), 201) 
    
    return response
 

class Plants(Resource):
    def get(self):
        plants_dict=Plant.query.all()
        response=make_response(jsonify(plants_dict), 200)
        return response
    pass

class PlantByID(Resource):
    pass
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
