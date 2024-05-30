from sqlalchemy.orm import Session
from sqlalchemy import select
from database import db
from models.user import User
from circuitbreaker import circuit
from werkzeug.security import generate_password_hash, check_password_hash
from utils.util import encode_token


def fallback_func(user_data):
    print('The fallback function is being executed')
    return None


def save(user_data):
    with Session(db.engine) as session:
        with session.begin():
            user_query = select(User).where(User.username == user_data['username'])
            user_check = session.execute(user_query).scalars().first()
            if user_check is not None:
                raise ValueError("User with that username already exists")
            new_user = User(name=user_data['name'], username=user_data['username'], password=generate_password_hash(user_data['password']))
            # Add and commit to the database
            session.add(new_user)
            session.commit()

        session.refresh(new_user)
        return new_user


def find_all():
    query = db.select(User)
    users = db.session.execute(query).scalars().all()
    return users


def get_token(username, password):
    query = db.select(User).where(User.username == username)
    user = db.session.execute(query).scalars().first()
    if user is not None and check_password_hash(user.password, password):
        auth_token = encode_token(user.id)
        return auth_token
    else:
        return None

def get_user(user_id):
    return db.session.get(User, user_id)