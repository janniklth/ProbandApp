import sqlalchemy

from flask import render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
from flask_paginate import Pagination, get_page_args
from flask_sqlalchemy import SQLAlchemy

import os
from flask import Flask
import json

from app.db import crud
from app.db.utils import handle_error
from app.db import utils

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

# determine search string from form
def determine_search_string():
    search_str = request.form.get('search_probands')
    if session['search'] is None or session['search'] == "":
        session['search'] = search_str
    elif session['search']:
        search_str = session['search']
    return search_str if search_str else ""


# determine search category from form
def determine_search_category():
    search_category = request.form.get('search_field')
    if session['search_category'] is None or session['search_category'] == "":
        session['search_category'] = search_category
    elif session['search_category']:
        search_category = session['search_category']
    return search_category if search_category else ""


### - - - - - - - Routes - - - - - - - ###

# route to get all probands
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
        return render_template('probands.html', probandsList=pagination_probands, genders=genders, page=page,
                               per_page=per_page, pagination=pagination)

    else:
        return render_template('probands.html')


# route to search for existing probands
@app.route('/search', methods=['POST', 'GET'])
def search():
    page, per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")
    if request.method == "POST":
        session['search'] = ""
        session['search_category'] = ""

    # get search string and category to search in
    search_category = determine_search_category()
    search_str = determine_search_string()

    # search for probands matching the search criteria
    search_result = crud.search_probands(search_str, search_category)
    print("search string: ", search_str)
    print("search category: ", search_category)
    print("search result: ", search_result)

    genders = crud.get_all_genders()

    if search_result is None:
        total = 0
    else:
        total = len(search_result)

    pagination_probands = crud.get_probands_with_pagination(search_result, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('probands.html', probandsList=pagination_probands, genders=genders, page=page,
                           per_page=per_page, pagination=pagination)


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
    try:
        oldemail = request.form.get("oldemail")
        newlastname = request.form.get("newlastname")
        newfirstname = request.form.get("newfirstname")
        newemail = request.form.get("newemail")
        newbirthday = request.form.get("newbirthday")
        newweight = request.form.get("newweight")
        newheight = request.form.get("newheight")
        newhealth = request.form.get("newhealth")
        newgender = request.form.get("genselect")

        crud.update_proband(oldemail, newlastname, newfirstname, newemail, newgender,
                            newbirthday, newweight, newheight, newhealth)

        return render_template('/probands.html')

    except Exception as e:
        handle_error(e)
        return redirect(url_for('index'))


# route to add new proband
@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        try:
            valid_mail = utils.validate_mail_new_proband(request.form.get("email"))
            if isinstance(valid_mail, Exception):
                return render_template('/error.html', error_message=valid_mail)

            else:

                gender_id = crud.get_gender_id(request.form.get("genselect"))

                crud.create_proband(request.form.get("firstname"), request.form.get("lastname"),
                                    request.form.get("email"), gender_id, request.form.get("birthday"),
                                    request.form.get("height"), request.form.get("weight"),
                                    request.form.get("health"),
                                    sqlalchemy.true())

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
        active_probands = crud.get_all_active_probands()
        inactive_probands = crud.get_all_inactive_probands()

        # Calculate total probands and counts
        total_probands = len(active_probands) + len(inactive_probands)
        total_active_probands = len(active_probands)
        total_inactive_probands = len(inactive_probands)

        # Calculate standard deviations
        stddev_weight = round(utils.calculate_stddev_weight(), 3)
        stddev_height = round(utils.calculate_stddev_height(), 3)
        stddev_height_male = round(utils.calculate_stddev_male_height(), 3)
        stddev_height_female = round(utils.calculate_stddev_female_height(), 3)
        stddev_weight_male = round(utils.calculate_stddev_male_weight(), 3)
        stddev_weight_female = round(utils.calculate_stddev_female_weight(), 3)

        # Calculate averages
        avg_height = round(utils.calculate_avg_height(), 2)
        avg_height_male = round(utils.calculate_avg_male_height(), 2)
        avg_height_female = round(utils.calculate_avg_female_height(), 2)
        avg_weight = round(utils.calculate_avg_weight(), 2)
        avg_weight_male = round(utils.calculate_avg_male_weight(), 2)
        avg_weight_female = round(utils.calculate_avg_female_weight(), 2)

        # Create report data
        report_data = {
            'total probands': total_probands,
            'total active probands': total_active_probands,
            'total inactive probands': total_inactive_probands,
            'stddev height': stddev_height,
            'stddev height male': stddev_height_male,
            'stddev height female': stddev_height_female,
            'stddev weight': stddev_weight,
            'stddev weight male': stddev_weight_male,
            'stddev weight female': stddev_weight_female,
            'avg height': avg_height,
            'avg height male': avg_height_male,
            'avg height female': avg_height_female,
            'avg weight': avg_weight,
            'avg weight male': avg_weight_male,
            'avg weight female': avg_weight_female
        }

        # TODO: add adjusted data
        return render_template('report.html', old_report=report_data, adjusted_report=report_data)

    else:
        return render_template('report.html')


if __name__ == "__main__":

    # create tables and load initial data
    print("running sql script")
    crud.run_sql_script()
    print("running initial data")
    crud.load_initial_data()

    # adjust average height and weight for male and female
    utils.adjust_avg_height_weight()

    # run the app
    app.run(debug=True, port=8080)
