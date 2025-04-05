import requests  # pip install requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/generate", methods=["POST"])
def generate():
    name = request.form["name"]
    age = request.form["age"]
    mood = request.form["mood"]
    recovery = request.form["recovery"]
    equipment = request.form["equipment"]
    workout_type = request.form["workout_type"]
    duration = request.form["duration"]
    body_part = request.form["body_part"]

    #Call the API based on body part
    url = f"https://exercisedb.p.rapidapi.com/exercises/bodyPart/{body_part}"
    headers = {
        "x-rapidapi-key": "fe88645cffmsh4f548111d115addp1071f2jsn6ef27e71bcb4",
        "x-rapidapi-host": "exercisedb.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "❌ Failed to fetch exercises from API."

    exercises = response.json()

    
    matching_exercises = [ex for ex in exercises if ex["equipment"].lower() == equipment.lower()]

    
    if not matching_exercises:
        matching_exercises = exercises[:5]
    else:
        matching_exercises = matching_exercises[:5]

  
    result_html = f"<h2>Hi {name}!</h2><p>Here’s your {duration}-minute {workout_type} workout for {body_part}:</p><ul>"
    for ex in matching_exercises:
        result_html += f"<li>{ex['name'].title()} – Equipment: {ex['equipment']}</li>"
    result_html += "</ul>"

    return result_html

if __name__ == "__main__":
    app.run(debug=True, port=5050)