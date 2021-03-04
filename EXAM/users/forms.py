#from EXAM.users.routes import enrol
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, \
    BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from EXAM.model import enrol_students_model, user


class user_form(FlaskForm):
    user_name = StringField(
        'Name', validators=[DataRequired(), Length(min=2, max=50)])
    organization_id = StringField(
        'ID', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[
        DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_password', validators=[
        DataRequired(), EqualTo('password')])
    # phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=5, max=50)])
    # profile_pic = FileField('Upload Profile Picture', validators=[FileRequired(), FileAllowed({'jpg', 'jpeg', 'png'})])
    user_category = RadioField(' What type of user are you? ', choices=[('admin', 'Admin'), ('teacher', 'Teacher'),
                                                                        ('student', 'Student')])


class searchForm(FlaskForm):
    organization_id = StringField('Search for your students....')
    enroll_key=StringField('Enter the enroll key',validators=[DataRequired()])
    submit = SubmitField('search')

    @staticmethod
    def search_user(organization_id):
        searchTheOrganization_id = user.objects.filter(
            organization_id=organization_id.data).first()
        if searchTheOrganization_id:
            raise ValidationError('Not Found')
        return searchTheOrganization_id


class enrolForm(FlaskForm):
    enrol_key = StringField(validators=[DataRequired()])
    submit = SubmitField('Enter the Key')

    @staticmethod
    def validate_enrol_key(enrol_key):
        searchTheKey = enrol_students_model.objects.filter(
            enrol_key=enrol_key.data).first()
        if searchTheKey:
            raise ValidationError('Wrong key')


class registration_form(FlaskForm):
    user_name = user_form.user_name
    organization_id = user_form.organization_id
    email = user_form.email
    password = user_form.password
    confirm_password = user_form.confirm_password
    # profile_pic = user_form.profile_pic
    user_category = user_form.user_category
    # credit = StringField('Credit', validators=[DataRequired()])
    submit = SubmitField('SignUp')

    @staticmethod
    def validation_email(email):
        searchTheEmail = user.objects.filter(email=email.data).first()
        if searchTheEmail:
            raise ValidationError(
                'That email is already taken,Please choose another one')


class forgetPasswordForm(FlaskForm):
    email = user_form.email
    submit = SubmitField('Request for Password reset')

    @staticmethod
    def validation_email(email):
        searchTheEmail = user.objects.filter(email=email.data).first()
        if searchTheEmail:
            print('ase email')
        else:
            raise ValidationError(
                'There is no account with that email,please Register ')


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
