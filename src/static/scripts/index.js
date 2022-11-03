url = "/translate-api";

async function send_text() {

  let request = {};
  request.from = document.getElementById('from').value.toLowerCase();
  request.to = document.getElementById('to').value.toLowerCase();
  request.from_text = document.getElementById('from_text').value;
  request.id = parseInt(1000000000 * Math.random())

  let res = await fetch(url, {
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
