from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd
from geopy.distance import geodesic

app = Flask(__name__)

# Load the model and column list
model = joblib.load('travel_time_model.pkl')
model_columns = joblib.load('model_columns.pkl')

# Emission factors (grams per meter)
emission_factors = {
    'driving': 0.192,
    'transit': 0.105,
    'bicycling': 0.0,
    'walking': 0.0
}

# Scoring function from RouteScoring_REU2025.ipynb
def route_score(t, e, T=1800, E=1000, a=15, b=1, alpha=0.04, beta=0.015):
    t_ratio = t / T
    e_ratio = e / E
    penalty_t = alpha * max(0, t - T)
    penalty_e = beta * max(0, e - E)
    return a * t_ratio + b * e_ratio + penalty_t + penalty_e


# Utility to build input sample
def build_sample_geo(origin, destination, mode, hour, day):
    if not (6 <= hour <= 22):
        raise ValueError("Hour must be between 6 and 22.")
    if not (0 <= day <= 6):
        raise ValueError("Day must be between 0 (Monday) and 6 (Sunday).")

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
    df = df[model_columns]
    return df

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    emissions = None
    score = None

    if request.method == 'POST':
        try:
            origin = (float(request.form['origin_lat']), float(request.form['origin_lng']))
            destination = (float(request.form['destination_lat']), float(request.form['destination_lng']))
            mode = request.form['mode']
            hour = int(request.form['hour'])
            day = int(request.form['day'])

            sample = build_sample_geo(origin, destination, mode, hour, day)
            predicted_time = model.predict(sample)[0]

            # Calculate emissions
            distance = sample.iloc[0]['geo_distance']
            emission = emission_factors.get(mode, 0) * distance

            # Calculate score
            score_value = route_score(predicted_time, emission)

            # Round for display
            result = round(predicted_time, 2)
            emissions = round(emission, 2)
            score = round(score_value, 2)

        except Exception as e:
            result = f"Error: {e}"

    return render_template('index.html', result=result, emissions=emissions, score=score)

# API route for prediction
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    try:
        # Parse from URL query parameters
        origin_lat = float(request.args.get('origin_lat'))
        origin_lng = float(request.args.get('origin_lng'))
        dest_lat = float(request.args.get('destination_lat'))
        dest_lng = float(request.args.get('destination_lng'))
        mode = request.args.get('mode')
        hour = int(request.args.get('hour'))
        day = int(request.args.get('day'))

        origin = (origin_lat, origin_lng)
        destination = (dest_lat, dest_lng)

        sample = build_sample_geo(origin, destination, mode, hour, day)
        pred = model.predict(sample)[0]

        return jsonify({
            'predicted_duration_seconds': round(pred, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
