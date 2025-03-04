from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class AddCafeForm(FlaskForm):
    name = StringField("", validators=[DataRequired()],
                       render_kw={"placeholder": "Café Name", "class": "add-bar"})
    map_url = StringField("", validators=[DataRequired(), URL()],
                          render_kw={"placeholder": "Map URL", "class": "add-bar"})
    img_url = StringField("", validators=[DataRequired(), URL()],
                          render_kw={"placeholder": "Image URL", "class": "add-bar"})
    location = StringField("", validators=[DataRequired()],
                           render_kw={"placeholder": "City Name", "class": "add-bar"})
    sockets = StringField("", validators=[DataRequired()],
                              render_kw={"placeholder": "Outlets available? True/False", "class": "add-bar"})
    toilet = StringField("", validators=[DataRequired()],
                             render_kw={"placeholder": "Restroom available? True/False", "class": "add-bar"})
    wifi = StringField("", validators=[DataRequired()],
                           render_kw={"placeholder": "WiFi available? True/False", "class": "add-bar"})
    calls = StringField("", validators=[DataRequired()],
                                 render_kw={"placeholder": "Call-Friendly? True/False", "class": "add-bar"})
    seats = StringField("", validators=[DataRequired()],
                        render_kw={"placeholder": "Approximate Number of Seats", "class": "add-bar"})
    coffee_price = StringField("", validators=[DataRequired()],
                               render_kw={"placeholder": "Avg. Coffee Price", "class": "add-bar"})
    submit = SubmitField("Add Cafe", render_kw={"id": "add-btn"})

class SearchCafeForm(FlaskForm):
    city = StringField("", validators=[DataRequired()],
                       render_kw={"placeholder": "Enter city name", "id": "city-search-bar"})
    submit = SubmitField("Search")
