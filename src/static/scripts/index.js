URL = "/translate-api";
const MAX_CACHE_SIZE = 100; //max number of cache entries in localStorage

function focusOnInput() {
  document.getElementById("from_text").focus();
}

/**
 * generating the hash of the input string enabling a cache mechanism for storing up to 100 input strings
 *
 * @param {string} string
 * @returns {number}
 */
function hashGenerator(string) {
    var hash = 0, i, chr;
    if (string.length === 0) return hash;
    for (i = 0; i < string.length; i++) {
      chr = string.charCodeAt(i);
      hash = ((hash << 5) - hash) + chr;
      hash |= 0; // Convert to 32bit integer
    }
    return hash;
}

async function sendText() {
  let request = {};
  request.from = document.getElementById('from').value.toLowerCase();
  request.to = document.getElementById('to').value.toLowerCase();
  request.from_text = document.getElementById('from_text').value;
  request.id = hashGenerator(request.from_text); //generating the hash of the input string


  //clearing the localStorage of the browser to prevent hash collisions after caching 100 entries
  if(localStorage.length >= MAX_CACHE_SIZE){
    localStorage.clear();
  }
  let cached = localStorage.getItem(request.id)
  if(cached){
    document.getElementById('to_text').value = cached;
    return
  }


  let res = await fetch(URL, {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request)
  })

  if (!res.ok){
    alert(await res.text())
    return
  }

  let json = await res.json()

  document.getElementById('to_text').value = json.to_text

  localStorage.setItem(request.id, json.to_text)
}

//switching both selected languages and textAreas
function switchLang() {
  from = document.getElementById('from').value;
  to = document.getElementById('to').value;
  from_text = document.getElementById('from_text').value;
  to_text = document.getElementById('to_text').value;

  document.getElementById('from').value = to;
  document.getElementById('to').value = from;
  document.getElementById('from_text').value = '' + to_text;
  document.getElementById('to_text').value = '' + from_text;
}

var timeout = 1000; // milliseconds to wait for request the translate to the server
var timer;

function sendTextDelayed() {
  document.getElementById('to_text').value = "...";
  clearTimeout(timer);
  timer = setTimeout(function(){
    sendText();
  }, timeout);
}

console.log(document.getElementById("translate"));
document.getElementById("translate").onclick=sendText;
document.body.onload=focusOnInput;
document.getElementById("invert").onclick=switchLang;
document.getElementById("from_text").onkeyup=sendTextDelayed;
