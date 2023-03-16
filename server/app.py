#!/usr/bin/env python3

# Importing required libraries
from flask import Flask, make_response
from flask_migrate import Migrate

# Importing database models
from models import db, Pet, Owner

# Initializing a Flask application
app = Flask(__name__)

# Configuring the application to use the existing database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Disabling track modifications to avoid unhelpful data buildup in memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing Flask-Migrate with the application and database
migrate = Migrate(app, db)

# Initializing the database with the application
db.init_app(app)

# Routing the application's index page
@app.route('/')
def index():
    # Creating a response with a welcome message and status code 200 (OK)
    response = make_response(
        '<h1>Welcome to the pet/owner directory!</h1>',
        200
    )
    # Returning the response to the client
    return response

# Routing to a specific pet's information page
@app.route('/pets/<int:id>')
def pet_by_id(id):
    # Querying the database for a pet with the specified id
    pet = Pet.query.filter(Pet.id == id).first()

    # If the pet is not found in the database, return a 404 response
    if not pet:
        response_body = '<h1>404 pet not found</h1>'
        response = make_response(response_body, 404)
        return response
    
    # Building a response body with the pet's information
    response_body = f'''
        <h1>Information for {pet.name}</h1>
        <h2>Pet Species is {pet.species}</h2>
        <h2>Pet Owner is {pet.owner.name}</h2>
    '''

    # Creating a response with the response body and status code 200 (OK)
    response = make_response(response_body, 200)

    # Returning the response to the client
    return response

# Routing to a specific owner's information page
@app.route('/owner/<int:id>')
def owner_by_id(id):
    # Querying the database for an owner with the specified id
    owner = Owner.query.filter(Owner.id == id).first()

    # If the owner is not found in the database, return a 404 response
    if not owner:
        response_body = '<h1>404 owner not found</h1>'
        response = make_response(response_body, 404)
        return response
    
    # Building a response body with the owner's information
    response_body = f'<h1>Information for {owner.name}</h1>'

    # Querying the owner's pets from the database
    pets = [pet for pet in owner.pets]

    # If the owner has no pets, add a message to the response body
    if not pets:
        response_body += f'<h2>Has no pets at this time.</h2>'

    # Otherwise, add each pet's species and name to the response body
    else:
        for pet in pets:
            response_body += f'<h2>Has pet {pet.species} named {pet.name}.</h2>'

    # Creating a response with the response body and status code 200 (OK)
    response = make_response(response_body, 200)

    # Returning the response to the client
    return response

# Starting the application on port 5555 and enabling debug mode
if __name__ == '__main__':
    app.run(port=5555, debug=True)