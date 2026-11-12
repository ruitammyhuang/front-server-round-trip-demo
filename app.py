"""
A minimal round trip for EME 6209.

The browser sends data to this server. The server reads it, decides
something, and sends an answer back. The page uses that answer.

To run it: open this file, then click Run Python File
(the triangle at the top right of PyCharm).
Then open http://127.0.0.1:5001 in your browser.

How to follow the STEP comments:
Python reads this file from top to bottom. The import, app, ANSWER,
and every def block only get things ready. Nothing runs for a browser
until STEP 0 at the bottom starts the server.
Version A (fetch) runs STEP A1 to A10. Version B (form POST) runs STEP B1 to B8.
The steps jump between app.py, the templates, and main.js, in the order they run.
"""

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# The answer lives on the server. A player cannot find it with View Source.
ANSWER = "hypertext markup language"


def judge(guess):
    """Decide if a guess is right, and write the message the player sees."""
    # This runs at STEP A7 (Version A) and at STEP B6 (Version B).
    guess = guess.strip().lower()
    if guess == "":
        return False, "Type an answer first."
    if guess == ANSWER:
        return True, "Correct. HTML stands for HyperText Markup Language."
    return False, f'"{guess}" is not it. Hint: the H stands for HyperText.'


# ---------- The page ----------

@app.route("/")
def home():
    # STEP A1: the browser asks for "/" (a normal GET request).
    # The server sends back the HTML page. Next: STEP A2 in index.html.
    return render_template("index.html")


# ---------- Version A: fetch ----------

@app.route("/check", methods=["POST"])
def check():
    # STEP A6: fetch() in main.js sent a POST to /check, so this function runs.
    # Read what the browser sent.
    data = request.get_json()
    # STEP A7: make the judgement and store results
    # judge() gives back two things: right or wrong, and a message
    # notice the function judge() is defined above, and it has two return values in two different variable types:
    # a Boolean (True or False) and a string
    correct, message = judge(data["guess"])
    # STEP A8: send an answer back. Next: STEP A9 in main.js.
    return jsonify({"correct": correct, "message": message})


# ---------- Version B: a plain form POST ----------

@app.route("/form", methods=["GET", "POST"])
def form_version():
    # This function runs twice in Version B:
    # STEP B1, when the browser first asks for /form (a GET request)
    # STEP B4, when the person presses Check (a POST request)

    # STEP B1 and B4: start with empty values. These are what the page shows
    # the first time someone visits, before they press Check.
    guess = ""
    correct = False
    message = ""
    # The above variable declaration and initiation can be combined into one line
    # guess, correct, message = "", False, ""

    # A POST method is when a person pressed Check and sent the form.
    if request.method == "POST":
        # STEP B5: read what the browser sent
        guess = request.form["guess"]
        # STEP B6: make the judgement and store results
        correct, message = judge(guess)

    # STEP B2 (first visit): send back the page with an empty box and no message.
    # Next: STEP B3 in form.html.
    # STEP B7 (after Check): send back a whole new page with the message in it.
    # Next: STEP B8 in form.html.
    return render_template("form.html", guess=guess, correct=correct, message=message)


if __name__ == "__main__":
    # STEP 0: this runs first, when you click Run Python File.
    # It starts the server, which then waits for the browser to ask for a page.
    # Port 5001, because macOS uses 5000 for AirPlay.
    # In GitHub Codespaces, change host to "0.0.0.0".
    app.run(host="127.0.0.1", port=5001, debug=True)
