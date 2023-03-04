from flask import Flask, request, jsonify;
from flask_cors import CORS;
from pymongo import MongoClient;
import datetime;

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

if __name__ == '__main__':
    app.run(debug=True)
