#from EXAM.users.routes import enrol
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField,BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from EXAM.model import enrol_students_model, user
from flask_wtf.file import FileAllowed, FileField, FileRequired

def validate_email(self, email):
        searchTheEmail = user.objects(email=email.data).first()
        if searchTheEmail:
            raise ValidationError('That email is already taken,Please choose another one')

class user_form(FlaskForm):
    user_name = StringField(
        'Name', validators=[DataRequired(), Length(min=2, max=50)])
    organization_id = StringField(
        'ID', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[
        DataRequired(), Length(min=2, max=50),validate_email])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_password', validators=[
        DataRequired(), EqualTo('password')])
    # phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=5, max=50)])
    profile_pic = FileField('Upload Profile Picture', validators=[FileRequired(), FileAllowed({'jpg', 'jpeg', 'png'})])
    user_category = RadioField(' What type of user are you? ', choices=[('admin', 'Admin'), ('teacher', 'Teacher'),('student', 'Student')])
    

def search_user(organization_id):
        searchTheOrganization_id = user.objects.filter(
            organization_id=organization_id.data).first()
        if searchTheOrganization_id:
            raise ValidationError('Not Found')
        return searchTheOrganization_id


class searchForm(FlaskForm):
    organization_id = StringField('Search for your students....')
    enroll_key=StringField('Enter the enroll key',validators=[DataRequired(),search_user])
    submit = SubmitField('search')

    
def validate_enrol_key(enrol_key):
        searchTheKey = enrol_students_model.objects.filter(
            enrol_key=enrol_key.data).first()
        if searchTheKey:
            raise ValidationError('Wrong key')


class enrolForm(FlaskForm):
    enrol_key = StringField(validators=[DataRequired(),validate_enrol_key])
    submit = SubmitField('Enter the Key')

    


class registration_form(FlaskForm):
    user_name = user_form.user_name
    organization_id = user_form.organization_id
    email = user_form.email
    password = user_form.password
    confirm_password = user_form.confirm_password
    # phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=5, max=50)])
    #profile_pic = FileField('Upload Profile Picture', validators=[FileRequired(), FileAllowed({'jpg', 'jpeg', 'png'})])
    profile_pic=user_form.profile_pic
    user_category = user_form.user_category
    submit = SubmitField('SignUp')

    #@staticmethod
    # def validate_email(self, email):
    #     searchTheEmail = user.objects(email=email.data).first()
    #     if searchTheEmail:
    #         raise ValidationError('That email is already taken,Please choose another one')


class forgetPasswordForm(FlaskForm):
    email = user_form.email
    submit = SubmitField('Request for Password reset')

class resetPasswordForm(FlaskForm):
    password = user_form.password
    confirm_password = user_form.confirm_password
    submit = SubmitField('Reset Password')


class LoginForm(FlaskForm):
    email = user_form.email
    password = user_form.password
    # credit = IntegerField('Credit Card Number', validators=[DataRequired(), Length(min=5, max=30)])
    # for using secret cookies for session login
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')
