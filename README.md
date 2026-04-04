# Multi-Modal Route Optimization with Hybrid Travel

**Jordan Clifford** — ASU Student  
Visiting UNLV for the Smart Cities 2025 REU Program  
Under the guidance of Professor Grzegorz Chmaj & Professor Henry Salvaraj

This REU project tackles multi-modal routing through a dense, walkable, transit-friendly city environment — Seattle was chosen as the target city. A machine learning model predicts travel time across four transport modes (driving, transit, bicycling, walking) and scores routes based on time and emissions to recommend the optimal mode per leg.

See the final poster (`JordanClifford_REU2025_POSTER.pdf`) for a broad overview of the project.

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
pip install streamlit pandas scikit-learn geopy joblib
```

### 4. Run the app
```bash
cd model
python -m streamlit run streamlit_app.py
```

Then open `http://localhost:8501` in your browser.

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

## Project Structure

| Folder | Description |
|--------|-------------|
| `model/` | Trained ML model, Streamlit app, and Flask app |
| `abcs_routes/` | Final selected routes used to train the model |
| `colab_notebooks/` | Early synthetic data experiments and ML notebooks |
| `google_maps_api_scripts/` | Scripts used to collect real-world route durations via Google Maps API |
| `real_life_data/` | Points of interest used to build the route network |
| `papers_to_cite/` | Research papers referenced during the project |
