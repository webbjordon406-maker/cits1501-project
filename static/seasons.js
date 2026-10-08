// Shared helpers used by both the home page and the season pages

const GRADIENT = ["#933708", "#A95607", "#BE7505", "#D49504", "#EEAA0D", "#FFC40C"];
// The two darkest steps need white text; the rest read better with dark text
const TEXT_ON = ["#FFFFFF", "#FFFFFF", "#2B1606", "#2B1606", "#2B1606", "#2B1606"];

// Give each season a gradient step by its mean max temperature:
// the coolest season gets the darkest colour, the warmest the lightest.
function colourBySeason(summary) {
  const ranked = [...summary].sort((a, b) => a.mean_max_temp - b.mean_max_temp);
  const colours = {};
  ranked.forEach((row, i) => {
    colours[row.season] = { fill: GRADIENT[i], text: TEXT_ON[i] };
  });
  return colours;
}

// Always show one decimal place, e.g. 31.0 rather than 31
function oneDecimal(value) {
  return value === null || value === undefined ? "–" : Number(value).toFixed(1);
}

// Fetch JSON, and throw an error if the server says something went wrong
function getJSON(url) {
  return fetch(url).then(response => {
    if (!response.ok) throw new Error(`Request failed: ${url}`);
    return response.json();
  });
}

// Shared font and colour settings for Plotly charts
const CHART_FONT = { family: "Libre Franklin, Arial, sans-serif", color: "#3B2410" };