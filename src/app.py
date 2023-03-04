from flask import Flask, request, jsonify;
from flask_cors import CORS;
from pymongo import MongoClient;
import datetime;
from bson.objectid import ObjectId;
app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb+srv://hamid:143Haadii@haadiidev.398eusj.mongodb.net/?retryWrites=true&w=majority')
print("Connected to MongoDB")

db = client['test']

@app.route('/api', methods=['GET'])
def get():
    return jsonify({'message': 'Hello World!'})

@app.route('/api/users', methods=['POST'])
def create_user():
    # check if user already exists
    existing_user = db.users.find_one({'email': request.json['email']})
    if existing_user:
      return jsonify({'message': 'User already exists!'}), 400
    else:
        db.users.insert_one({
            'name': request.json['name'],
            'email': request.json['email'],
            'password': request.json['password']
        })
        return jsonify({'message': 'User created successfully!'}), 201

@app.route('/api/users', methods=['GET'])
def get_users():
    users = []
    for doc in db.users.find():
        users.append({
            'id': str(doc['_id']),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })
    return jsonify({'users': users}), 200

# authorizing user

@app.route('/api/users/auth', methods=['POST'])
def auth_user():
    user = db.users.find_one({
        'email': request.json['email'],
        'password': request.json['password']
    })
    if user:
        
        token = jwt.encode({
            'id': str(user['_id']),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    else:
        return jsonify({'message': 'Invalid email or password!'})


@app.route('/api/mybikes', methods=['POST'])
def create_bike():
    # check if bike already exists
    existing_bike = db.bikes.find_one({'name': request.json['name']})
    if existing_bike:
      return jsonify({'message': 'Bike already exists!'}), 400
    else:
        db.bikes.insert_one({
            'name': request.json['name'],
            'bike_type': request.json['bike_type'],
            'images':  request.json['images'],
            'description': request.json['description'],
            'daily_rate': request.json['daily_rate'],
            'brand': request.json['brand'],
            'color': request.json['color'],
        })
        return jsonify({'message': 'Bike created successfully!'}), 201


@app.route('/api/mybikes', methods=['GET'])
def get_bikes():
    bikes = []
    for doc in db.bikes.find():
        bikes.append({
            'id': str(doc['_id']),
            'name': doc['name'],
            'bike_type': doc['bike_type'],
            'images': doc['images'],
            'description': doc['description'],
            'daily_rate': doc['daily_rate'],
            'brand': doc['brand'],
            'color': doc['color'],
        })
    return jsonify({'bikes': bikes}), 200

@app.route('/api/mybikes/<id>', methods=['GET'])
def get_bike(id):
    bike = db.bikes.find_one({'_id': ObjectId(id)})
    return jsonify({
        'id': str(bike['_id']),
        'name': bike['name'],
        'bike_type': bike['bike_type'],
        'images': bike['images'],
        'description': bike['description'],
        'daily_rate': bike['daily_rate'],
        'brand': bike['brand'],
        'color': bike['color'],
    })

# update bike
@app.route('/api/mybikes/<id>', methods=['PUT'])
def update_bike(id):
    db.bikes.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'bike_type': request.json['bike_type'],
        'images':  request.json['images'],
        'description': request.json['description'],
        'daily_rate': request.json['daily_rate'],
        'brand': request.json['brand'],
        'color': request.json['color'],
    }})
    return jsonify({'message': 'Bike updated successfully!'}), 200

# delete bike
@app.route('/api/mybikes/<id>', methods=['DELETE'])
def delete_bike(id):
    db.bikes.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'Bike deleted successfully!'}), 200

# create bike reservation from bike id
@app.route('/api/mybikes/<id>/reservations', methods=['POST'])
def create_bike_reservation(id):
    # check if bike already exists
    existing_bike = db.bikes.find_one({'_id': ObjectId(id)})
    if existing_bike:
        db.reservations.insert_one({
            'bike_id': id,
            'resevation_date': request.json['resevation_date'],
            'due_date': request.json['due_date'],
            'city': request.json['city'],
        })
        return jsonify({'message': 'Bike reservation created successfully!'}), 201
    else:
        return jsonify({'message': 'Bike does not exist!'}), 400


@app.route('/api/mybikes/reservations', methods=['GET'])

def get_bike_reservations():
    reservations = []
    for doc in db.reservations.find():
        reservations.append({
            'id': str(doc['_id']),
            # 'resevation_date': doc['resevation_date'],
            'due_date': doc['due_date'],
            'city': doc['city'],
        })
    return jsonify({'reservations': reservations}), 200


if __name__ == '__main__':
    app.run(debug=True)
