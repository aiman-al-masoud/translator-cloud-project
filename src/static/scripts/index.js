URL = "/translate-api";
const MAX_CACHE_SIZE = 100;// max number of cache entries in localStorage

function focus_on_input() {
  document.getElementById("from_text").focus();
}

/**
 * 
 * @param {string} string 
 * @returns {number}
 */
function hash(string) {
    var hash = 0, i, chr;
    if (string.length === 0) return hash;
    for (i = 0; i < string.length; i++) {
      chr = string.charCodeAt(i);
      hash = ((hash << 5) - hash) + chr;
      hash |= 0; // Convert to 32bit integer
    }
    return hash;
}

async function send_text() {

  let request = {};
  request.from = document.getElementById('from').value.toLowerCase();
  request.to = document.getElementById('to').value.toLowerCase();
  request.from_text = document.getElementById('from_text').value;
  // request.id = parseInt(1000000000 * Math.random());

  request.id = hash(request.from_text);

  if(localStorage.length >= MAX_CACHE_SIZE){
    localStorage.clear();
  }

  let cached = localStorage.getItem(request.id)
  if(cached){
    document.getElementById('to_text').value = cached
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

function switch_lang() {
  from = document.getElementById('from').value;
  to = document.getElementById('to').value;
  from_text = document.getElementById('from_text').value;
  to_text = document.getElementById('to_text').value;

  document.getElementById('from').value = to;
  document.getElementById('to').value = from;
  document.getElementById('from_text').value = '' + to_text;
  document.getElementById('to_text').value = '' + from_text;
}
