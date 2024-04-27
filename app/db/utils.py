from email_validator import validate_email, EmailNotValidError

from db.crud import get_probands_age_filtered

from sqlalchemy import func

from app.models.proband import Proband


### - - - - Helper functions for calculating the average values and standard derivations of the probands - - - - ###

def calculate_stddev_weight():
    stddev = get_probands_age_filtered(func.stddev(Proband.weight), None)
    return stddev if stddev else 0.0


def calculate_stddev_height():
    stddev = get_probands_age_filtered(func.stddev(Proband.height), None)
    return stddev if stddev else 0.0


# TODO: get gender id from database
def calculate_stddev_male_height():
    stddev = get_probands_age_filtered(func.stddev(Proband.height), 1)
    return stddev if stddev else 0.0


# TODO: get gender id from database
def calculate_stddev_female_height():
    stddev = get_probands_age_filtered(func.stddev(Proband.height), 2)
    return stddev if stddev else 0.0


# TODO: get gender id from database
def calculate_stddev_male_weight():
    stddev = get_probands_age_filtered(func.stddev(Proband.weight), 1)
    return stddev if stddev else 0.0


# TODO: get gender id from database
def calculate_stddev_female_weight():
    stddev = get_probands_age_filtered(func.stddev(Proband.weight), 2)
    return stddev if stddev else 0.0


def calculate_avg_weight():
    avg = get_probands_age_filtered(func.avg(Proband.weight), None)
    return avg if avg else 0.0


def calculate_avg_height():
    avg = get_probands_age_filtered(func.avg(Proband.height), None)
    return avg if avg else 0.0


# TODO: get gender id from database
def calculate_avg_male_height():
    avg = get_probands_age_filtered(func.avg(Proband.height), 1)
    return avg if avg else 0.0


# TODO: get gender id from database
def calculate_avg_female_height():
    avg = get_probands_age_filtered(func.avg(Proband.height), 2)
    return avg if avg else 0.0


# TODO: get gender id from database
def calculate_avg_male_weight():
    avg = get_probands_age_filtered(func.avg(Proband.weight), 1)
    return avg if avg else 0.0


# TODO: get gender id from database
def calculate_avg_female_weight():
    avg = get_probands_age_filtered(func.avg(Proband.weight), 2)
    return avg if avg else 0.0



### - - - - Helper functions for adjusting the average values of the probands - - - - ###
def adjust_male_avg_weight(wanted_avg_weight):
    # get current average and calculate difference
    avg = calculate_avg_male_weight()
    diff = wanted_avg_weight - avg


def adjust_male_avg_height(wanted_avg_height):
    # get current average
    avg = calculate_avg_male_height()
    diff = wanted_avg_height - avg


def adjust_female_avg_weight(wanted_avg_weight):
    # get current average
    avg = calculate_avg_female_weight()
    diff = wanted_avg_weight - avg


def adjust_female_avg_height(wanted_avg_height):
    # get current average
    avg = calculate_avg_female_height()
    diff = wanted_avg_height - avg


def validate_mail_new_proband(_new_mail):
    try:
        v = validate_email(_new_mail)
        return v
    except EmailNotValidError as e:
        print("new proband mail is not valid!")
        return e

def handle_error(e):
    print("Action failed!")
    print(e)