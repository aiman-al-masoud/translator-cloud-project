/**
 * Generating the hash of the input string enabling a cache mechanism for storing up to 100 input strings
 *
 * @param {string} string
 * @returns {number}
 */
export default function hashGenerator(string) {
    var hash = 0, i, chr;
    if (string.length === 0) return hash;
    for (i = 0; i < string.length; i++) {
      chr = string.charCodeAt(i);
      hash = ((hash << 5) - hash) + chr;
      hash |= 0; // Convert to 32bit integer
    }
    return hash;
}