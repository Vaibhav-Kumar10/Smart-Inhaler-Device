from flask import Blueprint, request, jsonify
from .models import db, User, SensorData, Prediction, Alert
from datetime import datetime

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
