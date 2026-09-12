from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import random
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": ["*"]}})

# Load trained ML model
model = joblib.load("cooked_model.pkl")


def get_trash_talk(sleep, assignments, exam_days,
                   attendance, backlogs, screen_time,
                   coffee, score):

    talks = []

    # Specific trash talks based on input

    if sleep < 4:
        talks.append("Bro's sleep schedule has officially stopped existing. 😭")

    elif sleep < 6:
        talks.append("Your pillow misses you more than your teachers do. 😴")

    if assignments >= 10:
        talks.append("Your assignments have formed their own government. 📚💀")

    elif assignments >= 5:
        talks.append("That assignment pile is becoming a historical monument. 🏛️")

    if exam_days <= 1:
        talks.append("Exam tomorrow and you came here for emotional damage. 💀")

    elif exam_days <= 3:
        talks.append("The exam is running toward you. You are standing still. 🔥")

    if attendance < 50:
        talks.append("At this point, you are not a student. You are a visitor. 🚪😂")

    elif attendance < 75:
        talks.append("Your attendance is playing hide and seek with the college. 📉")

    if backlogs >= 5:
        talks.append("Your backlogs have started multiplying like a group project. 💀")

    elif backlogs >= 2:
        talks.append("The backlog department recognizes your name. 😭")

    if screen_time >= 10:
        talks.append("Your phone has better attendance than you. 📱😂")

    elif screen_time >= 7:
        talks.append("Your screen time is working harder than you are. 📱🔥")

    if coffee >= 480:
        talks.append("Coffee is no longer a drink. It is your life support system. ☕😭")

    # Overall prediction trash talk

    if score <= 20:
        talks.append("😎 NOT COOKED. Somehow you escaped the academic fire.")

    elif score <= 40:
        talks.append("😅 Slightly toasted. There is still hope... barely.")

    elif score <= 60:
        talks.append("😰 You are getting cooked. Maybe open the textbook now.")

    elif score <= 80:
        talks.append("🔥 DEEP FRIED. Your syllabus is waiting with a weapon—metaphorically. 😭")

    else:
        talks.append("💀 ABSOLUTELY COOKED. Even your timetable has lost hope.")

    return random.choice(talks)


@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        sleep = float(data["sleep"])
        assignments = float(data["assignments"])
        exam_days = float(data["examDays"])
        attendance = float(data["attendance"])
        backlogs = float(data["backlogs"])
        screen_time = float(data["screenTime"])
        coffee = float(data["coffee"])


        # Your HTML asks number of coffees.
        # Dataset model uses coffee intake in mg.
        # Approximate 1 coffee = 80 mg.

        coffee_mg = coffee * 80


        # IMPORTANT:
        # Column names and order must match train_model.py

        input_data = pd.DataFrame([{
            "sleep_hours": sleep,
            "assignments_completed": assignments,
            "exam_days": exam_days,
            "attendance_percentage": attendance,
            "backlogs": backlogs,
            "phone_usage_hours": screen_time,
            "coffee_intake_mg": coffee_mg
        }])


        # ML Prediction
        prediction = model.predict(input_data)[0]

        score = round(max(0, min(100, prediction)))


        # Cooked level

        if score <= 20:
            level = "NOT COOKED"
            emoji = "😎"

        elif score <= 40:
            level = "SLIGHTLY TOASTED"
            emoji = "😅"

        elif score <= 60:
            level = "GETTING COOKED"
            emoji = "😰"

        elif score <= 80:
            level = "DEEP FRIED"
            emoji = "🔥"

        else:
            level = "ABSOLUTELY COOKED"
            emoji = "💀"


        survival = 100 - score


        # Generate trash talk
        trash_talk = get_trash_talk(
            sleep,
            assignments,
            exam_days,
            attendance,
            backlogs,
            screen_time,
            coffee_mg,
            score
        )


        # Send result to JavaScript

        return jsonify({
            "score": score,
            "level": level,
            "emoji": emoji,
            "survival": survival,
            "message": trash_talk
        })


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)