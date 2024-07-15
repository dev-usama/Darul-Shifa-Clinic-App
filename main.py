from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


@app.route("/")
@app.route("/homepage")
def home():
    return render_template("index.html", title="Homepage")

@app.route("/about")
def about():
    return "About page"

if __name__ == "__main__":
    app.run(debug=True)