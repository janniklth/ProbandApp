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

from app.db import crud
from app.db.session import get_db
from models.gender import Gender
from db.crud import handle_error
from models.proband import Proband

# create a new Flask app
app = Flask(__name__)

# load openai config
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
    "SQLALCHEMY_DATABASE_URI": "mysql://root:@127.0.0.1:3306/dbproject",
}

app.config.update(DB_CONFIG)

mysql = MySQL(app)

# Init DB
db = SQLAlchemy(app)


# def get_probands(items, offset=0, per_page=12):
#     return items[offset: offset + per_page]


# def create_proband(firstname: str, lastname: str, email: str, gender: str, birthday: datetime, height: float,
#                    weight: float, health: float, isactive: bool) -> Proband:
#     """
#     Create a Proband instance and add it to the database.
#
#     :param health:
#     :param isactive:
#     :param weight:
#     :param height:
#     :param birthday:
#     :param gender:
#     :param email:
#     :param lastname:
#     :param firstname: probands firstname
#     :return: a Proband instance or None
#     """
#
#     proband = Proband(firstname=firstname, lastname=lastname, email=email, gender=gender, birthday=birthday,
#                       height=height, weight=weight, health=health, isactive=isactive)
#     db.session.add(proband)
#     db.session.commit()
#     return proband


# def handle_error(e: Exception):
#     print("Action failed!")
#     print(e)


#
# def load_data_from_sql():
#     try:
#         with app.app_context():
#             # Überprüfen, ob bereits Daten in der Proband-Tabelle vorhanden sind
#             if not db.session.query(Proband.query.exists()).scalar():
#                 with open("Daten.sql", 'r', encoding='utf-8') as data_file:
#                     lines = data_file.readlines()
#
#                     current_table = ""
#
#                     for line in lines:
#                         line = line.strip()
#                         if line.startswith("-- "):
#                             current_table = line.replace("-- ", "").strip()
#
#                         if line and not line.startswith("--"):
#                             if current_table == "Probanden":
#                                 data = line.split(',')
#                                 country_id = randint(0, 26)
#                                 proband_data = {
#                                     "firstname": data[0].strip(),
#                                     "lastname": data[1].strip(),
#                                     "email": data[2].strip(),
#                                     "gender": data[3].strip(),
#                                     "birthday": data[4].strip(),  # assuming birthday format is correct
#                                     "weight": float(data[5].strip()),
#                                     "height": float(data[6].strip()),
#                                     "health": float(data[7].strip()),
#                                     "isactive": bool(data[8].strip())
#                                 }
#                                 try:
#                                     proband = ProbandCreate(**proband_data)
#                                     create_proband(proband)
#                                 except ValidationError as e:
#                                     print(f"Validation failed for data: {proband_data}")
#                                     print(e)
#     except Exception as e:
#         print(f"Error loading data from Daten.sql: {e}")
#

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


# @app.route('/probands', methods=['POST', 'GET'])
# def probands():
#     if request.method == 'GET':
#         # total = 20
#         page, per_page, offset = get_page_args(page_parameter="page",
#                                                per_page_parameter="per_page")
#         genders = Gender.query.all()
#         probands = Proband.query.filter(Proband.isActive.is_(True)).all()
#         total = len(probands)
#         pagination_probands = get_probands(probands, offset=offset, per_page=per_page)
#         pagination = Pagination(page=page, per_page=per_page, total=total,
#                                 css_framework='bootstrap4')
#         return render_template('probands.html', probandsList=pagination_probands, genders=genders, page=page,
#                                per_page=per_page,
#                                pagination=pagination)
#     else:
#         return render_template('probands.html')

# @app.route('/probands', methods=['POST', 'GET'])
# def probands():
#     if request.method == 'GET':
#         page, per_page, offset = get_page_args(page_parameter="page",
#                                                per_page_parameter="per_page")
#         genders = Gender.query.all()
#         probands = crud.get_active_probands()
#         total = len(probands)
#         pagination_probands = crud.get_probands_with_pagination(probands, offset=offset, per_page=per_page)
#         pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
#         return render_template('probands.html', probandsList=pagination_probands, genders=genders, page=page,
#                                per_page=per_page, pagination=pagination)
#     else:
#         return render_template('probands.html')

@app.route('/probands', methods=['POST', 'GET'])
def probands():
    if request.method == 'GET':
        page, per_page, offset = get_page_args(page_parameter="page",
                                               per_page_parameter="per_page")

        # get all genders
        genders = crud.get_all_genders()

        # get all active probands and count them
        probands = crud.get_all_active_probands()

        total = len(probands)

        # get paginated probands
        pagination_probands = crud.get_probands_with_pagination(probands, offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
        return render_template('probands.html', probandsList=probands, genders=genders, page=page,
                               per_page=per_page, pagination=pagination)

    else:
        return render_template('probands.html')


def determine_search_string():
    search_str = request.form.get('search_probands')
    if session['search'] is None or session['search'] == "":
        session['search'] = search_str
    elif session['search']:
        search_str = session['search']
    return search_str if search_str else ""


# route to search for existing probands
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
    # TODO: only search for active probands
    probands = Proband.query.filter(Proband.lastname.like(formatted_search)).all()

    genders = Gender.query.all()
    total = len(probands)
    pagination_probands = get_probands(probands, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('/probands.html', probandsList=pagination_probands, genders=genders, page=page,
                           per_page=per_page,
                           pagination=pagination, search=search_str)


# route to delete existing proband (use crud)
@app.route("/delete", methods=["POST"])
def delete():
    try:
        email = request.form.get("email")
        crud.delete_proband_by_email(email)
        return redirect(url_for('probands'))
    except Exception as e:
        handle_error(e)
        return redirect(url_for('index'))


# route to update existing proband
@app.route("/update", methods=["POST"])
def update():
    # TODO: add validation??
    # TODO: clean up code
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
        # TODO: add divers gender and more
        with get_db() as db:
            all_genders_in_database = db.query(Gender).all()
            try:
                medi = db.query(Gender).filter(Gender.name == medi).first()
                newmedi = medi.id
                print("newgender")
                print(newmedi)
                proband = db.query(Proband).filter(Proband.email == oldemail).first()

                updated_proband = Proband(firstName=newfirstname, lastName=newlastname, email=newemail, genderId=medi,
                                          birthday=newbirthday,
                                          weight=newweight, height=newheight, health=newhealth,
                                          countryId=proband.countryId,
                                          isActive=proband.isActive)

                proband.lastName = newlastname
                proband.firstName = newfirstname
                proband.email = newemail
                proband.genderId = newmedi
                proband.birthday = newbirthday
                proband.weight = newweight
                proband.height = newweight
                proband.health = newhealth

                db.commit()
                return redirect(url_for('probands'))

            except Exception as gender_not_in_databas:
                handle_error(gender_not_in_databas)
                print(f"Gender not found in database")
                return redirect(url_for('index'))

        # if medi == 'M':
        #     medi = 1
        # else:
        #     medi = 2
        # p = Proband.query.filter_by(email=oldemail).first()
        # p.firstname = newfirstname
        # p.lastname = newlastname
        # p.email = newemail
        # p.gender = medi
        # p.birthday = newbirthday
        # p.height = newheight
        # p.weight = newweight
        # p.health = newhealth
        # db.session.commit()
        # return redirect(url_for('probands'))

    except Exception as e:
        handle_error(e)
        return redirect(url_for('index'))


# route to add new proband
@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        try:
            # TODO: add divers gender and more
            medi = request.form.get("genselect")
            if medi == 'M':
                medi = 1
            else:
                medi = 2

            crud.create_proband(request.form.get("firstname"), request.form.get("lastname"),
                                request.form.get("email"), medi, request.form.get("birthday"),
                                request.form.get("height"), request.form.get("weight"), request.form.get("health"),
                                sqlalchemy.true())

            # crud.create_proband("fghj", "zuio",
            #                     "ghjk", medi, "01.01.2000",
            #                     "30", "20", "1",
            #                     sqlalchemy.true())
            return redirect(url_for('index'))
        except Exception as e:
            handle_error(e)
            return render_template('/probands.html')
    else:
        return render_template('/probands.html')


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


# route for openai chatbot
# @app.route("/generate", methods=["POST", "GET"])
# def generate():
#     question = request.args.get("question", "")
#     question = str(question).strip()
#     context = request.args.get("context", "")
#     context = str(context).strip()
#     data = ''
#     if question:
#         def stream():
#             openai.api_key = openai_api_key
#             messages = create_messages(question, context)
#             response = openai.ChatCompletion.create(
#                 model="gpt-4",
#                 messages=messages,
#                 temperature=0.7,  # Kreativität der Generierung; zufällig Generierung nächster Token
#                 # Eingabe werden in Tokens unterteilt, die dann in Vektoren umgewandelt werden
#                 # max_tokens=1000,
#                 stream=True,
#                 top_p=1,  # Alternative zu temperature
#             )
#             for trunk in response:
#                 if trunk['choices'][0]['finish_reason'] is not None:
#                     data = '[DONE]'
#                 else:
#                     data = trunk['choices'][0]['delta'].get('content', '')
#                 yield "data: %s\n\n" % data.replace("\n", "<br>")
#
#         return flask.Response(stream(), mimetype="text/event-stream")
#     return render_template('generate.html')


# route for home
@app.route('/')
def index():  # put application's code here
    return render_template('home.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    return render_template('registration.html')


@app.route('/report', methods=["GET", "POST"])
def report():
    if request.method == 'GET':
        page, per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")

        # Get all genders
        genders = crud.get_all_genders()

        # Get all probands
        probands = crud.get_all_active_probands()

        # Filter active and inactive probands
        active_probands = [proband for proband in probands if proband.isActive]
        inactive_probands = [proband for proband in probands if not proband.isActive]

        # Calculate total probands and counts
        total_probands = len(probands)
        total_active_probands = len(active_probands)
        total_inactive_probands = len(inactive_probands)

        # Calculate standard deviations
        stddev_weight = crud.calculate_stddev_weight()
        stddev_height = crud.calculate_stddev_height()

        # Create report data
        report_data = {
            'total_probands': total_probands,
            'total_active_probands': total_active_probands,
            'total_inactive_probands': total_inactive_probands,
            'stddev_weight': stddev_weight,
            'stddev_height': stddev_height
        }

        print(report_data)

        return render_template('report.html', report=report_data)

    else:
        return render_template('report.html')


if __name__ == "__main__":
    # load initial data if database is empty
    crud.load_initial_data()

    # run the app
    app.run(debug=True, port=8080)
