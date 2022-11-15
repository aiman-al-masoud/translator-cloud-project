const URL2 = "/query-db-api2";

/**
 * Generating the hash of the input string enabling a cache mechanism for storing up to 100 input strings
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
    finally{
      alert("Thank you for your help");
      document.getElementById(idTextarea).getElementsByClassName("to_text_possible")[0].value="";
    }
}


