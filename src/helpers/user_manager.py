from src.database.mysql_manager import MysqlManager
from dataclasses import dataclass
from src.helpers.models import User


@dataclass
class UserManager(MysqlManager):

    def add(self, email: str, first_name: str, last_name: str, hashed_password: str) -> bool:
        """
        Add a new user to the database with the provided email, first name, last name, and hashed password.

        Args:
            email (str): The email of the new user.
            first_name (str): The first name of the new user.
            last_name (str): The last name of the new user.
            hashed_password (str): The hashed password of the new user.

        Returns:
            bool: True if the user is successfully added to the database, False otherwise.
        """
        return self.sql_add_user(email, first_name, last_name, hashed_password)

    def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email from the database and return a User instance.

        Args:
            email (str): The email of the user to be retrieved.

        Returns:
            User | None: An instance of the User class if the user is found, or None if the user does not exist.
        """
        user_data = self.sql_get_user_by_email(email)
        if user_data:
            return user_data
        return None

    def get_by_id(self, user_id: int) -> User | None:
        """
        Retrieve a user by their ID from the database and return a User instance.

        Args:
            user_id (int): The ID of the user to be retrieved.

        Returns:
            User | None: An instance of the User class if the user is found, or None if the user does not exist.
        """
        user_data = self.sql_get_user_by_id(user_id)
        if user_data:
            return user_data
        return None
