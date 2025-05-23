import pickle
import locale
# locale.setlocale(locale.LC_ALL, 'en_IN')

import json
import numpy as np
from flask import Flask, render_template, request, flash, jsonify
from forms import RadioForm, PredictForm, HydForm

# Load models and data
with open("hyd_house_price_prediction.pickle", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)
app.config["SECRET_KEY"] = "this_is_abhi_secret_key"

# Load columns data
with open("./columns.json", "r") as f:
    columns = json.load(f)["data_columns"]
    locations = columns[5:]

def format_inr(number):
    number = int(round(number))
    s = str(number)[::-1]
    parts = []

    # First 3 digits
    parts.append(s[:3])
    s = s[3:]

    # Rest in chunks of 2
    while s:
        parts.append(s[:2])
        s = s[2:]

    formatted = ','.join(parts)[::-1]
    return formatted

def predict_price(location, area, bhk, resale, il, ol):
    try:
        loc_index = locations.index(location)
        loc_index = loc_index + 5
        x = np.zeros(len(columns))
        x[0] = area
        x[1] = bhk
        x[2] = resale
        x[3] = il
        x[4] = ol
        print(loc_index)
        if loc_index >= 4:
            x[loc_index] = 1
        return model.predict([x])[0]
    except Exception as e:
        print(f"Prediction error: {e}")
        return None

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="home")

@app.route("/set_city", methods=["POST"])
def set_city():
    selected_city = request.form.get("rcity", "0")
    return jsonify({"selected_city": selected_city})

@app.route("/predict", methods=["GET", "POST"])
def predict():
    radio_form = RadioForm()
    predict_form = PredictForm()
    hyd_form = HydForm()
    prediction_msg = "Please provide information"
    selected_city = request.form.get('rcity', '1')

    if request.method == 'POST':
        try:
            if hyd_form.validate_on_submit():
                area = float(request.form.get('area'))
                bedrooms = int(request.form.get('bedrooms'))
                resale = request.form.get('resale')
                indoor_luxury = request.form.get('indoor_luxury')
                outdoor_luxury = request.form.get('outdoor_luxury')
                location = request.form.get('location')

                # model = load_model(selected_city)
                prediction = predict_price(
                    location,
                    np.log1p(area),
                    bedrooms,
                    resale,
                    indoor_luxury,
                    outdoor_luxury
                )

                if prediction is not None:
                    prediction = np.expm1(prediction) * 1.05
                    prediction = format_inr(prediction)
                    prediction_msg = f"The predicted price of the house is {prediction} INR"
                else:
                    prediction_msg = "Error in prediction. Please try again."
            else:
                prediction_msg = "Please fill all fields properly"
        except Exception as e:
            print("Form Error:", e)
            prediction_msg = "Something went wrong. Please try again."

        # If AJAX request, return JSON
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({
                "prediction": prediction_msg,
                "selected_city": selected_city
            })

    # Normal GET or fallback
    return render_template(
        "predict.html",
        title="Predict",
        formr=radio_form,
        formp=predict_form,
        formh=hyd_form,
        output=prediction_msg,
        selected_city=selected_city
    )

if __name__ == "__main__":
    print("Starting the application.....")
    app.run(host="0.0.0.0")
