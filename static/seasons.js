// Helpers shared by the home page and the season pages

// Season colours, from coolest (blue) to warmest (red). These reuse the colours
// of the weather events chart, so blue always means cold and red always means hot.
const GRADIENT = ["#2F5D73", "#6F97AE", "#8A9BA6", "#EEAA0D", "#B85A17", "#933708"];

// Text colour for each step: white on the dark colours, dark brown on the light ones
const TEXT_ON = ["#FFFFFF", "#2B1606", "#2B1606", "#2B1606", "#FFFFFF", "#FFFFFF"];

// Rank the seasons by mean max temperature and give each a colour:
// the coolest season gets the darkest blue, the warmest the deepest red.
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