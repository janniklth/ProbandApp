from random import random, randint

import sqlalchemy
import flask
from flask import render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
from flask_paginate import Pagination, get_page_args
from flask_sqlalchemy import SQLAlchemy
from pydantic import ValidationError
from sqlalchemy import func, text
import datetime
import os
import openai
from flask import Flask
import json

from schemas.proband import ProbandCreate

app = Flask(__name__)

with open('app/config.json') as f:
    config = json.load(f)
    openai_api_key = config['openai']['api_key']

app.config['SECRET_KEY'] = os.urandom(24)
app.secret_key = "super secret key"

DB_CONFIG = {
    "MYSQL_HOST": "127.0.0.1",
    "MYSQL_USER": "root",
    "MYSQL_PASSWORD": "change-me",
    "MYSQL_DB": "dbproject",
    "SQLALCHEMY_DATABASE_URI": "mysql://root:change-me@127.0.0.1:3306/dbproject",
}

app.config.update(DB_CONFIG)

mysql = MySQL(app)

# Init DB
db = SQLAlchemy(app)


def get_probands(items, offset=0, per_page=12):
    return items[offset: offset + per_page]


class Proband(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), unique=False, nullable=False)
    lastname = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(10), unique=True, nullable=False)
    gender = db.Column(db.String(1), unique=False, nullable=False)
    birthday = db.Column(db.DateTime, unique=False, nullable=False)
    height = db.Column(db.Float, unique=False, nullable=False)
    weight = db.Column(db.Float, unique=False, nullable=False)
    health = db.Column(db.Float, unique=False, nullable=False)
    isactive = db.Column(db.Boolean, unique=False, nullable=False)

    def __init__(self, firstname, lastname, email, gender, birthday, height, weight, health, isactive):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.gender = gender
        self.birthday = birthday
        self.height = height
        self.weight = weight
        self.health = health
        self.isactive = isactive


class Gender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name


def create_proband(firstname: str, lastname: str, email: str, gender: str, birthday: datetime, height: float,
                   weight: float, health: float, isactive: bool) -> Proband:
    """
    Create a Proband instance and add it to the database.

    :param health:
    :param isactive:
    :param weight:
    :param height:
    :param birthday:
    :param gender:
    :param email:
    :param lastname:
    :param firstname: probands firstname
    :return: a Proband instance or None
    """

    proband = Proband(firstname=firstname, lastname=lastname, email=email, gender=gender, birthday=birthday,
                      height=height, weight=weight, health=health, isactive=isactive)
    db.session.add(proband)
    db.session.commit()
    return proband


def handle_error(e: Exception):
    print("Action failed!")
    print(e)

def load_data_from_sql():
    try:
        with app.app_context():
            # Überprüfen, ob bereits Daten in der Proband-Tabelle vorhanden sind
            if not db.session.query(Proband.query.exists()).scalar():
                with open("Daten.sql", 'r', encoding='utf-8') as data_file:
                    lines = data_file.readlines()

                    current_table = ""

                    for line in lines:
                        line = line.strip()
                        if line.startswith("-- "):
                            current_table = line.replace("-- ", "").strip()

                        if line and not line.startswith("--"):
                            if current_table == "Probanden":
                                data = line.split(',')
                                country_id = randint(0, 26)
                                proband_data = {
                                    "firstname": data[0].strip(),
                                    "lastname": data[1].strip(),
                                    "email": data[2].strip(),
                                    "gender": data[3].strip(),
                                    "birthday": data[4].strip(),  # assuming birthday format is correct
                                    "weight": float(data[5].strip()),
                                    "height": float(data[6].strip()),
                                    "health": float(data[7].strip()),
                                    "isactive": bool(data[8].strip())
                                }
                                try:
                                    proband = ProbandCreate(**proband_data)
                                    create_proband(proband)
                                except ValidationError as e:
                                    print(f"Validation failed for data: {proband_data}")
                                    print(e)
    except Exception as e:
        print(f"Error loading data from Daten.sql: {e}")

#
# with app.app_context():
#     with db.engine.connect() as conn:
#         with open("initial.sql", 'r') as file:
#             content = file.read()
#             transaction = conn.begin()
#             try:
#                 for command in content.split(";"):
#                     if command.strip() != "":
#                         conn.execute(text(command))
#                 transaction.commit()
#             except Exception as alleskaputt:
#                 print(f"Command skipped: {command}")
#                 print(alleskaputt)
#                 transaction.rollback()
#
#         transaction = conn.begin()
#         probands = conn.execute(text('SELECT * FROM Proband;')).fetchall()
#         if len(probands) == 0:
#             print("No entries, first setup, seeding the database with data :))")
#             try:
#                 with open("Daten.sql", 'r', encoding='utf-8') as dada:
#                     lines = dada.readlines()
#
#                     current_table = ""
#
#                     for line in lines:
#                         line = line.replace("\n", "")
#                         if line.startswith("-- "):
#                             current_table = line.replace("-- ", "")
#                             current_table = current_table.replace(" ", "")
#
#                         if line != "" and line != f"-- {current_table}":
#                             if current_table == "Medikament":
#                                 conn.execute(text(f"INSERT INTO Medication (name) VALUES ({line});"))
#                             if current_table == "Krankheit":
#                                 conn.execute(text(f"INSERT INTO Sickness (name) VALUES ({line});"))
#                             if current_table == "Geschlecht":
#                                 conn.execute(text(f"INSERT INTO Gender (name) VALUES ({line});"))
#                             if current_table == "Länder":
#                                 conn.execute(text(f"INSERT INTO Country (countrycode, name) VALUES ({line});"))
#                             if current_table == "Probanden":
#                                 country_id = randint(0, 26)
#                                 conn.execute(text(
#                                     f"INSERT INTO Proband (firstname, lastname, email, gender, birthday, weight, height, countryid) VALUES ({line}, {country_id});"))
#
#                 conn.execute(text("SET GLOBAL FOREIGN_KEY_CHECKS=1;"))
#                 transaction.commit()
#                 print("we seeded the db succesfully")
#             except Exception as this_no_worky:
#                 print(f" {this_no_worky}")


@app.route('/probands', methods=['POST', 'GET'])
def probands():
    if request.method == 'GET':
        # total = 20
        page, per_page, offset = get_page_args(page_parameter="page",
                                               per_page_parameter="per_page")
        genders = Gender.query.all()
        probands = Proband.query.filter(Proband.isactive.is_(True)).all()
        total = len(probands)
        pagination_probands = get_probands(probands, offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')
        return render_template('probands.html', probandsList=pagination_probands, genders=genders, page=page,
                               per_page=per_page,
                               pagination=pagination)
    else:
        return render_template('probands.html')


def determine_search_string():
    search_str = request.form.get('search_probands')
    if session['search'] is None or session['search'] == "":
        session['search'] = search_str
    elif session['search']:
        search_str = session['search']
    return search_str if search_str else ""


@app.route('/search', methods=['POST', 'GET'])
def search():
    page, per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")
    if request.method == "POST":
        session['search'] = ""

    search_str = request.form.get('search_probands')

    if session['search'] is None or session['search'] == "":
        session['search'] = search_str
    elif session['search']:
        search_str = session['search']
    if search_str is None:
        search_str = ""

    search_str = determine_search_string()

    formatted_search = "%{}%".format(search_str)
    # TODO: nur aktive
    probands = Proband.query.filter(Proband.lastname.like(formatted_search)).all()

    genders = Gender.query.all()
    total = len(probands)
    pagination_probands = get_probands(probands, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('/probands.html', probandsList=pagination_probands, genders=genders, page=page,
                           per_page=per_page,
                           pagination=pagination, search=search_str)


@app.route("/delete", methods=["POST"])
def delete():
    try:
        email = request.form.get("email")
        proband = Proband.query.filter_by(email=email).first()
        proband.isactive = False
        db.session.commit()
        return redirect(url_for('probands'))
    except Exception as e:
        handle_error(e)


@app.route("/update", methods=["POST"])
def update():
    try:
        oldemail = request.form.get("oldemail")
        newlastname = request.form.get("newlastname")
        newfirstname = request.form.get("newfirstname")
        newemail = request.form.get("newemail")
        newbirthday = request.form.get("newbirthday")
        newweight = request.form.get("newweight")
        newheight = request.form.get("newheight")
        newhealth = request.form.get("newhealth")
        medi = request.form.get("genselect")
        if medi == 'M':
            medi = 1
        else:
            medi = 2
        p = Proband.query.filter_by(email=oldemail).first()
        p.firstname = newfirstname
        p.lastname = newlastname
        p.email = newemail
        p.gender = medi
        p.birthday = newbirthday
        p.height = newheight
        p.weight = newweight
        p.health = newhealth
        db.session.commit()
        return redirect(url_for('probands'))

    except Exception as e:
        handle_error(e)


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        try:
            medi = request.form.get("genselect")
            if medi == 'M':
                medi = 1
            else:
                medi = 2
            create_proband(request.form.get("firstname"), request.form.get("lastname"),
                           request.form.get("email"), medi, request.form.get("birthday"),
                           request.form.get("height"), request.form.get("weight"), request.form.get("health"),
                           sqlalchemy.true())
            return redirect(url_for('probands'))
        except Exception as e:
            handle_error(e)


def create_messages(question, context):
    return [
        {
            "role": "system",  # Rolle für generelle Einstellungen der Konversation, also Kontextinformationen
            "content": context
        },
        {
            "role": "user",  # Benutzer, der Prompts formuliert
            "content": question
        }
    ]


@app.route("/generate", methods=["POST", "GET"])
def generate():
    question = request.args.get("question", "")
    question = str(question).strip()
    context = request.args.get("context", "")
    context = str(context).strip()
    data = ''
    if question:
        def stream():
            openai.api_key = openai_api_key
            messages = create_messages(question, context)
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,  # Kreativität der Generierung; zufällig Generierung nächster Token
                # Eingabe werden in Tokens unterteilt, die dann in Vektoren umgewandelt werden
                # max_tokens=1000,
                stream=True,
                top_p=1,  # Alternative zu temperature
            )
            for trunk in response:
                if trunk['choices'][0]['finish_reason'] is not None:
                    data = '[DONE]'
                else:
                    data = trunk['choices'][0]['delta'].get('content', '')
                yield "data: %s\n\n" % data.replace("\n", "<br>")

        return flask.Response(stream(), mimetype="text/event-stream")
    return render_template('generate.html')


@app.route('/')
def index():  # put application's code here
    return render_template('home.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    return render_template('registration.html')


@app.route('/report', methods=["GET", "POST"])
def report():
    if request.method == 'GET':

        probands = Proband.query.all()
        activeProbands = Proband.query.filter(Proband.isactive.is_(True)).all()
        inactiveProbands = Proband.query.filter(Proband.isactive.is_(False)).all()

        std = db.session.query(func.stddev(Proband.weight))
        result = db.session.execute(std)
        stddevweight = [row[0] for row in result]

        std = db.session.query(func.stddev(Proband.height))
        result = db.session.execute(std)
        stddevheight = [row[0] for row in result]

        totalProbands = len(probands)
        totalActiveProbands = len(activeProbands)
        totalInactiveProbands = len(inactiveProbands)

        probandReport = [totalProbands, totalActiveProbands, totalInactiveProbands]
        parent_list = [{'Probanden insgesamt: ': totalProbands, 'Aktive Probanden: ': totalActiveProbands,
                        'Inaktive Probanden: ': totalInactiveProbands,
                        'STDDEV Gewicht: ': stddevweight, 'STDDEV Größe: ': stddevheight}]
        print(probandReport)

        return render_template('report.html', report=parent_list)
    else:
        return render_template('report.html')


if __name__ == "__main__":
    # load data from sql
    load_data_from_sql()

    # run the app
    app.run(debug=True, port=8080)


