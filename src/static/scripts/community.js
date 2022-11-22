import hashGenerator from "./utils/hash_generator.js";
import './utils/common.js';
const URL2 = "/query-db-api2";
const URL3 = "/query-db-api3";

const state = {
  badTranslations : [],
  possibleTranslations : {
    2139615360 : ['migliore traduzione 1', 'migliore traduzione 2', 'migliore traduzione 3']
  },
  page: 0
}

function clearAll(){
  let bigList = document.getElementsByClassName("big-list")[0]
  bigList.innerHTML = "";
}

function createElementFromHTML(tag, html){
  let element = document.createElement(tag)
  element.innerHTML = html
  return element
}

function update(){
  clearAll();
  let bigList = document.getElementsByClassName("big-list")[0]
  state.badTranslations.forEach(e => {
    let html = `
    <details id="${e[4]}" class="item">
      <summary onclick="loadPossibleTranslations('${e[4]}')">
      <span class="complaints"><i class="ri-emotion-sad-line"></i>&nbsp&nbsp${e[5]}</span>
      <div> <strong>${e[0]}:</strong>
        <span id="fromText" class="fromText" name="fromText">${e[2]}</span><br>
        <strong>${e[1]}:</strong> ${e[3]}
      </div>
      </summary>
      <div id="inner-${e[4]}">
        <div class="possible-translations-area">
          <textarea id="to_text_possible" class="to_text_possible" name="to_text_possible"></textarea>
          <button id="possible-translations-button" class="button" onclick="sendQueryToDB2('${e[4]}')">
            <i class="ri-send-plane-2-fill"></i>
          </button>
        </div>
      </div>
    </details>
    `
    bigList.appendChild(createElementFromHTML('div', html))
  })
}

function loadPossibleTranslations(id){
  let detailsSection = document.getElementById(id)
  if(detailsSection.hasAttribute("open")){
    return ""
  }

  let innerEl = document.getElementById(`inner-${id}`)

  state.possibleTranslations[id].forEach(e => {
    let html = `
      <div class="possible-translation-el"> ${e} </div>
    `
    innerEl.appendChild(createElementFromHTML('div', html))
  })
}

//generation of the JSON file invoked in case of a bad translation
async function sendQueryToDB2(idTextarea) {
  let request = {};
  request.from_text = document.getElementById(idTextarea).getElementsByClassName("fromText")[0].innerHTML;
  request.to_text = document.getElementById(idTextarea).getElementsByClassName("to_text_possible")[0].value;
  request.secondid = hashGenerator(request.to_text); //will be changed
  request.fid = parseInt(idTextarea);

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
    alert("Thank you for your help");
    document.getElementById(idTextarea).getElementsByClassName("to_text_possible")[0].value = "";
  }
}

window.sendQueryToDB2 = sendQueryToDB2 //do not remove this, because we call 'sendQueryToDB2' inline in HTML
window.loadPossibleTranslations = loadPossibleTranslations //do not remove this

async function getData() {
  try {
    var res = await fetch(URL3, {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({page : state.page})
    })
  } catch (error) {
    console.log(error);
  }
  state.page += 1;
  let result = await res.json();
  if(Object.keys( result ).length==0){
    document.getElementById("get-new-data").style.visibility = "hidden";
    return ""
  }
  state.badTranslations = state.badTranslations.concat(result);
  update();
}

window.state = state;

window.onload = getData;
document.getElementById("get-new-data").onclick = getData;