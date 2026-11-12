# Round Trip Demo

EME 6209, Module 5 (Client-Server Communication).

This is the smallest example I could write of the Module 5 requirement for the Culminating Project. The browser sends data to a server you wrote. The server reads it and sends something back. The page uses what comes back.

The app asks one question: what does HTML stand for? You type a guess. The server checks it and sends back a message. The answer lives in `app.py`, so nobody can find it with View Source. That is a reason to use a server, not just a way to meet a requirement.

The same question runs two ways, so you can compare them:

| | Version A: fetch | Version B: form POST |
|---|---|---|
| Address | http://127.0.0.1:5001/ | http://127.0.0.1:5001/form |
| Sends the data | `main.js` calls `fetch()` | the HTML form, when you press Check |
| Server route | `/check` | `/form` |
| Server sends back | a small piece of JSON | a whole new HTML page |
| The page | stays put and changes one line | reloads |
| Covered in | Module 5 videos, Live 5 | Live 4 (Bit Flip) |

Either one meets the requirement. Pick the one that fits your project.

## What you need

- Python 3.10 or newer
- PyCharm

## Set up in PyCharm

1. Copy the `round-trip-demo` folder somewhere on your computer that is **not** inside Google Drive, OneDrive, or iCloud. PyCharm makes a virtual environment with thousands of small files, and a sync service slows that down.
2. Open PyCharm. Choose **Open**, then pick the `round-trip-demo` folder.
3. If PyCharm asks about an interpreter, create a new virtual environment for this project. If it does not ask, go to Settings, then Project, then Python Interpreter, then Add Interpreter, and add a local virtual environment.
4. Open the Terminal tab at the bottom of PyCharm and type:

   ```
   pip install -r requirements.txt
   ```

5. Open `app.py` and click Run Python File (the triangle at the top right).
6. Open http://127.0.0.1:5001 in your browser.

Press the red square in PyCharm to stop the server.

## Follow the trip

I marked each step in the code with a comment, in the order it runs. Search for `STEP` to find them. The steps jump between files, because the browser and the server take turns.

**Before anything else**

| Step | Where | What happens |
|---|---|---|
| 0 | `app.py`, last lines | `app.run()` starts the server, and it waits |

**Version A: fetch**

| Step | Where | What happens |
|---|---|---|
| A1 | `app.py`, `home()` | the browser asks for `/`, and the server sends `index.html` |
| A2 | `templates/index.html` | the browser draws the page, then loads `main.js` |
| A3 | `static/js/main.js`, top | finds the form, the box, and the message area, and waits for Check |
| A4 | `static/js/main.js`, `sendGuess()` | the person presses Check, and `preventDefault()` stops a page reload |
| A5 | `static/js/main.js`, `sendGuess()` | `fetch()` sends `{"guess": "..."}` to `/check` |
| A6 | `app.py`, `check()` | `request.get_json()` reads the guess |
| A7 | `app.py`, `check()` and `judge()` | `judge()` decides right or wrong and writes a message |
| A8 | `app.py`, `check()` | `jsonify()` sends back `correct` and `message` |
| A9 | `static/js/main.js`, `sendGuess()` | `response.json()` reads the server's answer |
| A10 | `static/js/main.js`, `showFeedback()` | the message appears on the page |

**Version B: form POST**

| Step | Where | What happens |
|---|---|---|
| B1 | `app.py`, `form_version()` | the browser asks for `/form`, and the variables start empty |
| B2 | `app.py`, `form_version()` | `render_template()` sends the page with an empty box |
| B3 | `templates/form.html` | the person presses Check, and the form sends `guess` to `/form` |
| B4 | `app.py`, `form_version()` | the same function runs again, and the variables start empty again |
| B5 | `app.py`, `form_version()` | `request.form["guess"]` reads the guess |
| B6 | `app.py`, `form_version()` and `judge()` | `judge()` decides right or wrong and writes a message |
| B7 | `app.py`, `form_version()` | `render_template()` builds a new page with the message in it |
| B8 | `templates/form.html` | Jinja shows `{{ message }}` on the new page |

Both versions call the same `judge()` function. Only the way the data travels is different.

## See it in the browser

This is how I show the round trip in the video walkthrough, and you can do the same in yours.

1. Open Version A. Right-click the page, choose Inspect, and open the **Network** tab.
2. Type a wrong guess and press Check.
3. Click the `check` row. **Payload** shows what the browser sent. **Response** shows what the server sent back.
4. Look at the PyCharm Run window. The server printed a line for that same `POST /check` request.
5. Now open Version B and do it again. This time the Network tab shows a whole page coming back, not JSON.

## Want jQuery instead of fetch?

The Module 5 videos and Live 5 used jQuery's `$.ajax`. Both do the same job. This is STEP A5 and STEP A9 in jQuery:

```js
$.ajax({
  url: "/check",
  type: "POST",
  contentType: "application/json",
  data: JSON.stringify({ guess: $("#guess").val() }),
  success: showFeedback
});
```

jQuery has to be loaded on the page first, with a `<script>` tag that points to it. `fetch()` is built into every modern browser, so it needs nothing extra.
