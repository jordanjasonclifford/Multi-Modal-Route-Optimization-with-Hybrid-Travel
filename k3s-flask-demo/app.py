from flask import Flask, request, render_template
import joblib
import pandas as pd
from geopy.distance import geodesic

app = Flask(__name__, template_folder="templates")
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Load model & columns
model = joblib.load('travel_time_model.pkl')
model_columns = joblib.load('model_columns.pkl')

# Emission factors (grams per meter)
emission_factors = {'driving': 0.192, 'transit': 0.105, 'bicycling': 0.0, 'walking': 0.0}

# Scoring
def route_score(t, e, T=1800, E=1000, a=15, b=2.5, alpha=0.04, beta=0.015):
    t_ratio = t / T
    e_ratio = e / E
    penalty_t = alpha * max(0, t - T)
    penalty_e = beta * max(0, e - E)
    return a * t_ratio + b * e_ratio + penalty_t + penalty_e

# Build sample
def build_sample_geo(origin, destination, mode, hour, day):
    if not (6 <= hour <= 22): raise ValueError("Hour must be between 6 and 22.")
    if not (0 <= day <= 6):   raise ValueError("Day must be between 0 (Mon) and 6 (Sun).")

    data = {
        'hour_of_day': hour,
        'day_of_week': day,
        'origin_lat': origin[0],
        'origin_lng': origin[1],
        'destination_lat': destination[0],
        'destination_lng': destination[1],
        'geo_distance': geodesic(origin, destination).meters
    }
    for m in ['bicycling', 'driving', 'transit', 'walking']:
        data[f'mode_{m}'] = 1 if m == mode else 0

    df = pd.DataFrame([data])
    for col in model_columns:
        if col not in df.columns:
            df[col] = 0
    return df[model_columns]

def predict_leg(origin, destination, mode, hour, day):
    sample = build_sample_geo(origin, destination, mode, hour, day)
    predicted_time = float(model.predict(sample)[0])
    distance = float(sample.iloc[0]['geo_distance'])
    emission = emission_factors.get(mode, 0) * distance
    score_value = route_score(predicted_time, emission)
    return {'time': predicted_time, 'emission': emission, 'score': score_value, 'distance_m': distance}

def best_mode_for_leg(origin, destination, hour, day):
    """Return (mode, leg_stats) minimizing score for that leg."""
    best = ('', float('inf'), None)
    for m in ['driving', 'bicycling', 'transit', 'walking']:
        leg = predict_leg(origin, destination, m, hour, day)
        if leg['score'] < best[1]:
            best = (m, leg['score'], leg)
    return best[0], best[2]

@app.route('/', methods=['GET','POST'])
def home():
    ui = dict(
        result_total=None, emissions_total=None, score_total=None,
        mode=None, leg1=None, leg2=None, leg1_mode=None, leg2_mode=None,
        error=None
    )

    if request.method == 'POST':
        try:
            A = tuple(map(float, request.form['coord_a'].split(',')))
            B = tuple(map(float, request.form['coord_b'].split(',')))
            C = tuple(map(float, request.form['coord_c'].split(',')))
            hour = int(request.form['hour'])
            day = int(request.form['day'])
            action = request.form['action']

            if action == 'predict':
                # Single selected mode for BOTH legs
                mode = request.form['mode']
                leg1 = predict_leg(A, B, mode, hour, day)
                leg2 = predict_leg(B, C, mode, hour, day)
                total_time = leg1['time'] + leg2['time']
                total_emis = leg1['emission'] + leg2['emission']
                total_score = route_score(total_time, total_emis)
                ui.update(
                    mode=mode,
                    leg1={k: round(v,2) for k,v in leg1.items()},
                    leg2={k: round(v,2) for k,v in leg2.items()},
                    result_total=round(total_time,2),
                    emissions_total=round(total_emis,2),
                    score_total=round(total_score,2)
                )

            elif action == 'best_mixed':
                # Best mode per leg independently
                m1, leg1 = best_mode_for_leg(A, B, hour, day)
                m2, leg2 = best_mode_for_leg(B, C, hour, day)
                total_time = leg1['time'] + leg2['time']
                total_emis = leg1['emission'] + leg2['emission']
                total_score = route_score(total_time, total_emis)
                ui.update(
                    leg1_mode=m1, leg2_mode=m2,
                    leg1={k: round(v,2) for k,v in leg1.items()},
                    leg2={k: round(v,2) for k,v in leg2.items()},
                    result_total=round(total_time,2),
                    emissions_total=round(total_emis,2),
                    score_total=round(total_score,2)
                )

        except Exception as e:
            ui['error'] = str(e)

    return render_template('index.html', **ui)

if __name__ == '__main__':
    app.run(debug=True)
