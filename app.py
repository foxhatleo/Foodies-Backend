import json
from db import db, Food
from flask import Flask

app = Flask(__name__)

db_filename = 'hackc.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)


with app.app_context():
    db.create_all()


def get_param(i):
    """ Get a field in the JSON request body.

    :param i: The name of the field.
    :return: The value of the field. If the field does not exist, or the
    value is not string, returns None.
    """
    try:
        req_body = json.loads(request.data)
        if not req_body or i not in req_body:
            return None
        return req_body[i]
    except json.decoder.JSONDecoder:
        return None


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/foods/', methods=['GET'])
def get_foods():
    foods = Food.query.all()
    r = {'success': True, 'data': [p.serialise() for p in foods]}
    return json.dumps(r), 200, {'ContentType': 'application/json'}


@app.route('/api/foods/', methods=['POST'])
def create_food():
    try:
        name = get_param('name')
        location = get_param('location')
        description = get_param('description')

        # If the request is a good one:
        if name is not None and location is not None and description is not None:
            food = Food(name, location, description)
            db.session.add(food)
            db.session.commit()

            return json.dumps({'success': True, 'data': food.serialise()}), 200, {'ContentType': 'application/json'}
        else:
            raise Exception()

    # If the request is bad, respond with 400.
    except:
        return json.dumps({'success': False}), 400,\
               {'ContentType': 'application/json'}


@app.route('/api/food/<int:class_id>/', methods=['GET'])
def get_food(food_id):
    found_food = Food.query.filter_by(id=food_id).first()
    if not found_food:
        return json.dumps({'success': False}), 404, \
               {'ContentType': 'application/json'}
    else:
        d = found_food.serialise()
        return json.dumps({'success': True, 'data': d}), 200, \
               {'ContentType': 'application/json'}


@app.route('/api/food/<int:food_id>/', methods=['DELETE'])
def delete_food(food_id):
    found_food = Food.query.filter_by(id=food_id).first()
    if not found_food:
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}
    else:
        d = found_food.serialise()
        db.session.delete(found_food)
        db.session.commit()
        return json.dumps({'success': True, 'data': d}), 200, \
               {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run()
