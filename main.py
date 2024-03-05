# Import necessary modules and classes for Flask, Flask-WTF, and CSV handling
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, URLField
from wtforms.validators import DataRequired, URL
import csv

# Create a Flask application instance
app = Flask(__name__)
# Set a secret key for securely signing the session cookie
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
# Apply Bootstrap5 styling to the app
Bootstrap5(app)


# Define a form class for adding new cafes, inheriting from FlaskForm
class CafeForm(FlaskForm):
    cafe = StringField(
        "Cafe name", validators=[DataRequired()]
    )  # Field for the cafe's name, input required
    location = URLField(
        "Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()]
    )  # URL field for location, must be a valid URL
    open_time = StringField(
        "Opening Time e.g. 8AM", validators=[DataRequired()]
    )  # Opening time field, input required
    close_time = StringField(
        "Closing Time e.g. 5:30PM", validators=[DataRequired()]
    )  # Closing time field, input required
    # Select fields for coffee, wifi, and power ratings with predefined choices
    coffee_rating = SelectField(
        "Coffee Rating",
        choices=[
            ("☕", "☕"),
            ("☕ ☕", "☕ ☕"),
            ("☕ ☕ ☕", "☕ ☕ ☕"),
            ("☕ ☕ ☕ ☕", "☕ ☕ ☕ ☕"),
            ("☕ ☕ ☕ ☕ ☕", "☕ ☕ ☕ ☕ ☕"),
        ],
        validators=[DataRequired()],
    )
    wifi_rating = SelectField(
        "Wifi Strength Rating",
        choices=[
            ("✘", "✘"),
            ("💪", "💪"),
            ("💪 💪", "💪 💪"),
            ("💪 💪 💪", "💪 💪 💪"),
            ("💪 💪 💪 💪", "💪 💪 💪 💪"),
            ("💪 💪 💪 💪 💪", "💪 💪 💪 💪 💪"),
        ],
        validators=[DataRequired()],
    )
    power_socket = SelectField(
        "Power Socket Availability",
        choices=[
            ("✘", "✘"),
            ("🔌", "🔌"),
            ("🔌 🔌", "🔌 🔌"),
            ("🔌 🔌 🔌", "🔌 🔌 🔌"),
            ("🔌 🔌 🔌 🔌", "🔌 🔌 🔌 🔌"),
            ("🔌 🔌 🔌 🔌 🔌", "🔌 🔌 🔌 🔌 🔌"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")  # Submit button for the form


# Define the home page route
@app.route("/")
def home():
    return render_template("index.html")  # Render the home page template


# Define the route for adding a new cafe
@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()  # Create an instance of CafeForm
    if form.validate_on_submit():  # Check if the form is submitted and valid
        # If valid, collect the form data
        cafe_name = form.cafe.data
        location_url = form.location.data
        open_time = form.open_time.data
        close_time = form.close_time.data
        coffee_rating = form.coffee_rating.data
        wifi_rating = form.wifi_rating.data
        power_socket = form.power_socket.data
        # Open the CSV file in append mode and write the collected data as a new row
        with open(
            "cafe-data.csv",
            mode="a",
            newline="",
            encoding="utf-8",
        ) as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow(
                [
                    cafe_name,
                    location_url,
                    open_time,
                    close_time,
                    coffee_rating,
                    wifi_rating,
                    power_socket,
                ]
            )
        # After writing to the CSV file, redirect to the cafes page
        return redirect(url_for("cafes"))
    return render_template("add.html", form=form)  # Render the add cafe form template


# Define the route for displaying the list of cafes
@app.route("/cafes")
def cafes():
    with open(
        "cafe-data.csv",
        newline="",
        encoding="utf-8",
    ) as csv_file:  # Open the CSV file in read mode
        csv_data = csv.reader(csv_file, delimiter=",")
        list_of_rows = []
        for (
            row
        ) in (
            csv_data
        ):  # Iterate over each row in the CSV file and append to list_of_rows
            list_of_rows.append(row)
    return render_template(
        "cafes.html", cafes=list_of_rows
    )  # Render the cafes page template with the list of cafes


# Check if the script is the main program and run the app.
if __name__ == "__main__":
    app.run(debug=True, port=5001)
