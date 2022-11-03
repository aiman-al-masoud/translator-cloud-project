url = "/translate-api";

function send_text() {

  var request = new Object();
  request.from = document.getElementById('from').value.toLowerCase();
  request.to = document.getElementById('to').value.toLowerCase();
  request.from_text = document.getElementById('from_text').value;
  request.id = parseInt(1000000000 * Math.random())

  fetch(url, {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request)
  })

    .then( res => res.json()
    
    ).then(json => {
      document.getElementById('to_text').value = json.to_text
    })

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
