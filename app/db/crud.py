from sqlalchemy import func

from app.db.session import get_db
from models.proband import Proband
from models.gender import Gender


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
        proband = Proband(firstName=_firstName, lastName=_lastName, email=_email, gender=_gender, birthday=_birthday,
                          height=_height, weight=_weight, health=_health, isActive=_isActive)
        db.add(proband)
        db.commit()
        return proband


# TODO: Annika, please implement the following method
def load_initial_data():
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
