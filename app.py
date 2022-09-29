import datetime
import requests
import pandas as pd
from os import environ
from flask import Flask, session, request, redirect, render_template, url_for, flash
from dotenv import load_dotenv

print(pd.__version__)

load_dotenv()

app = Flask(__name__)
app.secret_key = environ.get('SECRET_KEY')


def get_population_by_state():
    response = requests.get(
        'https://datausa.io/api/data?drilldowns=State&measures=Population')
    data = response.json()
    return data.get('data', [])


@app.context_processor
def today():
    return {'today': datetime.date.today()}


@app.route("/")
def root():
    username = session.get('username')
    if username is None:
        return redirect(url_for('login'))

    data = get_population_by_state()
    df = pd.DataFrame(data, columns=['State', 'Year', 'Population'])
    dfstyle = df.style.background_gradient()

    return render_template("root.html", username=username, population=data, table=dfstyle.to_html())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        flash('You were successfully logged in')
        return redirect(url_for('root'))

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('root'))
