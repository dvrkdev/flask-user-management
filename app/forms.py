from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, URLField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    # Name field
    name = StringField(
        'Name',
        validators=[
            DataRequired(message='Name is required.'),
            Length(min=3, max=64, message='Name must be between 3 and 64 characters.')
        ],
        description='Enter your full name'
    )

    # Email field
    email = EmailField(
        'Email Address',
        validators=[
            DataRequired(message='Email is required.'),
            Email(message='Please enter a valid email address.')
        ],
        description='Enter a valid email address'
    )

    # Password field
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required.'),
            Length(min=10, message='Password must be at least 10 characters long.')
        ],
        description='Use at least 10 characters.'
    )

    # Password confirmation
    password_confirm = PasswordField(
        'Password Confirmation',
        validators=[
            DataRequired(message='Please confirm your password.'),
            EqualTo('password', message='Passwords must match.')
        ],
        description='Re-enter your password'
    )

    submit = SubmitField('Create Account')

    # Custom validation for email uniqueness
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email address is already registered.')


class LoginForm(FlaskForm):
    # Email field
    email = EmailField(
        'Email Address',
        validators=[
            DataRequired(message='Email is required.'),
            Email(message='Please enter a valid email address.')
        ],
        description='Enter your registered email'
    )

    # Password field
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required.'),
            Length(min=10, message='Password must be at least 10 characters long.')
        ],
        description='Enter your account password'
    )

    submit = SubmitField('Login')


class UserChangeForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(message='Name is required.'),
            Length(min=3, max=64, message='Name must be between 3 and 64 characters.')
        ]
    )

    email = EmailField(
        'Email Address',
        validators=[
            DataRequired(message='Email is required.'),
            Email(message='Please enter a valid email address.')
        ]
    )

    profile_picture = URLField(
        'Profile Picture',
        validators=[
            Length(max=255, message='URL must be shorter than 255 characters.')
        ]
    )

    bio = TextAreaField(
        'Bio',
        validators=[
            Length(max=300, message='Bio must be at most 300 characters long.')
        ]
    )

    submit = SubmitField('Update Profile')

    # Custom validation for email uniqueness (excluding current user)
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.id != current_user.id:
            raise ValidationError('This email address is already registered.')


class PasswordChangeForm(FlaskForm):
    old_password = PasswordField(
        'Current Password',
        validators=[DataRequired(message='Current password is required.')]
    )

    new_password = PasswordField(
        'New Password',
        validators=[
            DataRequired(message='New password is required.'),
            Length(min=10, message='Password must be at least 10 characters long.')
        ]
    )

    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(message='Please confirm your new password.'),
            EqualTo('new_password', message='Passwords must match.')
        ]
    )

    submit = SubmitField('Change Password')
