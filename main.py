from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from forms import SearchCafeForm, AddCafeForm
import os
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
db = SQLAlchemy(model_class=Base)
db.init_app(app)
Bootstrap5(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html", content_id="home-page-body")

# HTTP GET - Read Record
@app.route("/all")
def get_all_cafes():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    if all_cafes:
        return render_template("cafes.html", content_id="all-cafes-body", all_cafes=all_cafes)
    else:
        return render_template("no_cafes.html", content_id="all-cafes-body", all_cafes=all_cafes)

@app.route("/search", methods=['GET', 'POST'])
def search_cafe():
    form = SearchCafeForm()
    if form.validate_on_submit():
        query_location = request.form.get("city")
        query_location = query_location.title()
        result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
        all_cafes = result.scalars().all()
        if all_cafes:
            return render_template("cafes.html", content_id="all-cafes-body", all_cafes=all_cafes)
        else:
            return render_template("no_cafes.html", content_id="all-cafes-body", query_location=query_location)
    return render_template("search_cafe.html", form=form, content_id="search-cafes-body")

# HTTP POST - Create Record

@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():
        try:
            new_cafe = Cafe(
                name=request.form.get("name"),
                map_url=request.form.get("map_url"),
                img_url=request.form.get("img_url"),
                location=request.form.get("location"),
                has_sockets=request.form.get("sockets"),
                has_toilet=request.form.get("toilet"),
                has_wifi=request.form.get("wifi"),
                can_take_calls=request.form.get("calls"),
                seats=request.form.get("seats"),
                coffee_price=request.form.get("coffee_price"),
            )
            if new_cafe.has_sockets.title() == "True":
                new_cafe.has_sockets = True
            else:
                new_cafe.has_sockets = False
            if new_cafe.has_toilet.title() == "True":
                new_cafe.has_toilet = True
            else:
                new_cafe.has_toilet = False
            if new_cafe.has_wifi.title() == "True":
                new_cafe.has_wifi = True
            else:
                new_cafe.has_wifi = False
            if new_cafe.can_take_calls.title() == "True":
                new_cafe.can_take_calls = True
            else:
                new_cafe.can_take_calls = False
            db.session.add(new_cafe)
            db.session.commit()
            return redirect(url_for('get_all_cafes'))
        except IntegrityError:

            form.name.errors.append("That café already exists in our database!")
            return render_template("add_cafe.html", form=form, content_id="add-cafes-body", errors=form.errors)
    return render_template("add_cafe.html", form=form, content_id="add-cafes-body")

# HTTP DELETE - Delete Record

@app.route("/report-closed/<int:cafe_id>")
def delete(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    delete_listing = request.args.get('delete_listing')
    if delete_listing:
        db.session.delete(cafe)
        db.session.commit()
        return redirect(url_for('get_all_cafes'))
    return render_template('report_closed.html', cafe=cafe, content_id="delete_cafe_body")

if __name__ == '__main__':
    app.run(debug=True)
