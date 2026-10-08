// Helpers shared by the home page and the season pages

// Season colours, from darkest (coolest) to lightest (warmest)
const GRADIENT = ["#933708", "#A95607", "#BE7505", "#D49504", "#EEAA0D", "#FFC40C"];

// Text colour for each step: white on the two dark colours, dark brown on the rest
const TEXT_ON = ["#FFFFFF", "#FFFFFF", "#2B1606", "#2B1606", "#2B1606", "#2B1606"];

// Rank the seasons by mean max temperature and give each a colour:
// the coolest season gets the darkest colour, the warmest the lightest.
function colourBySeason(summary) {
  const ranked = [...summary].sort((a, b) => a.mean_max_temp - b.mean_max_temp);
  const colours = {};
  ranked.forEach((row, i) => {
    colours[row.season] = { fill: GRADIENT[i], text: TEXT_ON[i] };
  });
  return colours;
}

// Show numbers with one decimal place, e.g. 31.0 rather than 31
function oneDecimal(value) {
  return value === null ? "–" : value.toFixed(1);
}

// Ask the Flask app for data; stop with an error if the request fails
function getJSON(url) {
  return fetch(url).then(response => {
    if (!response.ok) throw new Error(`Request failed: ${url}`);
    return response.json();
  });
}

// Font used in every chart
const CHART_FONT = { family: "Libre Franklin, Arial, sans-serif", color: "#3B2410" };