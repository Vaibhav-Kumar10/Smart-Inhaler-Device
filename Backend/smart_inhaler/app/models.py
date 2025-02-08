from . import db

class User(db.Model):
    __tablename__ = 'user'  # Ensures consistent table naming

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_no = db.Column(db.String(15), unique=True, nullable=False)
    emergency_contact = db.Column(db.String(15), nullable=False)  # Emergency SOS Contact
    password = db.Column(db.String(255), nullable=False)  # Store hashed in production
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)  # Height in cm
    weight = db.Column(db.Float, nullable=False)  # Weight in kg
    medical_history = db.Column(db.Text)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    air_quality = db.Column(db.Integer, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    device_status = db.Column(db.String(50), nullable=False)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    risk_level = db.Column(db.String(50), nullable=False)
    recommendation = db.Column(db.Text)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

