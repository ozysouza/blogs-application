from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, TextAreaField, EmailField, ValidationError, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

import phonenumbers


class ContactForm(FlaskForm):
    """ Contact Form """
    username = StringField('Name',
                           validators=[DataRequired(message='Name is required.'),
                                       Length(min=3, max=25, message='User name must be between 3 and 25 characters')])
    email = EmailField('Email Address',
                       validators=[DataRequired(),
                                   Email(message='Email is not valid.'),
                                   Length(min=6, max=25, message='Email must be between 6 and 25 characters')])
    number = StringField('Phone Number', validators=[DataRequired(message='Phone Number is required.')])
    message = TextAreaField('Message', validators=[DataRequired(message='Message is required.')])
    submit_button = SubmitField('Send Email')

    # TODO: Add countries flags with the code
    @staticmethod
    def validate_number(self, number):
        if len(number.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(number.data, None)
            if not phonenumbers.is_valid_number(input_number):
                raise ValidationError('Invalid phone number.')
        except Exception:
            raise ValidationError('Invalid phone number format.')


class CreateBlogForm(FlaskForm):
    """ Blog Form """
    title = StringField('Blog Title', validators=[DataRequired(message='Blog Title is required.')])
    subtitle = StringField('Subtitle', validators=[DataRequired(message='Subtitle is required.')])
    img_url = StringField('Blog Image URL', validators=[DataRequired(message='Image URL is required.')])
    content = CKEditorField('Content', validators=[DataRequired(message='Text is required.')])
    submit_button = SubmitField('Submit Blog')


class RegisterForm(FlaskForm):
    """ Registration Form """
    firstname = StringField('First Name', validators=[DataRequired(message='First Name is required.'),
                                                      Length(min=4, max=15)])
    lastname = StringField('Last Name', validators=[DataRequired(message='Last Name is required.'),
                                                    Length(min=4, max=15)])
    email = EmailField('Email Address', validators=[DataRequired(),
                                                    Email(message='Email is not valid.'),
                                                    Length(min=6, max=25,
                                                           message='Email must be between 6 and 25 characters')])
    password = PasswordField('Password', validators=[DataRequired(message='Password is required.'),
                                                     Length(min=6, max=25)])
    confirm_password = PasswordField('Verify Password',
                                     validators=[DataRequired(message='Verify Password is required.'),
                                                 EqualTo('password',
                                                         message='Passwords must match.')])
    submit_button = SubmitField('Create Account')


class LoginForm(FlaskForm):
    """Sign in Form"""
    email = EmailField('Email', validators=[DataRequired(),
                                            Email(message='Email is not valid.'),
                                            Length(min=6, max=25, message='Email must be between 6 and 25 characters')])
    password = PasswordField('Password', validators=[DataRequired(message='Password is required.'),
                                                     Length(min=6, max=25)])
    submit_button = SubmitField('Sign In')
