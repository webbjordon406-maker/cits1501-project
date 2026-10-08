# Nyoongar Seasons

An interactive web app that relates the six Nyoongar seasons of south-west Western Australia to a year of daily Perth weather observations.

- **Live app:** https://USERNAME.pythonanywhere.com
- **GitHub:** https://github.com/webbjordon406-maker/cits1501-project
- **Author:** Jordon Webb (CITS1501 project, completed individually)

## What the app does and who it's for

The Nyoongar calendar has six seasons, marked by changes in weather, flowering plants and animal behaviour rather than fixed dates. Most people in Perth know only the four European seasons. This app is for students, teachers, visitors and anyone curious about Nyoongar seasonal knowledge. It helps them see how each season relates to the weather they experience.

Users can:
- read about each of the six seasons and the calendar as a whole
- compare the seasons' temperature, rainfall, sunshine and humidity in a summary table
- see how often each season has hot days, extreme heat, cold nights, rain days and heavy rain
- open a page for each season showing its weather across the year
- enter a day's temperature and rainfall and find out **which season the day feels like**

## Screens

| Screen | Address | What it shows |
|---|---|---|
| Home | `/` | An introduction, a clickable season wheel, a summary table, a weather events chart, and the sources |
| Season (one per season) | `/season/<name>` | The season's description, a statistics table, and a year-long temperature and rainfall chart with the season shaded |
| Match a day | `/match` | A form where users enter a temperature and rainfall; shows the closest season and a chart of how close every season is |
| Error | any unknown address | A "page not found" message with a link back home |

## Installation

You need **Python 3.11 or newer**, because pandas 3 requires it.

1. Download the code:
   ```bash
   git clone https://github.com/webbjordon406-maker/cits1501-project.git
   cd cits1501-project
   ```
2. Install the libraries listed in `requirements.txt` (Flask, pandas and pytest).
   - macOS: `python3 -m pip install -r requirements.txt`
   - Windows: `py -m pip install -r requirements.txt`

## Running the app

1. Start the app from the project folder.
   - macOS: `python3 app.py`
   - Windows: `py app.py`
2. Open **http://127.0.0.1:5002** in a web browser.
3. To stop the app, press **Ctrl + C** in the terminal.

## How to use it

1. On the **home page**, read the introduction. Click any wedge of the season wheel, or a season name in the table, to open that season's page.
2. Hover over any chart to see exact values.
3. Use the **menu bar** at the top of every page to move between the home page, the six seasons and Match a day.
4. On **Match a day**:
   - Enter a maximum temperature (°C) and rainfall (mm), then click **Find the season**. You can also click one of the example buttons.
   - The result names the closest season and compares your day with that season's average day. Click the season name to open its page.
   - If an input is blank, isn't a number, or is outside the allowed range (0–50°C and 0–300 mm), the app explains what to fix instead of showing a result.

## Testing

### Automated tests

The project has 28 automated tests written with pytest. Run them from the project folder:

- macOS: `python3 -m pytest`
- Windows: `py -m pytest`

Add `-v` to see each test by name.

| File | Level | What it covers |
|---|---|---|
| `test_data.py` | Unit | The number of records, days per season, and day-first date reading |
| `test_analysis.py` | Unit | Summary values and event counts checked by hand against the CSV; edge cases (no data, lowercase season names, a threshold given as text); and the day matcher, including the input limits and invalid input (blanks, text, negative rain, a 60°C day) |
| `test_app.py` | Integration | Each route returns the right status code and data, including a 404 for an unknown season and a 400 for a missing input |

Two of the edge-case tests exposed real bugs, which were fixed in the code:
- `season_detail` rejected lowercase season names.
- `count_extreme_days` crashed when the threshold was text.

### Manual tests

**System test.** Run the app and work through the main user path:
1. The home page loads the wheel, the table and the events chart.
2. Clicking a wheel wedge opens that season's page with its table and year chart.
3. The menu bar works from every page.
4. On Match a day, 38°C with 0 mm gives Birak, and 16°C with 20 mm gives Makuru.
5. Entering 60°C, or leaving a box blank, shows an error message instead of a result.
6. Visiting `/season/Summer` shows the error page.

**Acceptance tests.** These check the app against its requirements:
- A user can find out which season is the wettest, from the summary table on the home page.
- A user can read about each of the six seasons, on the season pages.
- A user can find which season a given day is most like, on the Match a day page.
- Invalid input never crashes the app; the user is told what to fix.

## How it works

```
CITS1501 Data csv.csv ─┐
                       ├─> data.py ─> analysis.py ─> app.py ─────> browser pages
seasons.json ──────────┘   (load,     (summaries,     (page routes   (index, season, match,
                            clean,     event counts,   and JSON API)  error .html + seasons.js
                            seasons)   day matcher)                   + style.css + Plotly)
```

- **`data.py`** loads the BoM CSV, keeps the columns the app uses, reads dates in Australian day/month/year order, and gives each day a season. It also loads the season descriptions from `seasons.json` and checks that all six seasons are present.
- **`analysis.py`** calculates the season averages and totals, counts the days above or below weather thresholds, and contains the day matcher algorithm.
- **`app.py`** is the Flask backend. It loads the data once at startup, sends the HTML pages, and answers the JSON API routes that the pages call: `/api/summary`, `/api/season/<name>`, `/api/daily` and `/api/match`.
- **The pages** fetch data from the API and draw the tables and charts in the browser with Plotly.

### The day matcher algorithm

`closest_season()` in `analysis.py` finds the season whose average day is most like the user's day:

1. **Check the inputs.** Each must be present, a number, and within range (0–50°C, 0–300 mm). Otherwise it raises a `ValueError`, which the API returns as a 400 error with a clear message.
2. **Work out each season's average day:** its mean maximum temperature and mean daily rainfall.
3. **Scale the gaps.** Temperature and rain are in different units, so each gap is divided by that measure's standard deviation across the year. This stops temperature, which has bigger numbers, from deciding every match.
4. **Linear search.** For each of the six seasons, work out the distance `√(temperature gap² + rain gap²)` and keep the smallest. Seasons with no data are skipped, and on an exact tie the earlier season in the calendar wins.

## Data sources and licensing

**Weather data:** Bureau of Meteorology, [Daily Weather Observations for Perth, Western Australia](https://www.bom.gov.au/climate/dwo/IDCJDW6111.latest.shtml) (product IDCJDW6111), October 2025 to September 2026. This is 365 daily records, downloaded as monthly CSV files and combined into `CITS1501 Data csv.csv`.
- Temperature, rainfall and 3pm humidity are from Perth Metro (station 009225).
- Sunshine is from Perth Airport M.O. (station 009021).
- © Commonwealth of Australia, Bureau of Meteorology. Used for non-commercial educational purposes under the [Bureau's copyright terms](https://www.bom.gov.au/copyright).

**Season information:** [Nyoongar calendar](https://www.bom.gov.au/resources/indigenous-weather-knowledge/indigenous-seasonal-calendars/nyoongar-calendar), Indigenous Weather Knowledge, Bureau of Meteorology. This knowledge belongs to the Nyoongar communities who shared it, the Bureau of Meteorology, and Monash University's Centre for Australian Indigenous Studies. It is summarised in my own words in `seasons.json` for non-commercial study under fair dealing. No cultural content was generated by AI.

**Data preparation:**
- Only the six columns the app uses are kept.
- Dates are read as day/month/year.
- Missing values (one maximum temperature and one sunshine value) are left out of averages and counts rather than treated as zero.

## Security and privacy

- The app collects and stores **no personal information**: there are no accounts, forms that save data, or cookies. A notice on the home page tells users this.
- **No passwords or API keys** are used or committed.
- **All user input is checked on the server.** Invalid requests get a clear error message, not a crash.
- **Debug mode is off,** so error pages don't reveal the code.
- **Every route only reads data;** none can change or delete it.
- **Dependency versions are pinned** in `requirements.txt` to the versions that were tested.

## Deployment

The app is hosted on [PythonAnywhere](https://www.pythonanywhere.com), which runs Flask through a WSGI configuration file. To update the live site:

1. Run the tests locally, and only continue if they all pass.
2. Commit and push the changes to GitHub.
3. In a PythonAnywhere Bash console, run `cd ~/cits1501-project && git pull`.
4. Click **Reload** on the PythonAnywhere Web tab.

## Limitations

- Each season is matched to two calendar months so the data can be grouped. Real Nyoongar seasons are marked by changes in the environment, not by dates, so the boundaries are approximate.
- The data covers one year from two Perth weather stations. It may not represent other years or other parts of the Nyoongar region.
- The day matcher only uses temperature and rainfall, so its result is a rough guide to which season a day resembles.

## Use of AI

AI tools were used during development. Each significant use, including how the output was checked, changed or rejected, is recorded in [AI-LOG.md](AI-LOG.md).
