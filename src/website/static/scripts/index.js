import './utils/common.js';

import hashGenerator from "./utils/hash_generator.js";
const TRANSLATE = "https://api.cloud-translator.com/translate-api";
// const AVAILABLE_LANGS = "http://127.0.0.1:8081/get-available-langs";
const DB_QUERY = "https://api.cloud-translator.com/insert-bad-translation";

const TIMEOUT = 1000; // milliseconds to wait for request the translate to the server
const MAX_CACHE_SIZE = 100; //max number of cache entries in localStorage
const fpPromise = import('https://openfpcdn.io/fingerprintjs/v3').then(FingerprintJS => FingerprintJS.load());

async function getFingerprint() {
  const fp = await fpPromise;
  const result = await fp.get();
  return result.visitorId;
}

/**
 * All mutable state from the session should go in here.
 * Changes go to state first, then UI is updated with {@link update} following state.
 */
const state = {
  fromLangCode: 'it',
  toLangCode: 'en',
  fromText: '',
  toText: '',
  timer: -1, // reference to (possibly existing) old timer to be cleared
  complainButtonActive: false
}


function focusOnInput() {
  document.getElementById("from_text").focus();
}

async function sendText() {
  if (!state.fromText.trim()) return

  let request = {};
  request.from = state.fromLangCode;
  request.to = state.toLangCode;
  request.from_text = state.fromText;
  request.id = hashGenerator(request.from_text + request.to); //generating the hash of the input string AND THE OUTPUT LANGUAGE

  //clearing the localStorage of the browser to prevent hash collisions after caching 100 entries
  if (localStorage.length >= MAX_CACHE_SIZE) {
    localStorage.clear();
  }

  let cached = localStorage.getItem(request.id)

  if (cached) {
    state.toText = cached;
    state.complainButtonActive = true
    update()
    return
  }

  let res = await fetch(TRANSLATE, {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request)
  })

  if (!res.ok) {
    alert(await res.text())
    return
  }

  let json = await res.json()
  state.toText = json.to_text
  state.complainButtonActive = true
  localStorage.setItem(request.id, json.to_text)
  update()
}

//generation of the JSON file invoked in case of a bad translation
async function sendQueryToDB() {
  let request = {};
  request.from = state.fromLangCode;
  request.to = state.toLangCode;
  request.from_text = state.fromText;
  request.to_text = state.toText;
  request.id = hashGenerator(request.from_text + request.to); //will be changed
  request.fingerprint = await getFingerprint();

  try {
    let res = await fetch(DB_QUERY, {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    })
  } catch (error) {
    console.log(error); //Translation with this id is already under supervision
  }
  finally {
    alert("Thank you for your feedback")
    state.complainButtonActive = false
    update()
  }
}

/**
 * Switching both selected languages and textAreas
 */
function switchLang() {

  [state.fromLangCode, state.toLangCode] = [state.toLangCode, state.fromLangCode]; // semicol is important
  [state.fromText, state.toText] = [state.toText, state.fromText];

  update()
}

/**
 * Automatically translate text after users when the user stops typing after TIMEOUT seconds
 */
function sendTextDelayed() {
  document.getElementById('to_text').value = "...";
  clearTimeout(state.timer);
  state.timer = setTimeout(function () {
    sendText();
  }, TIMEOUT);
}

/**
 * Utters some text in a given language.
 * @param {string} languageCode
 * @param {string} text
 */
function speak(languageCode, text) {
  const speech = new SpeechSynthesisUtterance();
  speech.lang = languageCode
  speech.text = text
  window.speechSynthesis.cancel(); // TODO: maybe fixes chrome?
  window.speechSynthesis.speak(speech)
}

/**
 * Copy the translated text to clipboard
 */
function copyToClipboard() {
  let copyText = document.getElementById("to_text").value;
  navigator.clipboard.writeText(copyText);
}

/**
 * Paste text from clipboard
 */
async function pasteFromClipboard() {
  let pastedText = await navigator.clipboard.readText();
  state.fromText += pastedText;
  update();
  sendTextDelayed();
}

/**
 * Updates the UI, to be called after {@link state} has been modified.
 */
function update() {
  document.getElementById("to_text").value = state.toText
  document.getElementById("from_text").value = state.fromText
  document.querySelector(`select#to option[value="${state.toLangCode}"]`).selected = true;
  document.querySelector(`select#from option[value="${state.fromLangCode}"]`).selected = true;
  document.getElementById("button_query_to_db").disabled = !state.complainButtonActive
}

document.body.onload = focusOnInput; sendQueryToDB
document.getElementById("button_query_to_db").onclick = sendQueryToDB;
document.getElementById("translate").onclick = sendText;
document.getElementById("invert").onclick = switchLang;
document.getElementById("from_text").onkeyup = sendTextDelayed;
document.getElementById("button_copy_to").onclick = copyToClipboard;
document.getElementById("button_paste_from").onclick = pasteFromClipboard;
document.getElementById("button_speak_from").onclick = () => speak(state.fromLangCode, state.fromText)
document.getElementById("button_speak_to").onclick = () => speak(state.toLangCode, state.toText)

document.getElementById("from_text").oninput = () => {
  state.fromText = document.getElementById("from_text").value.toLowerCase();
}

document.getElementById("to_text").oninput = () => {
  state.toText = document.getElementById("to_text").value
}

document.getElementById("from").oninput = () => {
  state.fromLangCode = document.getElementById("from").value.toLowerCase();
}

document.getElementById("to").oninput = () => {
  state.toLangCode = document.getElementById("to").value.toLowerCase();
}

// (async () => {
//   const langs = await fetch(AVAILABLE_LANGS, {
//     method: 'GET',
//     headers: { 'Content-Type': 'application/json' }
//   })
//     .then(x => x.json())

//   Object.entries(langs).forEach(l => {
//     const option = document.createElement('option')
//     option.innerHTML = l[1]
//     option.value = l[0]
//     document.getElementById('from').appendChild(option)
//     document.getElementById('to').appendChild(option.cloneNode(true))
//   })
//   update()
// })()

