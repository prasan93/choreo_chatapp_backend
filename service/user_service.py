from datetime import datetime
from db.models.user import User

class UserService:
    @staticmethod
    def create_new_user_record(
        fullname: str,
        user_name: str,
        email: str,
        password: str,
    ):
        
        return User.add_new_record(
            fullname=fullname,
            user_name=user_name,
            email=email,
            password=password,
        )

    @staticmethod
    def get_user_by_id(user_id: str):
        return User.get_user_by_id(user_id=user_id)

    @staticmethod
    def get_user_by_credentials(user_name: str, password: str):
        return User.get_user_by_credentials(user_name=user_name, password=password)
