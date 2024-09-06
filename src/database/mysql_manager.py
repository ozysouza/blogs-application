from dataclasses import dataclass, field
from src.helpers.models import User, Blog
from src.helpers.log import Log

import mysql.connector as mysql
import os


@dataclass
class MysqlManager:
    """
    A class to represent a MySQL database connection and cursor.

    Attributes:
        db_host (str): The database host, retrieved from environment variables.
        db_user (str): The database user, retrieved from environment variables.
        db_passwd (str): The database password, retrieved from environment variables.
        myconnection: The MySQL database connection object.
        mycursor: The cursor object to execute queries.
    """
    logger = Log().logger
    db_host: str = os.getenv('MYSQL_HOST')
    db_user: str = os.getenv('MYSQL_USER')
    db_passwd: str = os.getenv('MYSQL_PASSWORD')
    db_name: str = os.getenv('MYSQL_DB_NAME')
    myconnection: mysql.connection.MySQLConnection = field(init=False)
    mycursor: mysql.connection.MySQLCursor = field(init=False)

    __connection_instance = None  # Singleton instance

    def __post_init__(self):
        """
        Initialize the database connection only if it has not been initialized yet.

        This ensures that the connection and cursor are set up correctly.
        """
        if MysqlManager.__connection_instance is None:
            try:
                self.myconnection = mysql.connect(
                    host=self.db_host,
                    user=self.db_user,
                    passwd=self.db_passwd
                )

                # Initialize the cursor object
                self.mycursor = self.myconnection.cursor()
                self.logger.info('Successfully connect yo Mysql server.')

                # Verify if the database exists, if not create it
                self._setup_database()

                # Connect to database 'USE database;'
                self.myconnection.database = self.db_name

                # Verify if the tables exists, if not create it
                self._setup_users_table()
                self._setup_blogs_table()

                # Set the instance to this object to maintain a single connection
                MysqlManager.__connection_instance = self
            except mysql.Error as err:
                self.logger.error(f'Error connecting to MySQL server: {err}')
        else:
            # Reuse the existing instance
            self.myconnection = MysqlManager.__connection_instance.myconnection
            self.mycursor = MysqlManager.__connection_instance.mycursor

    def _setup_database(self) -> bool:
        """
            Check if the database exists, and create it if it doesn't.
         :return:
            bool
        """
        try:
            self.mycursor.execute(f'SHOW DATABASES LIKE "{self.db_name}"')
            result = self.mycursor.fetchone()
            if not result:
                self.mycursor.execute(
                    f'CREATE DATABASE {self.db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci')
                self.logger.info(f'Database {self.db_name} created.')
            else:
                self.logger.info(f'Database {self.db_name} already exists.')
            return True
        except mysql.Error as err:
            self.logger.error(f'Error setting up database: {err}')
            return False

    def _setup_users_table(self):
        """
            Check if the required users table exist, and create them if they don't.
        :return:
            bool
        """
        try:
            self.mycursor.execute(f'SHOW TABLES LIKE "users"')
            result = self.mycursor.fetchone()
            if not result:
                self.mycursor.execute("""
                CREATE TABLE users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) UNIQUE KEY,
                    first_name VARCHAR(255),
                    last_name VARCHAR(255),
                    password VARCHAR(255)
                )
                """)
                self.logger.info('Table "users" created.')
            else:
                self.logger.info('Table "users" already exists.')
            return True
        except mysql.Error as err:
            self.logger.error(f'Error setting up tables: {err}')
            return False

    def _setup_blogs_table(self) -> bool:
        """
            Check if the required blogs table exist, and create them if they don't.
        :return:
            bool
        """
        try:
            self.mycursor.execute(f'SHOW TABLES LIKE "blogs"')
            result = self.mycursor.fetchone()
            if not result:
                self.mycursor.execute("""
                    CREATE TABLE blogs (
                        blog_id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255) UNIQUE KEY,
                        subtitle VARCHAR(255),
                        date VARCHAR(255),
                        author VARCHAR(255),
                        img_url VARCHAR(255),
                        body TEXT,
                        user_id INT,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                    )
                """)
                self.logger.info('Table "blogs" created.')
            else:
                self.logger.info('Table "blogs" already exists.')
            return True
        except mysql.Error as err:
            self.logger.error(f'Error setting up tables: {err}')
            return False

    def add_user(self, email: str, first_name: str, last_name: str, password: str) -> bool:
        """
        Insert the user into the database.
        Args:
            email (str): The email of the user.
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            password (str): The user's password.
          Returns:
              Boolean
        """
        try:
            self.mycursor.execute(f'USE {self.db_name}')
            query = ('INSERT INTO users (email, first_name, last_name, password)'
                     'VALUES (%s, %s, %s, %s)')
            self.mycursor.execute(query, (email, first_name, last_name, password))
            self.myconnection.commit()
            self.logger.info('User successfully inserted into database.')
            return True
        except mysql.Error as err:
            self.logger.error(f'Failed when add user into database: {err}')
            return False

    def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email from the database and return a User instance.

        Args:
            email (str): The email of the user to be retrieved.

        Returns:
            User | None: An instance of the User class if found, or None if the user does not exist.
        """
        try:
            query = 'SELECT * FROM users WHERE email = %s'
            self.mycursor.execute(query, (email,))
            result = self.mycursor.fetchone()
            if result:
                columns = [desc[0] for desc in self.mycursor.description]
                user_data = dict(zip(columns, result))
                # Convert dict to User object
                return User(**user_data)

            return None
        except mysql.Error as err:
            self.logger.error(f'Failed to retrieve user: {err}')
            return None

    def get_user_by_id(self, user_id: int) -> User | None:
        """
        Retrieve a user by their id from the database and return a User instance.

        Args:
            user_id (int): The email of the user to be retrieved.

        Returns:
            User | None: An instance of the User class if found, or None if the user does not exist.
        """
        try:
            query = 'SELECT * FROM users WHERE user_id = %s'
            self.mycursor.execute(query, (user_id, ))
            result = self.mycursor.fetchone()
            if result:
                columns = [desc[0] for desc in self.mycursor.description]
                user_data = dict(zip(columns, result))
                # Convert dict to User object
                return User(**user_data)

            return None
        except mysql.Error as err:
            self.logger.error(f'Failed to retrieve user: {err}')
            return None

    def add_blog(self, title: str, subtitle: str, date: str, author: str, img_url, body, user_id: int) -> bool:
        """
        Insert the blog into the database.
        Args:
            title (str): The title of the blog.
            subtitle (str): The subtitle of the blog.
            date (str): The date when the blog was posted.
            author (str): The Author of the blog.
            img_url (str): The image URL that will be displayed on the card.
            body (str): The content of the blog.
            user_id (int): The user ID who created the blog.
          Returns:
              Boolean
        """
        try:
            self.mycursor.execute(f'USE {self.db_name}')
            query = ('INSERT INTO blogs (title, subtitle, date, author, img_url, body, user_id)'
                     'VALUES (%s, %s, %s, %s, %s, %s, %s)')
            self.mycursor.execute(query, (title, subtitle, date, author, img_url, body, user_id))
            self.myconnection.commit()
            self.logger.info('Blog successfully inserted into database.')
            return True
        except mysql.Error as err:
            self.logger.error(f"Error when adding blog into database: {err}")
            return False

    def delete_blog(self, blog_id: str) -> bool:
        """
        Delete specific blog in the database.
        Args:
            blog_id (str): The id of the blog.
          Returns:
              Boolean
        """
        try:
            query = 'DELETE FROM blogs WHERE blog_id = %s'
            self.mycursor.execute(query, (blog_id,))
            self.myconnection.commit()
            self.logger.info(f'Blog {blog_id} successfully deleted')
            return True
        except mysql.Error as err:
            self.logger.error(f'Error when deleting: {err}')
            return False

    def get_all_blogs(self) -> list[dict] | None:
        """
        Retrieve the blogs from the database table.

        Returns:
            list: A list containing blogs details.
        """
        try:
            self.mycursor.execute('SELECT * FROM blogs ORDER BY blog_id DESC')
            result = self.mycursor.fetchall()

            if result:
                # Get column names from cursor.description
                columns = [descr[0] for descr in self.mycursor.description]
                # Create a list of dict using column names
                blogs = [dict(zip(columns, row)) for row in result]
                return blogs

            return None
        except mysql.Error as err:
            self.logger.error(f'Error retrieving the table data: {err}')
            return None

    def get_blog_by_id(self, blog_id: str) -> Blog | None:
        """
        Retrieve a specific blog by id from the database table.

        Args:
            blog_id (str): The ID of the blog to retrieve.

        Returns:
            dict | None: A dictionary containing the blog details if found, otherwise None.
        """
        try:
            query = 'SELECT * FROM blogs WHERE blog_id = %s'
            self.mycursor.execute(query, (blog_id,))
            result = self.mycursor.fetchone()

            if result:
                columns = [desc[0] for desc in self.mycursor.description]
                blog = dict(zip(columns, result))
                return Blog(**blog)

            return None

        except mysql.Error as err:
            self.logger.error(f'Error retrieving the table data: {err}')
            return None

    def update_blog(self, blog_id: str, title: str, subtitle: str, author: str, img_url, body) -> bool:
        """
        Update specific blog in the database.
        Args:
            blog_id (str): The id of the blog.
            title (str): The title of the blog.
            subtitle (str): The subtitle of the blog.
            author (str): The Author of the blog.
            img_url (str): The image URL that will be displayed on the card.
            body (str): The content of the blog.
          Returns:
              Boolean
        """
        try:
            query = '''
                UPDATE blogs
                SET title = %s, subtitle = %s, author = %s, img_url = %s, body = %s 
                WHERE blog_id = %s
                '''

            self.mycursor.execute(query, (title, subtitle, author, img_url, body, blog_id))
            self.myconnection.commit()
            self.logger.info('Blog successfully updated into database.')
            return True
        except mysql.Error as err:
            self.logger.info(f'Error when updating blog: {err}')
            return False
