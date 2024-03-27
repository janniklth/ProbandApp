from random import randint, sample
from typing import List

from email_validator import validate_email, EmailNotValidError
from sqlalchemy import func, inspect, text

from app.db.session import get_db, engine
from models.country import Country
from models.diseases import Diseases
from models.gender import Gender
from models.medication import Medication
from models.proband import Proband
from models.probandDiseases import ProbandDiseases
from models.probandMedication import ProbandMedication


def get_all_active_probands():
    with get_db() as db:
        return db.query(Proband).filter(Proband.is_active == 1).all()


def get_all_genders():
    with get_db() as db:
        return db.query(Gender).all()


def get_gender_id(gender_name):
    try:
        with get_db() as db:
            gender = db.query(Gender).filter(Gender.name == gender_name).first()
            gender_id = gender.id
            return gender_id
    except Exception as invalid_gender_name:
        print(f"Gender name not found in database!")
        handle_error(invalid_gender_name)


def get_proband_by_id(proband_id):
    with get_db() as db:
        return db.query(Proband).filter(Proband.id == proband_id).first()


def update_proband(oldemail, newlastname, newfirstname, newemail, newgendername, newbirthday, newweight, newheight,
                   newhealth):
    with get_db() as db:

        try:
            gender_id = get_gender_id(newgendername)
            proband = db.query(Proband).filter(Proband.email == oldemail).first()
            proband.last_name = newlastname
            proband.first_name = newfirstname
            proband.email = newemail
            proband.gender_id = gender_id
            proband.birthday = newbirthday
            proband.weight = newweight
            proband.height = newheight
            proband.health = newhealth

            db.commit()
        except Exception as e:
            handle_error(e)


def create_proband(_first_name, _last_name, _email, _gender, _birthday, _weight, _height, _health="1.0", _is_active=1):
    with get_db() as db:
        try:
        # generate random country
            _countryId = randint(0, 26)

        # create new proband and add it to the db
            proband = Proband(first_name=_first_name, last_name=_last_name, email=_email, gender_id=_gender, birthday=_birthday,
                          weight=_weight, height=_height, health=_health, country_id=_countryId, is_active=_is_active)

            db.add(proband)
            db.commit()
        except Exception as mannnnn:
            print(f"Proband couldnt be added")

        # generate between 1 and 5 unique random diseases
        try:
            # Lese alle Krankheiten aus der Datenbank
            _all_diseases = db.query(Diseases).all()

            # Extrahiere die IDs der Krankheiten und speichere sie in einem Array
            disease_ids = [disease.id for disease in _all_diseases]  # TODO: get diseases from db
            num_diseases = randint(1, 5)
            random_diseases = sample(disease_ids, num_diseases)

            # add diseases to db
            for disease in random_diseases:
                db.add(ProbandDiseases(proband_id=proband.id, sickness_id=disease))
                db.commit()
        except Exception as noDisease:
            print(f" {noDisease}")

        # assign medication to proband
        medications_for_proband = get_medications_for_proband(proband.id)
        for medication in medications_for_proband:
            db.add(ProbandMedication(proband_id=proband.id, medication_id=medication))
            db.commit()

        return proband


def delete_proband_by_email(proband_email):
    with get_db() as db:
        proband = db.query(Proband).filter(Proband.email == proband_email).first()
        if proband:
            proband.is_active = 0
            db.commit()
            return True
        return False


def create_country(_countrycode, _name):
    with get_db() as db:
        country = Country(countrycode=_countrycode, name=_name)
        db.add(country)
        db.commit()
        return country


def create_gender(_name):
    with get_db() as db:
        gender = Gender(name=_name)
        db.add(gender)
        db.commit()
        return gender


def create_medication(_name):
    with get_db() as db:
        medication = Medication(name=_name)
        db.add(medication)
        db.commit()
        return medication


def create_diseases(_name):
    with get_db() as db:
        disease = Diseases(name=_name)
        db.add(disease)
        db.commit()
        return disease


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
                                    create_diseases(line.strip("'"))

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
                    find_duplicates()
                    # validate_proband_email()

        except Exception as kabut:
            print(f" {kabut}")


def get_diseases_for_proband(proband_id: int) -> List[int]:
    """Retrieve diseases associated with a specific proband."""
    with get_db() as db:
        all_diseases = db.query(ProbandDiseases).filter(ProbandDiseases.proband_id == proband_id)
        disease_ids = [disease.sickness_id for disease in all_diseases]
    return disease_ids


def get_medications_for_diseases(diseases: List[int]) -> List[int]:
    """Determine medications based on diseases."""
    # Mapping of diseases to medications
    medication_mapping = {
        (1, 2, 3, 4, 5): [6, 1],
        # Rückenschmerzen, Bluthochdruck, Fehlsichtigkeit, Fettstoffwechselstörung, Grippe -> Supix, Wirknix
        (1, 4, 5): [2],  # Rückenschmerzen, Fettstoffwechselstörung, Grippe -> Machmichfix
        (2, 4): [4, 5],  # Bluthochdruck, Fettstoffwechselstörung -> Gesundix, Kannix
        (3,): [7],  # Fehlsichtigkeit -> Istnix
        (): [3]  # Sonst -> Tutnix
    }

    for diseases_combination, medications in medication_mapping.items():
        if set(diseases) == set(diseases_combination):
            return medications
    return [3]  # If no combination is found, return "Tutnix"


def get_medications_for_proband(proband_id: int) -> List[int]:
    """Determine medications for a proband based on their diseases."""
    diseases = get_diseases_for_proband(proband_id)
    medications = get_medications_for_diseases(diseases)
    return medications


# TODO: implement duplicates function
def find_duplicates():
    with (get_db() as db):
        subquery = db.query(Proband.email, func.count(Proband.email).label("email_count")).group_by(
            Proband.email).having(func.count(Proband.email) > 1).subquery()

        duplicated_probands = db.query(Proband).join(subquery, Proband.email == subquery.c.email).all()

        for proband in duplicated_probands:
            print(
                f"DOPPELLT! ID: {proband.id}, Email: {proband.email}, Proband: {proband.first_name} {proband.last_name}")

        return duplicated_probands


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


# TODO: get gender id from database
def calculate_stddev_male_height():
    with get_db() as db:
        std = db.query(func.stddev(Proband.height)).filter(Proband.gender_id == 1).scalar()
        return std if std else 0.0


# TODO: get gender id from database
def calculate_stddev_female_height():
    with get_db() as db:
        std = db.query(func.stddev(Proband.height)).filter(Proband.gender_id == 2).scalar()
        return std if std else 0.0


# TODO: get gender id from database
def calculate_stddev_male_weight():
    with get_db() as db:
        std = db.query(func.stddev(Proband.weight)).filter(Proband.gender_id == 1).scalar()
        return std if std else 0.0


# TODO: get gender id from database
def calculate_stddev_female_weight():
    with get_db() as db:
        std = db.query(func.stddev(Proband.weight)).filter(Proband.gender_id == 2).scalar()
        return std if std else 0.0


def calculate_avg_weight():
    with get_db() as db:
        avg = db.query(func.avg(Proband.weight)).scalar()
        return avg if avg else 0.0


def calculate_avg_height():
    with get_db() as db:
        avg = db.query(func.avg(Proband.height)).scalar()
        return avg if avg else 0.0


# TODO: get gender id from database
def calculate_avg_male_height():
    with get_db() as db:
        avg = db.query(func.avg(Proband.height)).filter(Proband.gender_id == 1).scalar()
        return avg if avg else 0.0


# TODO: get gender id from database
def calculate_avg_female_height():
    with get_db() as db:
        avg = db.query(func.avg(Proband.height)).filter(Proband.gender_id == 2).scalar()
        return avg if avg else 0.0


# TODO: get gender id from database
def calculate_avg_male_weight():
    with get_db() as db:
        avg = db.query(func.avg(Proband.weight)).filter(Proband.gender_id == 1).scalar()
        return avg if avg else 0.0


# TODO: get gender id from database
def calculate_avg_female_weight():
    with get_db() as db:
        avg = db.query(func.avg(Proband.weight)).filter(Proband.gender_id == 2).scalar()
        return avg if avg else 0.0


def validate_proband_email():
    with get_db() as db:
        all_probands = db.query(Proband).all()
        for proband in all_probands:
            try:
                v = validate_email(proband.email)
            except EmailNotValidError as e:
                print(f"Proband {proband.id} email is not a valid email: {str(e)}")


def run_sql_script():
    with engine.connect() as conn:
        print("Running SQL script...")
        with open("initial.sql", 'r') as file:
            content = file.read()
            commands = content.split(';')
            transaction = conn.begin()
            try:
                for command in commands:
                    # Entfernen von DELIMITER-Anweisungen und Leerraum
                    command = command.strip()
                    if command and not command.startswith('DELIMITER'):
                        conn.execute(text(command))
                transaction.commit()
            except Exception as e:
                print(f"Error occurred: {e}")
                transaction.rollback()
            else:
                print("Script executed successfully.")
