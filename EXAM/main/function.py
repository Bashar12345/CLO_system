from flask import request, flash
from EXAM.model import course_model, enrol_students_model, student_courses_model, teacher_created_courses_model, temporary_model, user_student, user_teacher
from EXAM.configaration import user_obj
import random

def delete_temporary_model():
    collection = temporary_model.objects().all()
    collection.delete()
    print("deleted")


def enroll_students(eroll_ki, user_type):
    usered = user_obj.e
    enrolled = enrol_students_model.objects(enrol_key=eroll_ki).first()
    print(enrolled.course_code)
    if enrolled:
        course_model_include = course_model.objects(course_code=enrolled.course_code).first()
        if course_model_include:
            assigning_students = student_courses_model()
            assigning_students.user_type = user_type
            #print(assigning_students.user_type)
            assigning_students.student_registered_id = usered
            assigning_students.course_title = course_model_include.course_title
            assigning_students.course_code = course_model_include.course_code
            assigning_students.course_lessons = course_model_include.course_lessons
            assigning_students.course_duration = course_model_include.course_duration
            assigning_students.course_caption = course_model_include.course_caption
            assigning_students.save()
            flash(f'A new course Enrolled ', "success")


def teacher_view_courses(user):
    delete_temporary_model()
    teacher_registered_id = user_teacher.objects.get_or_404(email=user)
    if teacher_registered_id:
        courses = teacher_created_courses_model.objects(
            teacher_registered_id=user)
        for i in courses:
            temporary_model_ins = temporary_model()
            temporary_model_ins.user_type = i.user_type
            temporary_model_ins.teacher_registered_id = i.teacher_registered_id
            temporary_model_ins.course_title = i.course_title
            temporary_model_ins.course_code = i.course_code
            temporary_model_ins.course_co = i.course_co
            temporary_model_ins.course_lessons = i.course_lessons
            temporary_model_ins.course_duration = i.course_duration
            temporary_model_ins.course_caption = i.course_caption
            temporary_model_ins.save()


def student_view_courses(user):
    delete_temporary_model()
    student_registered_id = user_student.objects(email=user).first()
    if student_registered_id:
        courses = student_courses_model.objects(
            student_registered_id=user)
        for i in courses:
            temporary_model_ins = temporary_model()
            temporary_model_ins.user_type = i.user_type
            temporary_model_ins.student_registered_id = i.student_registered_id
            temporary_model_ins.course_title = i.course_title
            temporary_model_ins.course_code = i.course_code
            temporary_model_ins.course_co = i.course_co
            temporary_model_ins.course_lessons = i.course_lessons
            temporary_model_ins.course_duration = i.course_duration
            temporary_model_ins.course_caption = i.course_caption
            temporary_model_ins.save()


def created_course_form_db_insertion(get_form, user_type):
    form = get_form
    course_code = form.course_code.data
    course_title = form.course_title.data
    course_co = request.form.getlist('course_co')
    # course_lessons = form.course_lessons.data
    course_lessons = request.form.getlist('total_lesson[]')
    print(course_lessons)
    t = form.course_duration.data
    course_duration = t.strftime('%Y-%m-%d')
    course_caption = request.form.get('Note:captions')
    course_register = teacher_created_courses_model()
    course_register.user_type = user_type
    course_register.teacher_registered_id = user_obj.e
    course_register.course_code = course_code
    course_register.course_title = course_title
    course_register.course_lessons = course_lessons
    course_register.course_co = course_co
    course_register.course_duration = course_duration
    course_register.course_caption = course_caption
    course_register.save()
    course_register_course_model_ins = course_model()
    course_register_course_model_ins.course_code = course_code
    course_register_course_model_ins.course_title = course_title
    course_register_course_model_ins.course_lessons = course_lessons
    course_register_course_model_ins.course_co = course_co
    course_register_course_model_ins.course_duration = course_duration
    course_register_course_model_ins.course_caption = course_caption
    course_register_course_model_ins.save()
    if course_register.save():
        return course_title


def process_data_for_machine_learning(objects_of_requirement):
    # courses= course_model.objects()
    # required_data=required_for_generate.objects()
    # question_model=machine_learning_mcq_model.objects()
    # connection = MongoClient('localhost', 27017)
    # mongosql = connection.exam
    # required = mongosql.required_for_generate
    # mcq_data = mongosql.machine_learning_mcq_model
    # required_for_generate = required.find()
    # required=required_for_generate.objects()
    needed_course_code = []
    MCQ_questions = []
    purify_question_part = list()
    question_part = []
    temp = list()
    crse_code = objects_of_requirement.course_code
    for i in mcqQuestion.objects(course_code=crse_code):
        MCQ_questions.append(i.question)
    question_part = random.sample(
        MCQ_questions, objects_of_requirement.number_of_question)
    for i in question_part:
        if i not in purify_question_part:
            purify_question_part.append(i)
    if len(purify_question_part) != objects_of_requirement.number_of_question:
        extra_needed = objects_of_requirement.number_of_question - \
            len(purify_question_part)
        temp = random.sample(MCQ_questions, extra_needed)
    for i in temp:
        if i not in purify_question_part:
            purify_question_part.append(i)
    question_part = purify_question_part
    # print(MCQ_questions)
    # print(random.sample(MCQ_questions, 2))
    # random.shuffle(MCQ_questions)
    # print(MCQ_questions)
    # print(question_part)
    shuffled_question_list = []
    full_set_shuffled_question = []
    for ques in question_part:
        for j in mcqQuestion.objects(question=ques):
            if j not in shuffled_question_list:
                shuffled_question_list.append(j.question_dictionary)
    return shuffled_question_list



def evaluate_a_question(shuffled_list, objects_of_requirement):
    course_code = ''
    lessons = []
    complex = ''
    easy = 1
    medium = 2
    hard = 3
    easy_count = 0
    medium_count = 0
    hard_count = 0
    question_count = []
    complexity_level_of_highest_question_count = 0
    total_question = objects_of_requirement.number_of_question
    for ques in shuffled_list:
        # print(ques)
        question_paper = mcqQuestion.objects(question_dictionary=ques).first()
        complex = question_paper.complex_level
        course_code = question_paper.course_code
        lsn = question_paper.lesson
        if lsn not in lessons:
            lessons.append(lsn)
        # print(complex)
        # if complex == '1':
        # print(complex)
        question_count.append(complex)
    print(lessons)
    #print(" eta total_counted", question_count)
    for i in question_count:
        if i == '1':
            easy_count += 1
        if i == '2':
            medium_count += 1
        if i == '3':
            hard_count += 1
    print(easy_count, "eta", medium_count, "eta", hard_count)
    easy = easy*easy_count
    medium = medium*medium_count
    hard = hard*hard_count
    question_point = ((easy+medium+hard)+total_question)
    if easy > medium and easy > hard:
        question_point = question_point/1
    if medium > easy and medium > hard:
        question_point = question_point/2
    if hard > easy and hard > medium:
        question_point = question_point/3
    # vhul ase thik krte hobe
    print(question_point)
    return question_point, lessons, course_code
    # pass
