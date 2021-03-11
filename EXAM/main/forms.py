from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TimeField, DateField, StringField, IntegerField, SubmitField, RadioField, \
    TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

from EXAM.model import course_model


class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])


class create_course_form(FlaskForm):
    course_code = StringField('Course Code')
    course_title = StringField('Enter Course Title (Dont give "#,$,@,&" these caracters)')
    course_co = StringField('Course Outcome (Only number please) ')
    course_lessons = StringField('Total Lessons of this course')
    course_duration = DateField(
        'Date: (Please, Enter When Course will be finished)', validators=[DataRequired()])
    course_caption = StringField('Course Caption/Details')
    submit = SubmitField(' Create Course ')

    @staticmethod
    def validation_course(course_code):
        searchTheCourse = course_model.objects.filter(
            course_code=course_code.data).first()
        if searchTheCourse:
            raise ValidationError(
                'That course_code is already taken,Please choose another one')
