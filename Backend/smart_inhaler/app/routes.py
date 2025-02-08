from flask import Blueprint, request, jsonify
from .models import db, User, SensorData, Prediction, Alert
from datetime import datetime
import requests

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET'])
def home():
    return {'message': 'Welcome to the Smart Inhaler API!'}

@routes.route('/upload-sensor-data', methods=['POST'])
def upload_sensor_data():
    data = request.json
    new_data = SensorData(
        user_id=data['user_id'],
        timestamp=datetime.now(),
        air_quality=data['air_quality'],
        humidity=data['humidity'],
        device_status=data['device_status']
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'message': 'Sensor data uploaded successfully'}), 201

@routes.route('/get-user-data/<int:user_id>', methods=['GET'])
def get_user_data(user_id):
    user_data = SensorData.query.filter_by(user_id=user_id).all()
    data = [{'timestamp': d.timestamp, 'air_quality': d.air_quality, 'humidity': d.humidity} for d in user_data]
    return jsonify({'user_data': data})

@routes.route('/get-alerts/<int:user_id>', methods=['GET'])
def get_alerts(user_id):
    alerts = Alert.query.filter_by(user_id=user_id).all()
    alert_data = [{'message': a.message, 'timestamp': a.timestamp} for a in alerts]
    return jsonify({'alerts': alert_data})

@routes.route('/register-user', methods=['POST'])
def register_user():
    data = request.json

    # Check if email or phone already exists
    existing_user = User.query.filter((User.email == data['email']) | (User.phone_no == data['phone_no'])).first()
    if existing_user:
        return jsonify({'error': 'User with this email or phone already exists'}), 400

    # Create new user
    new_user = User(
        name=data['name'],
        email=data['email'],
        phone_no=data['phone_no'],
        emergency_contact=data['emergency_contact'],  # New Field
        password=data['password'],  # Store as hashed in production
        gender=data['gender'],
        age=data['age'],
        height=data['height'],
        weight=data['weight'],
        medical_history=data.get('medical_history', '')  # Optional
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'user_id': new_user.id}), 201

@routes.route('/get-user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'phone_no': user.phone_no,
        'emergency_contact': user.emergency_contact,  # New Field
        'gender': user.gender,
        'age': user.age,
        'height': user.height,
        'weight': user.weight,
        'medical_history': user.medical_history
    }

    return jsonify(user_data)
# Your Fast2SMS API Key (Replace with your actual key)
FAST2SMS_API_KEY = "5UCYFaQwO4KNzqnoMG9pTP7tx6sy1DI8bAgWXrBHdjvhci0Sufjo5BX3KlM2zQfP76n8yZUCIwmAW0pT"

@routes.route('/send-sos', methods=['POST'])
def send_sos():
    data = request.json
    user_id = data.get('user_id')

    # Fetch user details
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    emergency_contact = user.emergency_contact  # Fetch stored emergency number

    # Message to be sent
    sos_message = f"🚨 SOS ALERT! {user.name} needs help. Contact: {user.phone_no}."

    # Sending SMS via Fast2SMS
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "route": "v3",
        "sender_id": "TXTIND",
        "message": sos_message,
        "language": "english",
        "flash": 0,
        "numbers": emergency_contact
    }
    headers = {
        'authorization': FAST2SMS_API_KEY,
        'Content-Type': "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    result = response.json()

    # Check if SMS was sent successfully
    if result.get('return') == True:
        return jsonify({'message': 'SOS alert sent successfully!', 'response': result}), 200
    else:
        return jsonify({'error': 'Failed to send SOS alert', 'response': result}), 500