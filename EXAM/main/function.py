from flask import request,flash
from EXAM.model import course_model, enrol_students_model, student_courses_model, teacher_created_courses_model, temporary_model, user_student, user_teacher
from EXAM.configaration import user_obj


def delete_temporary_model():
    collection = temporary_model.objects().all()
    collection.delete()
    print("deleted")





def enroll_students(eroll_ki,user_type):
    eroll_key=eroll_ki
    usered = user_obj.e
    enrolled=enrol_students_model.objects(enrol_key=eroll_key).first()
    if request.method == "POST":
        if enrolled:
            course_model_include=course_model.objects(course_code=enrolled.course_code).first()
            if course_model_include:
                assigning_students = student_courses_model()
                assigning_students.user_type =user_type
                assigning_students.student_registered_id = usered
                assigning_students.course_title = course_model_include.course_title
                assigning_students.course_code =course_model_include.course_code
                assigning_students.course_lessons =course_model_include.course_lessons
                assigning_students.course_duration =course_model_include.course_duration
                assigning_students.course_caption  = course_model_include.course_caption
                assigning_students.save()
                flash(f'A new course Enrolled ',"success")




def teacher_view_courses(user):
    delete_temporary_model()
    teacher_registered_id = user_teacher.objects.get_or_404(email=user)
    if teacher_registered_id:
        courses = teacher_created_courses_model.objects(
            teacher_registered_id=user)
        temporary_model_ins = temporary_model()
        for i in courses:
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
        temporary_model_ins = temporary_model()
        for i in courses:
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
    course_register_course_model_ins=course_model()
    course_register_course_model_ins.course_code=course_code
    course_register_course_model_ins.course_title=course_title
    course_register_course_model_ins.course_lessons=course_lessons
    course_register_course_model_ins.course_co=course_co
    course_register_course_model_ins.course_duration=course_duration
    course_register_course_model_ins.course_caption=course_caption
    course_register_course_model_ins.save()
    if course_register.save():
        return course_title
