from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,HiddenField
from wtforms.validators import EqualTo,DataRequired,Email,ValidationError,Length
from jobs.database import Admin

class Registration(FlaskForm):
    def validate_username(self,username_to_check):
        user=Admin.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists. Kindly log in to your account or use a different username')
    def validate_email_address(self,email_to_check):
        email=Admin.query.filter_by(email_address=email_to_check.data).first()
        if email:
            raise ValidationError('Email address exists. Log into your account or use a different email')

    username=StringField(label="User Name",validators=[Length(min=2,max=50),DataRequired()])
    email_address=StringField(label="Email",validators=[Email(),DataRequired()])
    setPassword=PasswordField(label="Password",validators=[DataRequired(),Length(min=6)])
    confirmPassword=PasswordField(label="Confirm password",validators=[DataRequired(),EqualTo("setPassword")])
    submit=SubmitField(label="Create Account")

   
class Login(FlaskForm):
    username=StringField(label="Username",validators=[DataRequired()])
    password=PasswordField(label="Password",validators=[DataRequired()])
    submit=SubmitField(label="Sign in")