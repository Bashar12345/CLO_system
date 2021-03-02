from EXAM.configaration import user_obj
from flask import request
from EXAM.model import student_courses_model, teacher_created_courses_model, temporary_model, user_student, user_teacher


def delete_temporary_model():
    collection = temporary_model.objects().all()
    collection.delete()
    print("deleted")


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
    course_co = form.course_co.data
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
    if course_register.save():
        return course_title
