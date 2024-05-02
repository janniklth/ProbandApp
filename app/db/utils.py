from email_validator import validate_email, EmailNotValidError

from app.db.crud import get_probands_age_filtered, get_all_active_probands, get_all_inactive_probands, update_height, \
    update_weight, get_active_probands_by_gender

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

    # update all male probands
    for proband in get_active_probands_by_gender(gender_id=1):
        update_weight(proband.id, proband.weight + diff)


def adjust_male_avg_height(wanted_avg_height):
    # get current average
    avg = calculate_avg_male_height()
    diff = wanted_avg_height - avg

    # update all male probands
    for proband in get_active_probands_by_gender(gender_id=1):
        update_height(proband.id, proband.height + diff)


def adjust_female_avg_weight(wanted_avg_weight):
    # get current average
    avg = calculate_avg_female_weight()
    diff = wanted_avg_weight - avg

    # update all female probands
    for proband in get_active_probands_by_gender(gender_id=2):
        update_weight(proband.id, proband.weight + diff)


def adjust_female_avg_height(wanted_avg_height):
    # get current average
    avg = calculate_avg_female_height()
    diff = wanted_avg_height - avg

    # update all female probands
    for proband in get_active_probands_by_gender(gender_id=2):
        update_height(proband.id, proband.height + diff)


def adjust_avg_height_weight():
    # print current report
    print("- - - - - - - - - - - - Current report: - - - - - - - - - - - -")
    print_report()

    # adjust averages
    # adjust average weight and height for male and female probands
    adjust_male_avg_height(180.0)
    adjust_male_avg_weight(88.0)
    adjust_female_avg_height(167.0)
    adjust_female_avg_weight(69.0)

    # print adjusted report
    print("- - - - - - - - - - - - Adjusted report: - - - - - - - - - - - -")
    print_report()

    pass


def validate_mail_new_proband(_new_mail):
    try:
        v = validate_email(_new_mail)
        return v
    except EmailNotValidError as e:
        print("new proband mail is not valid!")
        return e


def print_report():
    # get total probands and counts
    total_active_probands = len(get_all_active_probands())
    total_inactive_probands = len(get_all_inactive_probands())
    total_probands = total_active_probands + total_inactive_probands

    # print standard deviations
    stddev_weight = round(calculate_stddev_weight(), 3)
    stddev_height = round(calculate_stddev_height(), 3)
    stddev_height_male = round(calculate_stddev_male_height(), 3)
    stddev_height_female = round(calculate_stddev_female_height(), 3)
    stddev_weight_male = round(calculate_stddev_male_weight(), 3)
    stddev_weight_female = round(calculate_stddev_female_weight(), 3)

    # print averages
    avg_height = round(calculate_avg_height(), 2)
    avg_height_male = round(calculate_avg_male_height(), 2)
    avg_height_female = round(calculate_avg_female_height(), 2)
    avg_weight = round(calculate_avg_weight(), 2)
    avg_weight_male = round(calculate_avg_male_weight(), 2)
    avg_weight_female = round(calculate_avg_female_weight(), 2)

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

    # print report dictionary
    for key, value in report_data.items():
        print(key, ":", value)


def handle_error(e):
    print("Action failed!")
    print(e)
