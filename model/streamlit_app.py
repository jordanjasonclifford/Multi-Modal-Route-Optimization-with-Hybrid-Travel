import streamlit as st
import joblib
import pandas as pd
from pathlib import Path
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Modal Route Optimizer",
    page_icon="🗺️",
    layout="centered",
)

# ── Load model ─────────────────────────────────────────────────────────────────
BASE = Path(__file__).parent

@st.cache_resource
def load_model():
    m = joblib.load(BASE / "travel_time_model.pkl")
    cols = joblib.load(BASE / "model_columns.pkl")
    return m, cols

model, model_columns = load_model()

# ── Constants ──────────────────────────────────────────────────────────────────
EMISSION_FACTORS = {"driving": 0.192, "transit": 0.105, "bicycling": 0.0, "walking": 0.0}
MODE_ICONS       = {"driving": "🚗", "transit": "🚌", "bicycling": "🚴", "walking": "🚶"}
DAYS             = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SEATTLE_CENTER   = (47.6062, -122.3321)   # fallback reference for distance-only mode

# ── Geocoder ───────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def geocode(address: str):
    geolocator = Nominatim(user_agent="route_optimizer_app")
    loc = geolocator.geocode(address)
    return (loc.latitude, loc.longitude) if loc else None

# ── Core logic (identical to app.py) ──────────────────────────────────────────
def route_score(t, e, T=1800, E=1000, a=15, b=2.5, alpha=0.04, beta=0.015):
    t_ratio   = t / T
    e_ratio   = e / E
    penalty_t = alpha * max(0, t - T)
    penalty_e = beta  * max(0, e - E)
    return a * t_ratio + b * e_ratio + penalty_t + penalty_e

def _build_sample(origin, destination, distance_m, mode, hour, day):
    data = {
        "hour_of_day":     hour,
        "day_of_week":     day,
        "origin_lat":      origin[0],
        "origin_lng":      origin[1],
        "destination_lat": destination[0],
        "destination_lng": destination[1],
        "geo_distance":    distance_m,
    }
    for m in ["bicycling", "driving", "transit", "walking"]:
        data[f"mode_{m}"] = 1 if m == mode else 0
    df = pd.DataFrame([data])
    for col in model_columns:
        if col not in df.columns:
            df[col] = 0
    return df[model_columns]

def build_sample_geo(origin, destination, mode, hour, day):
    if not (6 <= hour <= 22): raise ValueError("Hour must be 6–22.")
    if not (0 <= day  <= 6):  raise ValueError("Day must be 0–6.")
    dist = geodesic(origin, destination).meters
    return _build_sample(origin, destination, dist, mode, hour, day)

def build_sample_distance(distance_m, mode, hour, day):
    """Use a direct distance value; reference coords are Seattle center."""
    if not (6 <= hour <= 22): raise ValueError("Hour must be 6–22.")
    if not (0 <= day  <= 6):  raise ValueError("Day must be 0–6.")
    return _build_sample(SEATTLE_CENTER, SEATTLE_CENTER, distance_m, mode, hour, day)

def predict_leg(origin, destination, mode, hour, day):
    sample   = build_sample_geo(origin, destination, mode, hour, day)
    time_s   = float(model.predict(sample)[0])
    dist_m   = float(sample.iloc[0]["geo_distance"])
    emission = EMISSION_FACTORS.get(mode, 0) * dist_m
    return {"time": time_s, "emission": emission, "score": route_score(time_s, emission), "distance_m": dist_m}

def predict_leg_distance(distance_m, mode, hour, day):
    sample   = build_sample_distance(distance_m, mode, hour, day)
    time_s   = float(model.predict(sample)[0])
    emission = EMISSION_FACTORS.get(mode, 0) * distance_m
    return {"time": time_s, "emission": emission, "score": route_score(time_s, emission), "distance_m": distance_m}

def best_mode_for_leg(origin, destination, hour, day):
    best = ("", float("inf"), None)
    for m in ["driving", "bicycling", "transit", "walking"]:
        leg = predict_leg(origin, destination, m, hour, day)
        if leg["score"] < best[1]:
            best = (m, leg["score"], leg)
    return best[0], best[2]

def best_mode_for_leg_distance(distance_m, hour, day):
    best = ("", float("inf"), None)
    for m in ["driving", "bicycling", "transit", "walking"]:
        leg = predict_leg_distance(distance_m, m, hour, day)
        if leg["score"] < best[1]:
            best = (m, leg["score"], leg)
    return best[0], best[2]

# ── Helpers ────────────────────────────────────────────────────────────────────
def score_badge(score: float) -> str:
    if score < 20: return "🟢 Low"
    if score < 40: return "🟡 Medium"
    return "🔴 High"

def fmt_time(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m}m {s}s" if m else f"{s}s"

def fmt_dist(meters: float) -> str:
    return f"{meters/1000:.2f} km" if meters >= 1000 else f"{meters:.0f} m"

def render_leg(label: str, leg: dict, mode: str):
    icon = MODE_ICONS.get(mode, "")
    st.markdown(f"**{label}** &nbsp; {icon} {mode.capitalize()}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Time",      fmt_time(leg["time"]))
    c2.metric("Distance",  fmt_dist(leg["distance_m"]))
    c3.metric("CO₂",       f"{leg['emission']:.0f} g")
    c4.metric("Score",     f"{leg['score']:.1f}  {score_badge(leg['score'])}")

# ── UI ─────────────────────────────────────────────────────────────────────────
st.title("🗺️ Multi-Modal Route Optimizer")
st.caption(
    "Predict travel time and emissions for a two-leg journey (A → B → C) "
    "and find the best transport mode per leg."
)
st.info(
    "**Note:** This model was trained on real-world route data collected across the Seattle, WA metro area. "
    "Predictions are most accurate for Seattle-area coordinates and distances typical of urban travel. "
    "Results for other regions are approximate.",
    icon="ℹ️",
)
st.divider()

# Input method
input_mode = st.radio(
    "Input method",
    ["📍 Address", "📏 Distance", "🔢 Coordinates"],
    horizontal=True,
)
st.write("")  # small spacer

# ── Address inputs ─────────────────────────────────────────────────────────────
if input_mode == "📍 Address":
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        addr_a = st.text_input("Place A — Origin",      placeholder="Space Needle, Seattle")
    with col_b:
        addr_b = st.text_input("Place B — Waypoint",    placeholder="Pike Place Market")
    with col_c:
        addr_c = st.text_input("Place C — Destination", placeholder="Capitol Hill, Seattle")

# ── Distance inputs ────────────────────────────────────────────────────────────
elif input_mode == "📏 Distance":
    st.info("Enter the straight-line distance for each leg. Coordinates default to the Seattle area.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Leg A → B**")
        dist_ab_val  = st.number_input("Distance", min_value=0.1, value=5.0, step=0.1, key="dist_ab")
        dist_ab_unit = st.selectbox("Unit", ["km", "miles"], key="unit_ab")
    with col2:
        st.markdown("**Leg B → C**")
        dist_bc_val  = st.number_input("Distance", min_value=0.1, value=5.0, step=0.1, key="dist_bc")
        dist_bc_unit = st.selectbox("Unit", ["km", "miles"], key="unit_bc")

# ── Coordinate inputs ──────────────────────────────────────────────────────────
else:
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        coord_a = st.text_input("Place A (lat, lng)", placeholder="47.6062, -122.3321")
    with col_b:
        coord_b = st.text_input("Place B (lat, lng)", placeholder="47.6205, -122.3493")
    with col_c:
        coord_c = st.text_input("Place C (lat, lng)", placeholder="47.6396, -122.3030")

st.divider()

# ── Time & mode settings ───────────────────────────────────────────────────────
col_t, col_d, col_m = st.columns(3)
with col_t:
    hour = st.slider("Hour of day", min_value=6, max_value=22, value=9, format="%d:00")
with col_d:
    day_label = st.selectbox("Day of week", DAYS)
    day = DAYS.index(day_label)
with col_m:
    mode = st.selectbox(
        "Transport mode",
        ["driving", "bicycling", "transit", "walking"],
        format_func=lambda m: f"{MODE_ICONS[m]}  {m.capitalize()}",
    )

st.write("")
btn_predict, btn_best = st.columns(2)
run_predict = btn_predict.button("Predict Route",     use_container_width=True)
run_best    = btn_best.button(   "Find Best Modes",   use_container_width=True, type="primary")

# ── Run predictions ────────────────────────────────────────────────────────────
if run_predict or run_best:
    try:
        # Resolve inputs into (origin, destination, leg function args) ──────────
        if input_mode == "📍 Address":
            with st.spinner("Geocoding addresses…"):
                A = geocode(addr_a)
                B = geocode(addr_b)
                C = geocode(addr_c)
            missing = [n for n, v in zip(["A", "B", "C"], [A, B, C]) if v is None]
            if missing:
                st.error(f"Could not geocode: {', '.join(missing)}. Try a more specific address.")
                st.stop()
            use_geo = True

        elif input_mode == "📏 Distance":
            to_m = lambda v, u: v * 1000 if u == "km" else v * 1609.34
            dist_ab_m = to_m(dist_ab_val, dist_ab_unit)
            dist_bc_m = to_m(dist_bc_val, dist_bc_unit)
            use_geo = False

        else:  # Coordinates
            A = tuple(map(float, coord_a.split(",")))
            B = tuple(map(float, coord_b.split(",")))
            C = tuple(map(float, coord_c.split(",")))
            use_geo = True

        st.divider()

        # ── Predict: single mode both legs ────────────────────────────────────
        if run_predict:
            if use_geo:
                leg1 = predict_leg(A, B, mode, hour, day)
                leg2 = predict_leg(B, C, mode, hour, day)
            else:
                leg1 = predict_leg_distance(dist_ab_m, mode, hour, day)
                leg2 = predict_leg_distance(dist_bc_m, mode, hour, day)

            total_time  = leg1["time"]     + leg2["time"]
            total_emis  = leg1["emission"] + leg2["emission"]
            total_score = route_score(total_time, total_emis)

            st.subheader(f"Prediction — {MODE_ICONS[mode]} {mode.capitalize()} both legs")

            # Totals row
            t1, t2, t3 = st.columns(3)
            t1.metric("Total Time",      fmt_time(total_time))
            t2.metric("Total CO₂",       f"{total_emis:.0f} g")
            t3.metric("Route Score",     f"{total_score:.1f}  {score_badge(total_score)}")

            st.write("")
            with st.container(border=True):
                render_leg("Leg A → B", leg1, mode)
            with st.container(border=True):
                render_leg("Leg B → C", leg2, mode)

        # ── Best: optimal mode per leg ─────────────────────────────────────────
        if run_best:
            with st.spinner("Evaluating all modes…"):
                if use_geo:
                    m1, leg1 = best_mode_for_leg(A, B, hour, day)
                    m2, leg2 = best_mode_for_leg(B, C, hour, day)
                else:
                    m1, leg1 = best_mode_for_leg_distance(dist_ab_m, hour, day)
                    m2, leg2 = best_mode_for_leg_distance(dist_bc_m, hour, day)

            total_time  = leg1["time"]     + leg2["time"]
            total_emis  = leg1["emission"] + leg2["emission"]
            total_score = route_score(total_time, total_emis)

            st.subheader("Best Modes — Optimized Per Leg")

            t1, t2, t3 = st.columns(3)
            t1.metric("Total Time",  fmt_time(total_time))
            t2.metric("Total CO₂",   f"{total_emis:.0f} g")
            t3.metric("Route Score", f"{total_score:.1f}  {score_badge(total_score)}")

            st.write("")
            with st.container(border=True):
                render_leg("Leg A → B", leg1, m1)
            with st.container(border=True):
                render_leg("Leg B → C", leg2, m2)

    except Exception as e:
        st.error(f"Error: {e}")

# ── Credits ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    """
    <div style="text-align: center; color: #888; font-size: 0.85em; line-height: 1.8em;">
        <strong>Multi-Modal Route Optimization with Hybrid Travel</strong><br>
        Developed by <strong>Jordan Clifford</strong> &nbsp;·&nbsp;
        Advised by <strong>Dr. Grzegorz Chmaj</strong> &amp; <strong>Dr. Henry Salvaraj</strong><br>
        <a href="https://smartcities.sites.unlv.edu/" target="_blank" style="color: #CF0A2C; text-decoration: none;">
            UNLV Smart Cities Research Program
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)
