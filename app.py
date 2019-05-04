import json
from db import db, Food
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

db_filename = 'foodies.db'

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
        title = get_param('title')
        location = get_param('location')
        location_detail = get_param('location_detail')
        description = get_param('description')
        start_time = get_param('start_time')
        end_time = get_param('end_time')
        date = get_param('date')

        params = [title, location, location_detail, description, start_time, end_time, date]

        # If the request is a good one:
        if all(p is not None for p in params):
            start_time = datetime.strptime(start_time, "%H:%M").time()
            end_time = datetime.strptime(end_time, "%H:%M").time()
            date = datetime.strptime(date, "%m/%d/%y").date()
            food = Food(title=title, location=location, location_detail=location_detail,
                        description=description, start_time=start_time, end_time=end_time, date=date)
            db.session.add(food)
            db.session.commit()

            return json.dumps({'success': True, 'data': food.serialise()}), 200, {'ContentType': 'application/json'}
        else:
            raise Exception("params wrong, params: " + str(params))

    # If the request is bad, respond with 400.
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)}), 400,\
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
