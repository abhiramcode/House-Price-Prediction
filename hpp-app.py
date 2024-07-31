import pickle
import numpy as np

from flask import Flask, render_template
from forms import InputForm

with open("hyd_house_price_prediction.pickle","rb") as f:
    model = pickle.load(f)

app = Flask(__name__)
app.config["SECRET_KEY"] = "this_is_abhi_secret_key"


import json

with open("./columns.json", "r") as f:
    columns=json.load(f)["data_columns"]
    locations = columns[5:]

def predict_price(location, area, bhk, resale, il, ol):
    loc_index = locations.index(location)

    x = np.zeros( len(columns) )
    x[0] = area
    x[1] = bhk
    x[2] = resale
    x[3] = il
    x[4] = ol
    if loc_index>4:
        x[loc_index] = 1

    return model.predict([x])[0]

@app.route("/")
@app.route("/home")
def home():
    return render_template( "home.html", title="home" )


@app.route("/predict", methods=["GET", "POST"])
def predict():
  input=InputForm()
  msg = ""
  if input.validate_on_submit():
    # x_input = pd.DataFrame({
    #   'Area': [input.area.data],
    #   'No. of Bedrooms': [input.bedrooms.data],
    #   'Resale': [input.resale.data],
    #   'IndoorLuxury': [input.indoor_luxury.data],
    #   'OutdoorLuxury': [input.outdoor_luxury.data],
    #   'Location': [input.location.data]
    # })
    prediction = predict_price(input.location.data, np.log1p(input.area.data), input.bedrooms.data, input.resale.data, input.indoor_luxury.data, input.outdoor_luxury.data)
    prediction = np.expm1(prediction)
    msg = f"The predicted price is {prediction:,.0f} INR"
  else :
    msg = "Please provide valid Information"
  return render_template( "predict.html", title="predict", form=input, output=msg )


if __name__ == "__main__":
    print("Starting the application.....")
    app.run(host="0.0.0.0", port=5000, debug=True)
