from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_grade(avg):
    if avg >= 90:
        return "A", "Outstanding performance! You've reached the top tier.", "EXCELLENT!"
    elif avg >= 70:
        return "B", "So close to an A! Keep pushing, you're doing wonderfully.", "AMAZING JOB!"
    elif avg >= 60:
        return "C", "Good effort! Keep improving steadily and you'll hit a B.", "GOOD WORK!"
    elif avg >= 50:
        return "D", "A passing grade! Let's aim higher next time, you can do it!", "KEEP PUSHING!"
    else:
        return "F", "Don't be discouraged. With more practice, you will improve!", "DON'T GIVE UP!"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/result', methods=['POST'])
def result():
    try:
        m1 = float(request.form["math"])
        m2 = float(request.form["science"])
        m3 = float(request.form["english"])

        avg = (m1 + m2 + m3) / 3
        grade, message, heading = calculate_grade(avg)

        return render_template("result.html", heading=heading, grade=grade, message=message)
    except ValueError:
        return "Please go back and enter valid numbers."

if __name__ == "__main__":
    app.run(debug=True)