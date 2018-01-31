from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, IntegerField, PasswordField
from wtforms.validators import Required, Email, EqualTo

class LoginForm(Form):
    email =StringField(validators=[Email(), Required()])
    password = PasswordField(validators=[Required()])
    submit = SubmitField("Submit")
    remember_me = BooleanField('remember_me', default=True)

class SignupForm(Form):
    first_name = StringField("First name:", validators=[Required()])
    second_name = StringField('Second name:', validators=[Required()])
    email = StringField('Email:', validators=[Email(), Required()])
    mobile_number = IntegerField('Mobile number:', validators=[Required()])
    password = PasswordField('Password:', validators=[Required()])
    password2 = PasswordField('Confirm password', validators=[EqualTo('password'), Required()])
    submit = SubmitField('Submit')

class PostForm(Form):
    post = StringField("Whats on your mind:", validators=[Required()])
    submit = SubmitField("Post")