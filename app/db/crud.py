from random import randint

from pydantic import ValidationError
from sqlalchemy import func, inspect, true

from app.db.session import get_db, engine
from models.country import Country
from models.medication import Medication
from models.proband import Proband
from models.gender import Gender
from models.sickness import Sickness

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


def create_proband(_firstName, _lastName, _email, _gender, _birthday, _weight, _height, _health="1.0", _isActive=1):
    with get_db() as db:
        country_id = randint(0, 26)
        proband = Proband(firstName=_firstName, lastName=_lastName, email=_email, genderId=_gender, birthday=_birthday,
                          weight=_weight, height=_height, health=_health, countryId=country_id, isActive=_isActive)
        print("created new proband : " + proband.firstName)
        db.add(proband)
        db.commit()
        return proband


def create_country(_countrycode, _name):
    with get_db() as db:
        country = Country(countrycode=_countrycode, name=_name)
        print("created new country : " + country.name)
        db.add(country)
        db.commit()
        return country


def create_gender(_name):
    with get_db() as db:
        gender = Gender(name=_name)
        print("created new gender : " + gender.name)
        db.add(gender)
        db.commit()
        return gender


def create_medication(_name):
    with get_db() as db:
        medication = Medication(name=_name)
        print("created new medication : " + medication.name)
        db.add(medication)
        db.commit()
        return medication


def create_sickness(_name):
    with get_db() as db:
        sickness = Sickness(name=_name)
        print("created new medication : " + sickness.name)
        db.add(sickness)
        db.commit()
        return sickness


def load_initial_data():
    with get_db() as db:
        try:
            inspector = inspect(engine)
            available_tables = inspector.get_table_names()

            if "PROBAND" in available_tables:
                count = db.query(Proband).count()
                if count < 1:
                    print("no data in proband table yet")
                    with open("Daten.sql", 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        current_table = ""

                        for line in lines:
                            line = line.strip()
                            if line.startswith("-- "):
                                current_table = line.replace("-- ", "").strip()

                            if line and not line.startswith("--"):
                                if current_table == "Medikament":
                                    create_medication(line.strip("'"))
                                elif current_table == "Krankheit":
                                    create_sickness(line.strip("'"))

                                elif current_table == "Geschlecht":
                                    create_gender(line.strip("'"))
                                elif current_table == "Länder":
                                    create_country(line.split(", ")[0].strip("'"), line.split(", ")[1].strip("'"))
                                elif current_table == "Probanden":
                                    line = line.split(", ")
                                    if line[3].strip("'") == 'M':
                                        gender = 1
                                    elif line[3].strip("'") == 'F':
                                        gender = 2
                                    elif line[3].strip("'") == 'D':
                                        gender = 3

                                    create_proband(line[0].strip("'"), line[1].strip("'"),
                                                   line[2].strip("'"), gender,
                                                   line[4].strip("'"), line[5].strip("'"),
                                                   line[6].strip("'"))

                        db.commit()
                    print("we seeded the db succesfully")

                else:
                    print("proband table already filled with data")

        except Exception as kabut:
            print(f" {kabut}")


# TODO: implement duplicates function
def find_duplicates():
    pass


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
