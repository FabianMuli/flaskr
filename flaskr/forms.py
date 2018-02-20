from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, IntegerField, PasswordField, FileField
from wtforms.validators import Required, Email, EqualTo, Length

class LoginForm(Form):
    email =StringField(validators=[Email(), Required()])
    password = PasswordField(validators=[Required()])
    submit = SubmitField("Log In")
    remember_me = BooleanField('remember me', default=True)

class SignupForm(Form):
    first_name = StringField("First name:", validators=[Required()])
    second_name = StringField('Second name:', validators=[Required()])
    email = StringField('Email:', validators=[Email(), Required()])
    mobile_number = IntegerField('Mobile number:', validators=[Required()])
    password = PasswordField('Password:', validators=[Required(), Length(8, 20)])
    password2 = PasswordField('Confirm password', validators=[EqualTo('password'), Required()])
    submit = SubmitField('Submit')

class ChangePasswordForm(Form):
    email = StringField(validators=[Email(), Required()])
    submit = SubmitField('Reset my password')


class PostForm(Form):
    post = StringField("Whats on your mind:", validators=[Required()])
    submit = SubmitField("Post")

class UploadPhoto(Form):
    picture = FileField("Upload profile photo:",validators=[Required()])
    upload = SubmitField("Upload")
