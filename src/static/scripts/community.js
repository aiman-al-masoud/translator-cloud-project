const URL2 = "/query-db-api2";

/**
 * All mutable state from the session should go in here.
 * Changes go to state first, then UI is updated with {@link update} following state.
 */
const state = {
    fromText : '',
    to_text_possible : '',
    fid : '',
    timer : -1 // reference to (possibly existing) old timer to be cleared
}

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
async function sendQueryToDB2() {
    let request = {};
    request.from_text = state.fromText;
    request.to_text = state.to_text_possible;
    request.secondid = hashGenerator(request.from_text); //will be changed
    request.fid = state.fid;
  
  
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
      alert("Thank you for your help")
    }
}

/**
 * Updates the UI, to be called after {@link state} has been modified.
 */
 function update(){
    document.getElementById("fromText").value = state.fromText
    document.getElementById("to_text_possible").value = state.to_text_possible
    document.getElementById("fid").value = state.fid
}

document.getElementById("possible-translations-button").onclick=sendQueryToDB2;