from dataclasses import dataclass
from flask_login import UserMixin


@dataclass
class Blog:
    """
    Blog class representing a blog entry in the application.

    Attributes:
        blog_id (int): The unique identifier for the blog.
        title (str): The title of the blog.
        subtitle (str): The subtitle of the blog.
        date (datetime): The date the blog was created or published.
        author (str): The author of the blog. This can be enhanced to store the user object.
        img_url (str): The URL to the image associated with the blog.
        body (str): The main content of the blog.
        user_id (int): The ID of the user who created the blog.
    """
    blog_id: int
    title: str
    subtitle: str
    date: str
    author: str
    img_url: str
    body: str
    user_id: int


@dataclass
class User(UserMixin):
    """
    User class representing a user entity in the application.
    It inherits from `UserMixin`, which provides
    default implementations of methods required by Flask-Login for user authentication
    and session management.

    Attributes:
        user_id (int): The unique identifier for the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user, used for login.
        password (str): The hashed password of the user, used for authentication.
    """

    user_id: int
    first_name: str
    last_name: str
    email: str
    password: str

    def get_id(self):
        try:
            return str(self.user_id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None
