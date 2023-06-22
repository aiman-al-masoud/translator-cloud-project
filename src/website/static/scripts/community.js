import hashGenerator from "./utils/hash_generator.js";
import './utils/common.js';
//import { io } from "./utils/socket.io.esm.min.js"

const URLdb = "https://api.cloud-translator.com";
const URL2 = URLdb + "/insert-possible-better-translation";
const URL3 = URLdb + "/read-bad-translations";
const URL4 = URLdb + "/read-possible-better-translation-by-id";
const URL5 = URLdb + "/vote-possible-better-translation";

// const socket = io("ws://172.17.0.4:8080")
// const socket = io()

const fpPromise = import('https://openfpcdn.io/fingerprintjs/v3').then(FingerprintJS => FingerprintJS.load());
async function getFingerprint() {
  const fp = await fpPromise;
  const result = await fp.get();
  return result.visitorId;
}

const state = {
  badTranslations: [],
  possibleTranslations: {},
  openDetails: "", //id of the details which are being displayed
  page: 0,
  pagePossible: 0
}

function clearAll() {
  let bigList = document.getElementsByClassName("big-list")[0]
  bigList.innerHTML = "";
}

function createElementFromHTML(tag, html) {
  let element = document.createElement(tag)
  element.innerHTML = html
  return element
}

function update() {
  clearAll();
  let bigList = document.getElementsByClassName("big-list")[0]
  state.badTranslations.forEach(e => {
    let html = `
    <details id="${e['id']}" class="item">
      <summary onclick="loadPossibleTranslations('frontend', '${e['id']}')">
      <span class="complaints"><img src="static/res/emotion-sad-line-white.png" class="complaints-image">&nbsp&nbsp${e['complaints']}</span>
      <div> <strong>${e['from']}:</strong>
        <span id="fromText" class="fromText" name="fromText">${e['from_text']}</span><br>
        <strong>${e['to']}:</strong> ${e['to_text']}
      </div>
      </summary>
      <div>
        <div class="possible-translations-area">
          <textarea id="to_text_possible" class="to_text_possible" name="to_text_possible"></textarea>
          <button id="possible-translations-button" class="button" onclick="sendQueryToDB2('${e['id']}')">
          <img src="static/res/send-plane-2-fill.png" class="button-image">
          <img src="static/res/send-plane-2-fill-hover.png" class="button-hover-image">
          </button>
        </div>
      </div>
      <div id="inner-${e['id']}">
      </div>
      <button id="get-new-proposals" class="button get-new-proposals" onclick="showMoreBetterTranslations('${e['id']}')">
        <img src="static/res/arrow-down-fill.png" class="button-image">
        <img src="static/res/arrow-down-fill-hover.png" class="button-hover-image">
      </button>
    </details>
    `
    bigList.appendChild(createElementFromHTML('div', html))
  })
}

function checkOpenDetails(id) {
  if (!state.openDetails) {
    state.openDetails = id;
    state.pagePossible = 0;
    return false
  } else if (state.openDetails != id) {
    document.getElementById(state.openDetails).removeAttribute("open");
    state.possibleTranslations[state.openDetails] = []
    update();
    state.openDetails = id;
    state.pagePossible = 0;
    return false
  }

  return true

}

async function asyncCallForBetterTranslations(request) {
  try {
    var res = await fetch(URL4, {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    })
  } catch (error) {
    console.log(error);
  }
  let result = await res.json();
  let innerEl = document.getElementById(`inner-${state.openDetails}`)
  state.possibleTranslations[state.openDetails] = result

  let possibleTranslationsArray = (JSON.parse(state.possibleTranslations[state.openDetails]))

  possibleTranslationsArray.forEach(e => {
    let html = `<div class="possible-translation-el">
    <span class="left">${e['to_text']}</span>
      <span class="right-votes">
        <span id="votes-field-${e.id}">VOTES : ${e.votes}</span>
        <button id="votes-plus-button-${e['id']}" class="button votes-plus-button" onclick="likeToPossibleBetterTranslations('${e['id']}')">+</button>
      </span>
    </div>`
    innerEl.appendChild(createElementFromHTML('div', html))
  })

  if (Object.keys(result).length == 0) {
    document.getElementById(state.openDetails).getElementsByClassName("get-new-proposals")[0].style.display = "none";
    return ""
  }
}

/**
 * Update votes for a given better translation proposal
 * @param {integer} secondid of the better translation proposal
 */
async function likeToPossibleBetterTranslations(secondid) {
  let request = {};
  request.secondid = secondid;
  let operation;

  if (document.getElementById("votes-plus-button-" + secondid).classList.contains("pressed")) {
    operation = -1;
  } else {
    operation = 1;
  }

  request.operation = operation;
  request.fingerprint = await getFingerprint();


  try {
    let res = await fetch(URL5, {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    })
  } catch (error) {
    console.log(error);
  }
  finally {
    if (operation == 1)
      document.getElementById("votes-plus-button-" + secondid).classList.add("pressed");
    else document.getElementById("votes-plus-button-" + secondid).classList.remove("pressed")
    // TODO: show the votes, updated, to the user
  }
}

/**
 * Load the possible better translations for the given section
 * @param {string} source to show the possible better translations in any case, expect for when details are reduced
 * @param {int} id of the bad translation section
 * @returns
 */
function loadPossibleTranslations(source, id) {
  let detailsSection = document.getElementById(id)

  if (checkOpenDetails(id) && source == "frontend") return

  let request = {};
  request.id_prop = id;
  request.page = state.pagePossible;

  asyncCallForBetterTranslations(request)
}

function showMoreBetterTranslations(id) {
  let request = {};
  request.id_prop = state.openDetails;
  state.pagePossible += 1;
  request.page = state.pagePossible;

  asyncCallForBetterTranslations(request)
}

/**
 * write the possible better translations of a given bad translation section
 * @param {int} idTextarea of the bad translations
 */
async function sendQueryToDB2(idTextarea) {
  if (!document.getElementById(idTextarea).getElementsByClassName("to_text_possible")[0].value.trim()) {
    alert("Empty better translation")
    return ""
  }

  let request = {};
  request.from_text = document.getElementById(idTextarea).getElementsByClassName("fromText")[0].innerHTML;
  request.to_text = document.getElementById(idTextarea).getElementsByClassName("to_text_possible")[0].value;
  request.secondid = hashGenerator(request.from_text + request.to_text); //will be changed ?!
  request.fid = parseInt(idTextarea);
  request.fingerprint = await getFingerprint();


  try {
    let res = await fetch(URL2, {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    })
  } catch (error) {
    console.log(error); //Translation with this id is already under supervision
  }
  finally {
    alert("Thank you for your help, scroll down the suggestions to find yours");
    document.getElementById(idTextarea).getElementsByClassName("to_text_possible")[0].value = "";
    // add the display of the sent translation
  }
}

/**
 * Get (in the state) the list of the bad translations from the database
 * @returns
 */
async function getData() {
  try {
    var res = await fetch(URL3, { 
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ page: state.page })
    })
  } catch (error) {
    console.log(error);
  }
  state.page += 1;

  let result = await res.json();

  if (Object.keys(result).length == 0) {
    document.getElementById("get-new-data").style.visibility = "hidden";
    return ""
  }

  state.badTranslations = state.badTranslations.concat(result);
  update();
}

window.state = state;
window.onload = getData;
document.getElementById("get-new-data").onclick = getData;

window.sendQueryToDB2 = sendQueryToDB2; //do not remove
window.loadPossibleTranslations = loadPossibleTranslations; //do not remove
window.showMoreBetterTranslations = showMoreBetterTranslations; //do not remove
window.likeToPossibleBetterTranslations = likeToPossibleBetterTranslations; //do not remove

// socket.on('votes-update', data => {
  
//   console.log(data)
//   const dataObj = JSON.parse(data)
//   console.log(dataObj)

//   if (dataObj.fid == state.openDetails) {
//     document.getElementById("votes-field-" + dataObj.secondid).innerHTML = `VOTES : ${dataObj.votes}`;
//   }
// })
