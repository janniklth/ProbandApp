from app import db
from models.proband import Proband
from models.gender import Gender


def get_all_probands():
    return db.session.query(Proband).all()


def get_proband_by_id(proband_id):
    return db.session.query(Proband).filter(Proband.id == proband_id).first()


def get_proband_by_name(name):
    return db.session.query(Proband).filter(Proband.name == name).first()


def create_proband(_firstName, _lastName, _email, _gender, _birthday, _height, _weight, _health, _isActive):
    proband = Proband(firstName=_firstName, lastName=_lastName, email=_email, gender=_gender, birthday=_birthday,
                      height=_height, weight=_weight, health=_health, isActive=_isActive)
    db.session.add(proband)
    db.session.commit()
    return proband


def load_initial_data():
    pass


def handle_error(e):
    print("Action failed!")
    print(e)
