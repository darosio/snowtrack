import os

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config
from models import Event, Participant  # db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# app = Flask(__name__)
# app.config.from_object(Config)
# db.init_app(app)
# migrate = Migrate(app, db)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(BASE_DIR, 'instance/local.db')}"
)
# app.config["SQLALCHEMY_DATABASE_URI"] = (
#     "sqlite:///instance/local.db"  # Adjust if needed
# )
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

migrations_applied = False


@app.before_request
def apply_migrations():
    global migrations_applied
    if not migrations_applied:
        from flask_migrate import upgrade

        upgrade()
        migrations_applied = True


# @app.before_first_request
# def apply_migrations():
#     from flask_migrate import upgrade

#     upgrade()


@app.route("/")
def home():
    events = Event.query.all()
    return render_template("view_event.html", events=events)


@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    if request.method == "POST":
        name = request.form["name"]
        new_event = Event(name=name)
        db.session.add(new_event)
        db.session.commit()
        flash("Event created successfully!", "success")
        return redirect(url_for("home"))
    return render_template("create_event.html")


@app.route("/participate", methods=["GET", "POST"])
def participate():
    events = Event.query.all()
    if request.method == "POST":
        event_id = request.form["event"]
        pickup_location = request.form["pickup_location"]
        participant = Participant(event_id=event_id, pickup_location=pickup_location)
        db.session.add(participant)
        db.session.commit()
        flash("Participation recorded!", "success")
        return redirect(url_for("home"))
    return render_template("participate.html", events=events)


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
