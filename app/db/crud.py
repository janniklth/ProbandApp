from random import randint

from pydantic import ValidationError
from sqlalchemy import func

from app.db.session import get_db
from models.proband import Proband
from models.gender import Gender

from schemas.proband import Proband as ProbandSchema
from schemas.gender import Gender as GenderSchema
from schemas.proband import ProbandCreate


def get_all_active_probands():
    with get_db() as db:
        return db.query(Proband).all()


def get_all_genders():
    with get_db() as db:
        return db.query(Gender).all()


def get_proband_by_id(proband_id):
    with get_db() as db:
        return db.query(Proband).filter(Proband.id == proband_id).first()


def create_proband(_firstName, _lastName, _email, _gender, _birthday, _height, _weight, _health, _isActive):
    with get_db() as db:
        country_id = randint(0, 26)
        proband = Proband(firstName=_firstName, lastName=_lastName, email=_email, gender=_gender, birthday=_birthday,
                          height=_height, weight=_weight, health=_health, countryId=country_id, isActive=_isActive)
        print("created new proband : " + proband.firstName)
        db.add(proband)
        db.commit()
        return proband


# TODO: Annika, please implement the following method

def load_initial_data():
    pass
    # try:
    #     with get_db().engine.connect() as conn:
    #         # with open("initial.sql", 'r') as file:
    #         #     content = file.read()
    #         #     transaction = conn.begin()
    #         #     try:
    #         #         for command in content.split(";"):
    #         #             if command.strip() != "":
    #         #                 conn.execute(text(command))
    #         #         transaction.commit()
    #         #     except Exception as alleskaputt:
    #         #         print(f"Command skipped: {command}")
    #         #         print(alleskaputt)
    #         #         transaction.rollback()
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
    #

def handle_error(e):
    print("Action failed!")
    print(e)


# TODO: Seperate following methods in utils file

def get_probands_with_pagination(probands, offset=0, per_page=12):
    """
    Paginate a list of probands.

    :param probands: List of probands to paginate.
    :param offset: Offset for pagination.
    :param per_page: Number of probands per page.
    :return: Paginated list of probands.
    """
    return probands[offset: offset + per_page]


def calculate_stddev_weight():
    with get_db() as db:
        std = db.query(func.stddev(Proband.weight)).scalar()
        return std if std else 0.0


def calculate_stddev_height():
    with get_db() as db:
        std = db.query(func.stddev(Proband.height)).scalar()
        return std if std else 0.0
