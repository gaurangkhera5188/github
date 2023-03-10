from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Log in")

class RegForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Register")

class FileForm(FlaskForm):
    file_name = StringField('Filename', validators=[DataRequired()])
    file = FileField("Upload a file", validators=[DataRequired()])
    submit = SubmitField('Upload')

class RepoForm(FlaskForm):
    name = StringField('Repository name', validators=[DataRequired()])
    private = BooleanField('Keep these files private')
    submit = SubmitField('Create')
