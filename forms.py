from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SelectMultipleField, SubmitField, RadioField


from wtforms.validators import DataRequired

import json

with open("./columns.json", "r") as f:
  columns=json.load(f)["data_columns"]
  locations = columns[5:]  

class RadioForm(FlaskForm):

  rcity = RadioField(
    choices=[('PREDICT','PREDICT'),
    ('HYDERABAD','HYDERABAD'),
    ('CHENNAI','CHENNAI'),
    ('BANGALORE','BANGALORE'),
    ('MUMBAI','MUMBAI'),
    ('DELHI','DELHI'),
    ('KOLKATA','KOLKATA'),],
    validators=[DataRequired()],
    # default='PREDICT'
  )


class PredictForm(FlaskForm):

  area = IntegerField(
    label='Area (Sqft)',
    validators=[DataRequired()]
  )

  bedrooms = IntegerField(
    label='No. of Bedrooms',
    validators=[DataRequired()]
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

  city = SelectField(
    label="City",
    choices=['Hyderabad', 'Chennai', 'Bangalore', 'Mumbai', 'Delhi', 'Kolkata'],
    validators=[DataRequired()]
  )

  submit = SubmitField("Predict")


class HydForm(FlaskForm):

  area = IntegerField(
    label='Area (Sqft)',
    validators=[DataRequired()]
  )

  bedrooms = IntegerField(
    label='No. of Bedrooms',
    validators=[DataRequired()]
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
