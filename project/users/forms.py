from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField
from wtforms.validators import EqualTo, DataRequired
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from project.models import User
from project import app, db


class LoginForm(FlaskForm):
    # ? Does this already check if the text is an Email?
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    username = StringField("UserName", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password_confirm", "Passwords do not match"),
        ],
    )
    password_confirm = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, email):
        with app.app_context():
            if User.query.filter_by(email=self.email.data).first():
                raise ValidationError("Your email is already registered!")

    def validate_username(self, username):
        with app.app_context():
            if User.query.filter_by(username=self.username.data).first():
                raise ValidationError("Your username is already registered!")


class UpdateForm(FlaskForm):
    username = StringField("UserName")
    email = EmailField("Email")
    picture = FileField("Profile Picture", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")

    # def validate_email(self, email):
    #     if self.email.data:
    #         with Session() as s:
    #             if s.query(User).filter_by(email=self.email.data).first():
    #                 print("Validation error", flush=True)
    #                 raise ValidationError("Your email is already registered!")

    # def validate_username(self, username):
    #     if self.username.data:
    #         with Session() as s:
    #             if s.query(User).filter_by(username=self.username.data).first():
    #                 print("Validation error", flush=True)
    #                 raise ValidationError("Your username is already registered!")

    def any_updates(self, user: User):
        if not self.email.data and not self.username.data and not self.picture.data:
            return False
        elif (
            self.email.data == user.email
            and self.username.data == user.username
            and not self.picture.data
        ):
            return False
        else:
            return True
