# Multi-Modal Route Optimization with Hybrid Travel

**Jordan Clifford** - ASU Student 

Visiting UNLV for the Smart Cities 2025 REU Program (June 2025 - August 2025)
Under the guidance of Professor Grzegorz Chmaj & Professor Henry Salvaraj

**[Visit the UNLV Smart Cities Site here](https://smartcities.sites.unlv.edu/)**

This REU project tackles multi-modal routing through a dense, walkable, transit-friendly city environment, Seattle was chosen as the target city. A machine learning model predicts travel time across four transport modes (driving, transit, bicycling, walking) and scores routes based on time and emissions to recommend the optimal mode per leg.

See the final poster (`JordanClifford_REU2025_POSTER.pdf`) for a broad overview of the project.

---

## Live Demo

**[Try the app here](https://multi-modal-routing-unlv-smartcities.streamlit.app/)** — no setup required.

---

## Running the App (Streamlit)

### 1. Clone the repo
```bash
git clone https://github.com/your-username/Multi-Modal-Route-Optimization-with-Hybrid-Travel.git
cd Multi-Modal-Route-Optimization-with-Hybrid-Travel
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r model/requirements.txt
```

### 4. Run the app
```bash
cd model
python -m streamlit run streamlit_app.py
```

Then open the localhost server (example: `http://localhost:8501`) in your browser.

> **Note:** The model was trained on Seattle, WA route data. Predictions are most accurate for Seattle-area inputs. Try addresses like `"Space Needle, Seattle"` or `"Pike Place Market, Seattle"` to get started.

---

## Input Modes

The app supports three ways to define a route (A → B → C):

| Mode | Description |
|------|-------------|
| **Address** | Type place names — geocoded automatically, no coordinates needed |
| **Distance** | Enter distances in km or miles per leg directly |
| **Coordinates** | Raw `lat, lng` pairs for precise control |

---

## Overview

Most routing software (Google Maps, Waze) optimizes for a single transport mode and ignores trade-offs between travel time and environmental impact. This project builds a **hybrid multimodal routing framework** that recommends the best transport mode (or mix of modes) for each leg of a journey, balancing both speed and emissions.

---

## Dataset

- **24,752 real-world routes** collected across the Seattle metro area via the Google Maps API
- Collected hourly from **6 AM to 10 PM over one week (August 2025)**
- Covers four modes: driving, transit, bicycling, and walking
- Features per route: origin/destination coordinates, mode, distance (m), duration (s), duration in traffic (driving only), and timestamp

---

## How It Works

### 1. Travel Time Prediction — Random Forest Regression
A Random Forest regressor was trained to predict travel time given a route's distance, mode, and time-of-day features. It was evaluated on a held-out test set of 10 routes (80/20 split).

| Mode | Relative Error |
|------|---------------|
| Driving | −6.5% (underprediction) |
| Transit | +19.7% |
| Bicycling | +29.9% |
| Walking | +41.8% |

Driving performed best due to higher hour-to-hour variability from the `duration_in_traffic` field. Bicycling and walking are time-invariant in the API, limiting data diversity.

### 2. Mode Selection — Multi-Objective Cost Function
Routes are scored using a cost function that balances predicted travel time and CO₂ emissions, with penalty terms that activate when either exceeds acceptable thresholds:

- **Thresholds:** T = 1,800 s, E = 1,000 g CO₂
- **Weights:** time (a = 15), emissions (b = 2.5), penalties (α = 0.04, β = 0.015)
- The mode with the lowest score wins for each leg

### 3. Reinforcement Learning — Q-Learning (Explored, Not Final)
Q-learning was explored as an alternative decision engine but showed a strong bias toward driving (78.15% of selections) regardless of reward tuning. The cost function was adopted instead for its direct, interpretable control over the time–emissions trade-off.

---

## Key Results

Tested across 43 routes and 20,468 data rows, the cost function produced **5,117 mode recommendations**:

| Mode | Wins |
|------|------|
| Driving | 2,876 (56.2%) |
| Bicycling | 1,873 (36.6%) |
| Transit | 368 (7.2%) |
| Walking | — |

Compared to Q-learning's 78.15% driving rate, the cost function meaningfully diversified mode selection toward bicycling — demonstrating that explicit emission weighting can shift recommendations toward more sustainable options without significantly increasing travel time.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Data collection | Python, Google Maps API |
| ML model | scikit-learn (Random Forest) |
| Web app | Streamlit |
| Geocoding | geopy (Nominatim) |
| Data processing | pandas |

---

## Project Structure

| Folder | Description |
|--------|-------------|
| `model/` | Trained ML model, Streamlit app, and Flask app |
| `abcs_routes/` | Final selected routes used to train the model |
| `colab_notebooks/` | Early synthetic data experiments and ML notebooks |
| `google_maps_api_scripts/` | Scripts used to collect real-world route durations via Google Maps API |
| `real_life_data/` | Points of interest used to build the route network, to be expanded upon in abcs_routes folder |
| `papers_to_cite/` | Research papers referenced during the project |
