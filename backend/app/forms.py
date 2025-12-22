from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField("البريد الإلكتروني", validators=[DataRequired(), Email(), Length(max=190)])
    password = PasswordField("كلمة المرور", validators=[DataRequired(), Length(min=8, max=128)])
    remember = BooleanField("تذكرني")
