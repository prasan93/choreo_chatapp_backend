from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os
import bcrypt 

Base = declarative_base()

# Load environment variables from .env file
load_dotenv()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    user_name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    new_password = Column(String, nullable=False)
    old_password = Column(String, nullable=False)

    def to_dict(self):
        user_dict = {
            'id': self.id,
            'full_name': self.full_name,
            'user_name': self.user_name,
            'email': self.email,
            'new_password': self.new_password,
            'old_password': self.old_password
        }
        return user_dict

    @classmethod
    def add_new_record(cls, fullname, user_name, email, password):
        try:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            new_user = cls(
                full_name=fullname,
                user_name=user_name,
                email=email,
                new_password=password_hash,
                old_password=password,
            )
            session.add(new_user)
            session.commit()
            return new_user
        except IntegrityError as e:
            session.rollback()  # Rollback the transaction
            error_message = str(e.orig)
            # Check if the error is due to unique constraint violation on email
            if 'users_email_key' in error_message:
                raise ValueError("Email already exists")
            else:
                raise ValueError("An error occurred while adding the user")

    @classmethod
    def get_user_by_id(cls, user_id):
        user = session.query(cls).filter_by(id=user_id).first()
        return user.to_dict() if user else {}

    @classmethod
    def get_user_by_credentials(cls, user_name, password):
        user = session.query(cls).filter_by(user_name=user_name).first()
        if user:
            # Retrieve the hashed password from the user object
            stored_password_hash = user.new_password
            # Check if the provided password matches the hashed password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                return user.to_dict()
        return {}


# Construct PostgreSQL connection URI using environment variables
DB_NAME = os.getenv('DB_NAME')
USER = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')

# Construct PostgreSQL connection URI
DB_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'

# Configure SQLAlchemy engine and session
engine = create_engine(DB_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
