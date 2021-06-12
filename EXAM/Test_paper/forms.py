from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TimeField, DateField, StringField, IntegerField, SubmitField, RadioField, \
    TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

#from EXAM.model import course_model
from EXAM.users.forms import user_form


# from flask_bootstrap import Bootstrap


class FileUploadFrom(FlaskForm):
    rename = StringField('Rename the file', validators=[DataRequired()])
    file = FileField('PDF', validators=[FileRequired(), FileAllowed({'pdf'})])
    submit = SubmitField('Upload')


class secret_Form(FlaskForm):
    exam_code = StringField('Exam Secret Code')
    submit = SubmitField('Confirm')
    # ekhane validation error er kazz korte baki ase


class writen_question_paper_Form(FlaskForm):
    exam_code = StringField('Exam Secret Code')
    # ethane email_code validation error er kazz korte baki ase
    exam_title = RadioField('Exam title :', choices=[(
        'mid-term', 'Mid-Term'), ('final', 'Final'), ('quiz', 'Quiz')])
    exam_course = StringField('Course', validators=[DataRequired()])
    exam_topic = StringField('Syllabus/Topic', validators=[DataRequired()])
    exam_start_time = TimeField('Start At:', validators=[DataRequired()])
    exam_end_time = TimeField('End At:', validators=[DataRequired()])
    exam_date = DateField('Date:', validators=[DataRequired()])
    f = FileUploadFrom
    rename_file = f.rename
    file = f.file
    submit = f.submit


class Written_question_answer_Form(FlaskForm):
    # , validators=[DataRequired(), Length(min=5, max=16)])
    student_id = StringField("First Confirm your ID:")
    answer = TextAreaField("Your Answer", validators=[])
    submit = SubmitField("Confirm Answer")  # , validators=[DataRequired()])





class McqQuestion_Paper_Form_part1(FlaskForm):
    exam_code = StringField('Exam Secret Code')
    # ekhane email_code validation error er kazz korte baki ase
    exam_title = RadioField('Exam title', choices=[(
        'mid-term', 'Mid-Term'), ('final', 'Final'), ('quiz', 'Quiz   ')])
    exam_course = StringField('Course', validators=[DataRequired()])
    exam_topic = StringField('Syllabus/Topic', validators=[DataRequired()])
    exam_start_time = TimeField('Start At', validators=[DataRequired()])
    exam_end_time = TimeField('End At', validators=[DataRequired()])
    exam_date = DateField('Date:', validators=[DataRequired()])
    caption = StringField('Caption for')


# under construction
class mcq_upload_form_part_1(FlaskForm):
    #course_title= SelectField("Questions for particular Course",coerce=str)
    lesson =SelectField("Pick a lesson",coerce=str,validate_choice=True)
    course_code =SelectField("Pick a Course Code",coerce=str,validate_choice=True)
    clo =SelectField("Pick a Course Learnig Outcome",coerce=str,validate_choice=True)
    # ekhane kaz korte hobe database theke lesson ante hobe
    submit = SubmitField('Next')



class Mcq_Question_generate_form(FlaskForm):
    title = ''
    # ekhane email_code validation error er kazz korte baki ase
    exam_title = RadioField('Exam title  ', choices=[(
        'mid-term', ' Mid-Term  '), ('final', '   Final  '),
        ('quiz-1', '  Quiz-1  '), ('quiz-2', '  Qui-2  '),
        ('quiz-3', '  Quiz-3 '), ('quiz-4', '  Quiz-4  '), ('quiz-5', '  Quiz-5  ')])
    exam_course = StringField('Course', validators=[DataRequired()])
    exam_course_code=StringField('Course_code',validators=[DataRequired()])
    # exam_topic = ('Syllabus/Topic/lesson', coerce=str, validate_choice=True)
    exam_topic = SelectField('Syllabus/Topic/lesson', coerce=str,validate_choice=True)
    exam_CLO = StringField('Course Outcome', validators=[
        DataRequired(), Length(min=1, max=10)])
    complex_level = StringField('Complex Level')
    exam_marks = StringField('Total marks :')
    exam_total_questions = IntegerField(
        'Number of Questions', validators=[DataRequired()])
    exam_start_time = TimeField('Start At:', validators=[DataRequired()])
    exam_end_time = TimeField('End At:', validators=[DataRequired()])
    exam_date = DateField('Date:', validators=[DataRequired()])
    caption = StringField('Special Note')
    exam_code = StringField('Exam Secret Code')
    submit = SubmitField(' Generate the question ')


class McqQuestion_Paper_Form_part2(FlaskForm):
    question = StringField('question', validators=[DataRequired()])
    option1 = StringField('option', validators=[DataRequired()])
    option2 = StringField('option', validators=[DataRequired()])
    option3 = StringField('option', validators=[DataRequired()])
    option4 = StringField('option', validators=[DataRequired()])
    submit = SubmitField('confirm')


class Mcq_answer_form(FlaskForm):
    fullname = StringField('Enter your Fullname', validators=[DataRequired()])
    organization_id = user_form.organization_id
    # answer = RadioField()
    submit = SubmitField()
