// The round trip, from the browser's side.
// STEP A1 and A2 happen before this file loads (see app.py and index.html).
// STEP A6 to A8 run on the server, in app.py, between STEP A5 and A9.

// STEP A3: these lines run once, as soon as the page loads main.js.
// Find the three parts of the page this file needs.
const form = document.getElementById("quiz-form");
const guessBox = document.getElementById("guess");
const feedback = document.getElementById("feedback");

// Tell the browser to run sendGuess when the form is submitted.
// Nothing else happens until the person presses Check.
form.addEventListener("submit", sendGuess);

async function sendGuess(event) {
  // STEP A4: the person pressed Check, so sendGuess runs.
  event.preventDefault();   // stop the browser from loading a new page

  // STEP A5: send the guess to /check as JSON. Next: STEP A6 in app.py.
  // fetch sends a request to the server's /check address.
  // await pauses sendGuess until the server responds; response stores that reply.
  const response = await fetch("/check", {
    // POST means we are sending data to the server.
    method: "POST",
    // Tell the server that the request body contains JSON.
    headers: { "Content-Type": "application/json" },
    // Get the text in the guess box, put it in an object, and turn it into JSON text, e.g., {"guess":"hyper-text"}
    body: JSON.stringify({ guess: guessBox.value })
  });

  // STEP A9: the server answered, so sendGuess picks up here.
  // Read the server's answer.
  const data = await response.json();

  // STEP A10: put the answer on the page
  showFeedback(data);
}

function showFeedback(data) {
  // STEP A10: change the message text, and its color (right or wrong).
  feedback.textContent = data.message;
  feedback.className = data.correct ? "right" : "wrong";
}
