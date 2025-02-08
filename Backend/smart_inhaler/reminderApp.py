from flask import Flask, request, jsonify
from flask_cors import CORS
import schedule
import time
from threading import Thread
from plyer import notification

app = Flask(__name__)
CORS(app)

reminders = []  # List to store reminders
remind_me_state = False  # State to track if reminders are enabled


def send_notification(message):
    notification.notify(title="Reminder!", message=message, timeout=10)


# Schedule the reminders
def schedule_reminders():
    while True:
        if remind_me_state:
            schedule.run_pending()
        time.sleep(1)


# Endpoint to toggle "Remind Me"
@app.route("/toggle-remind-me", methods=["POST"])
def toggle_remind_me():
    global remind_me_state
    data = request.json
    remind_me_state = data.get("remindMe", False)
    return jsonify({"message": f"Remind Me set to {remind_me_state}."})


# Endpoint to add a new reminder
@app.route("/reminders", methods=["POST"])
def add_reminder():
    if not remind_me_state:
        return jsonify({"error": "Remind Me is disabled. Please enable it first."}), 400

    data = request.json
    time = data.get("time")
    message = data.get("message", "Reminder!")

    if time:
        reminders.append({"time": time, "message": message})
        schedule.every().day.at(time).do(send_notification, message)
        return jsonify({"message": "Reminder added successfully!"}), 201

    return jsonify({"error": "Invalid time"}), 400


# Endpoint to get all reminders
@app.route("/reminders", methods=["GET"])
def get_reminders():
    return jsonify(reminders)


if __name__ == "__main__":
    Thread(target=schedule_reminders, daemon=True).start()
    app.run(debug=True)
