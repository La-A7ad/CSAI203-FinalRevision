from flask import Flask, render_template, request, jsonify
import json
import os
import random

app = Flask(__name__)


def load_lecture_data(lecture_id):
    filepath = os.path.join("data", f"{lecture_id}.json")
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return json.load(file)
    return None


@app.route("/")
def index():
    lectures = [
        {
            "lecture_id": "lecture1",
            "lecture_title": "Introduction to Software Products",
        },
        {"lecture_id": "lecture2", "lecture_title": "Web Basics"},
        {"lecture_id": "lecture3", "lecture_title": "Requirements and Design"},
        {"lecture_id": "lecture4-a", "lecture_title": "Waterfall and Agile"},
        {"lecture_id": "lecture4-b", "lecture_title": "Scrum"},
        {"lecture_id": "lecture5", "lecture_title": "Software Architecture Overview"},
        {"lecture_id": "lecture6", "lecture_title": "Cloud-Based Software"},
        {"lecture_id": "lecture7", "lecture_title": "Microservices"},
    ]
    return render_template("index.html", lectures=lectures)


@app.route("/lecture/<lecture_id>")
def show_lecture(lecture_id):
    lecture_data = load_lecture_data(lecture_id)
    if not lecture_data:
        return "Lecture not found", 404

    return render_template("lecture.html", lecture_data=lecture_data)


@app.route("/check-mcq", methods=["POST"])
def check_mcq():
    data = request.json
    lecture_id = data.get("lecture_id")
    question_id = data.get("question_id")
    selected_options = data.get("selected_options", [])

    if not lecture_id or question_id is None or not isinstance(selected_options, list):
        return jsonify({"error": "Invalid input data"}), 400

    lecture_data = load_lecture_data(lecture_id)
    if not lecture_data:
        return jsonify({"error": "Lecture not found"}), 404

    for question in lecture_data["mcqs"]:
        if question["id"] == question_id:
            correct_options = [
                i
                for i, option in enumerate(question["options"])
                if option["is_correct"]
            ]
            if set(selected_options) == set(correct_options):
                return jsonify({"correct": True, "message": "Correct!"})
            else:
                return jsonify({"correct": False, "message": "Incorrect. Try again."})
    return jsonify({"error": "Question not found"}), 404


# Replace the check_tf route with:


@app.route("/check-tf", methods=["POST"])
def check_tf():
    data = request.json
    lecture_id = data.get("lecture_id")
    question_id = data.get("question_id")
    selected_value = data.get("selected_value")

    # Validate input
    if not all([lecture_id, question_id is not None, isinstance(selected_value, bool)]):
        return jsonify({"correct": False, "message": "Invalid input data"}), 400

    lecture_data = load_lecture_data(lecture_id)
    if not lecture_data:
        return jsonify({"correct": False, "message": "Lecture not found"}), 404

    # Find and check the question
    for question in lecture_data["true_false_questions"]:
        if question["id"] == question_id:
            is_correct = question["is_true"] == selected_value
            return jsonify(
                {
                    "correct": is_correct,
                    "message": "Correct!" if is_correct else "Incorrect. Try again.",
                }
            )

    return jsonify({"correct": False, "message": "Question not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
