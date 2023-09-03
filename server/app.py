#!/usr/bin/env python3

from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    zoo_keeper = Zookeeper.query.filter(Zookeeper.id == animal.zookeeper_id).first()
    enclosure = Enclosure.query.filter(Enclosure.id == animal.enclosure_id).first()
    response_body = f"<ul>ID: {animal.id}</ul>"
    response_body += f"<ul>Name: {animal.name}</ul>"
    response_body += f"<ul>Species: {animal.species}</ul>"
    response_body += f"<ul>Zookeeper: {zoo_keeper.name}</ul>"
    response_body += f"<ul>Enclosure: {enclosure.environment}</ul>"
    response = make_response(response_body)
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    # Pull all of the critical informatioon out of the Zookeeper table.
    zoo_keeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    response_body = f"<ul>ID: {zoo_keeper.id}"
    response_body += f"<ul>Name: {zoo_keeper.name}"
    response_body += f"<ul>Birthday: {zoo_keeper.birthday}"

    animals = Animal.query.filter(Animal.zookeeper_id == zoo_keeper.id)
    for animal in animals:
        response_body += f"<ul>Animal: {animal.name}"


    response = make_response(response_body, 200)
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    # Pull all of the critical informatioon out of the Zookeeper table.
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    response_body = f"<ul>ID: {enclosure.id}"
    response_body += f"<ul>Environment: {enclosure.environment}"
    response_body += f"<ul>Open to Visitors: {'True' if enclosure.open_to_visitors else 'False'}"

    animals = Animal.query.filter(Animal.enclosure_id == enclosure.id)
    for animal in animals:
        response_body += f"<ul>Animal: {animal.name}"

    response = make_response(response_body, 200)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)

@app.route('/')
def index():
    response = make_response(
        '<h1>Welcome to the pet/owner directory!</h1>',
        200
    )
    return response

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if not pet:
        response_body = '<h1>404 pet not found</h1>'
        response = make_response(response_body, 404)
        return response
    
    response_body = f'''
        <h1>Information for {pet.name}</h1>
        <h2>Pet Species is {pet.species}</h2>
        <h2>Pet Owner is {pet.owner.name}</h2>
    '''

    response = make_response(response_body, 200)

    return response
