# Blog Platform with User Authentication
This project is a web-based blogging platform built using Python, Jinja2, Mysql, Flask and BootStrap5.

The platform allows users to create, edit, and manage blog posts while providing a robust authentication system to ensure secure access. 

It incorporates various modern web development techniques and tools to provide a seamless and user-friendly experience.

Key Features
1. User Authentication and Authorization
Registration and Login: Users can register for an account and securely log in using their email and password.
Session Management: The app uses Flask-Login for managing user sessions, ensuring a smooth and secure user experience.
Protected Routes: Certain routes and features (like creating a new blog post) are only accessible to authenticated users.

2. Blog Management
Create, Read, Update, and Delete (CRUD) Operations: Authenticated users can create new blog posts, edit existing ones, and delete them if necessary.
Dynamic Content Rendering: Each blog post can have a unique title, subtitle, content, and an associated image that is dynamically rendered.
Association with Users: Blogs are associated with the users who create them, ensuring a clear content ownership model.
Responsive Design: A responsive navbar and overall layout, compatible with Bootstrap 5.3.3, provide an optimal viewing experience on various devices.

3. Database Management
MySQL Database: The project uses a MySQL database to store user information and blog posts.
Data Models with Python Dataclasses: Data models for users and blogs are defined using Python dataclasses, enabling clear and concise code.
Custom ORM-like Classes: UserManager and BlogsManager classes handle database interactions for users and blogs, respectively.

4. Security
Password Hashing: User passwords are securely hashed using Werkzeug’s security features, ensuring they are never stored in plaintext.
Data Validation: Input validation is implemented to ensure data integrity and prevent SQL injection attacks.

5. Customization and Extensibility
Easily Customizable: The project structure allows for easy customization and extension. New features, models, or routes can be added with minimal effort.
Template-Driven: Jinja2 templates are used for HTML rendering, enabling dynamic content updates.

Technologies Used
Flask: Python web framework used to build the core application.
Flask-Login: Extension used for managing user sessions and authentication.
MySQL: Relational database management system used to store user and blog data.
Jinja2: Templating engine for rendering HTML pages.
Bootstrap 5.3.3: Frontend framework for responsive design and UI components.
Python Dataclasses: Used to define data models for User and Blog.
Werkzeug Security: Provides password hashing for secure storage.

# Getting Started
Prerequisites
Python 3.7+
MySQL Server
Virtual Environment (venv)

# Installation
Clone the Repository:
git clone https://github.com/ozysouza/blogs-application.git
cd your-repo-name

Create and Activate a Virtual Environment:
pip3 install virtualenv
Active virtual environment: source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
Deactivate virtual environment: deactivate

# Install Dependencies:
pip install -r requirements.txt

If there is an error to install the mysql connector, run the following command

python -m pip install mysql-connector 

# Set Up the MySQL Database:

Make sure you have the MySql installed and set the credentials on the environment variables.

# Run the Application:

flask run
The application will be available at http://127.0.0.1:5000.

# Folder Structure
src/: Contains the main application source code.
src/database: Handles the mysql manager
src/helpers: Handles several functions as mail_manager, forms, blogs_manager, user_manger and models.

src/website/auth/: Handles user authentication routes.
src/website/views/: Handles user visualization routes.

templates/: Contains HTML templates for rendering views.
static/: Contains static files like CSS, JavaScript, and images.

Future Improvements
Currently refactoring code to add relationship with the databases.
User should be able to edit only blogs related to their account.
Add pagination for the blog listing.
Implement user profile pages.
Fix support for rich text editing in blog creation.
Implement an admin panel for advanced management.

Contributions are welcome! Please fork the repository and submit a pull request for any feature additions or bug fixes.
