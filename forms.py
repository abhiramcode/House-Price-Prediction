from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField


from wtforms.validators import DataRequired

import json

with open("./columns.json", "r") as f:
  columns=json.load(f)["data_columns"]
  locations = columns[5:]  


class InputForm(FlaskForm):
  area = IntegerField(
    label='Area (Sqft)',
    validators=[DataRequired()]
  )

  bedrooms = IntegerField(
    label='No. of Bedrooms',
    validators=[DataRequired(),]
  )

  resale = SelectField(
    label='Resale',
    choices=[
      (1, "Yes"),
      (0, "No"),
    ],
    validators=[DataRequired()]
  )

  indoor_luxury = SelectField(
    label="Indoor Luxury",
    choices=[
      (0, "No"),
      (1, "Level 1"),
      (2, "Level 2"),
      (3, "Level 3"),
      (4, "Level 4")
    ],
    validators=[DataRequired()]
  )

  outdoor_luxury = SelectField(
    label="Outdoor Luxury",
    choices=[
      (0, "No"),
      (1, "Level 1"),
      (2, "Level 2"),
      (3, "Level 3"),
      (4, "Level 4")
    ],
    validators=[DataRequired()]
  )

  location = SelectField(
    label="Location",
    choices=locations,
    validators=[DataRequired()]
  )

  submit = SubmitField("Predict")