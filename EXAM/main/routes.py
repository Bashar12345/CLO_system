import os
import time
import datetime
import itertools
import json
#import requests
from io import BytesIO
import base64


from flask.wrappers import Response

from flask import render_template, request, redirect, url_for, flash, jsonify, make_response, Blueprint, app, session

from flask_login import login_required
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
# from newsapi import NewsApiClient

from EXAM.main.forms import create_course_form, PhotoForm

from EXAM.configaration import User_type, camera, user_obj

from EXAM.main.function import created_course_form_db_insertion, delete_exam_attened_exams, delete_old_question_requirements, enroll_students, evaluate_a_question, process_data_for_machine_learning, student_main_page, student_view_courses, teacher_view_courses, webcamera_live_stream

from EXAM.model import Only_file, course_model, enrol_students_model, machine_learning_mcq_model, marksheet, mcqQuestion, mcq_answer_paper, records_of_course_exams, set_exam_question_slot, student_attendence, student_courses_model, teacher_created_courses_model, teacher_posts_model, temporary_model, user_student, user_teacher

from EXAM.users.utils import delete_temporary_collection, remove_junk


main = Blueprint('main', __name__)
instance_path = "/home/b/Desktop/project/CLO_System/EXAM"
# newsapi = NewsApiClient(api_key="0bf80e3a6a5d4fefb6b80ceeaccb9560")
# newsapi = NewsApiClient("https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=0bf80e3a6a5d4fefb6b80ceeaccb9560")


@main.route("/live_stream")
# @login_required
def live_stream():
    return Response(webcamera_live_stream(camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.route('/upload', methods=['GET', 'POST'])
def upload():
    form = PhotoForm(CombinedMultiDict((request.files, request.form)))
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            instance_path, 'photos', filename
        ))
        return redirect(url_for('index'))

    return render_template('upload.html', form=form)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    # if User_type.user_type == 'admin':
    teachers = user_teacher.objects().all()
    students = user_student.objects().all()
    # context=zip(teachers,students)

    return render_template('admin.html', teachers=teachers, students=students, title='Admin', user_type=User_type.user_type)


main_page_count = 0


@main.route('/main_page', methods=['GET', 'POST'])
@login_required
def main_page():
    # ----------------------------------ekane teacher question evluate krbee
    # delete_exam_attened_exams()
    delete_old_question_requirements()
    teacher_email_id = user_obj.e
    student_id = session['email']

    if User_type.user_type == 'admin':
        return redirect(url_for('main.admin'))

    if User_type.user_type == 'student':
        todays_post, context = student_main_page(student_id)
        if request.method == "POST":
            eroll_key = request.form.get('enroll_key')
            delete_temporary_collection()
            print(eroll_key)
            enroll_students(eroll_key, User_type.user_type)
        exam_results = marksheet.objects(student_email=student_id)

        return render_template('main_page.html', latest_posts_from_teacher=todays_post, exam_results=exam_results, context=context, title='main_page', user_type=User_type.user_type)

    if User_type.user_type == 'teacher':  # ------------------------------------------------TEACHER

        shuffled_question_list, question_part, number_of_question, q_type = process_data_for_machine_learning()
        # print(shuffled_question_list)
        global main_page_count

        # for demo show purpose , question paper bar bar show kora hocche...... and not commented the ######process_data_for_machine_learning method

        # if main_page_count < 2:
        if request.method == "POST":
            difficulty = request.form.get('difficulty')
            if difficulty:
                print(difficulty)
            # ekhane kazzz baki ase-----------------------------------------------------
                evaluate_a_question(shuffled_question_list, question_part,
                                    number_of_question, difficulty, q_type)
            post_title = request.form.get('title')
            post_announcement = request.form.get('announcement')
            post_time = datetime.datetime.now()
            if post_title:
                upload_post = teacher_posts_model()
                upload_post.email = teacher_email_id
                upload_post.title = post_title
                upload_post.announcement = post_announcement
                upload_post.Date = post_time
                upload_post.save()

            # todays_post.append(teacher_posts_model(
            #     title=post_title, announcement=post_announcement, Date=post_time))

            # upload_post = user_teacher(
            #     email=teacher_email_id, post=todays_post)
            # # upload_post.objects(address__country="US").update_one(
            # #     set__posts__S=todays_post(title=post_title,announcement=post_announcement, Date=post_time)
            # # )
            # upload_post.save()

        main_page_count += 1
        return render_template('main_page.html', shuffled_question_list=shuffled_question_list,
                               title='main_page', user_type=User_type.user_type)

    return render_template('main_page.html', title='main_page', user_type=User_type.user_type)


@main.route('/take_a_tour')
def take_a_tour():
    return render_template('views/take_a_tour.html', title='main_page', user_type=User_type.user_type)


@main.route('/guideline')
def guideline():
    return render_template('guideline.html', title='guideline_Page', user_type=User_type.user_type)


@main.route('/guildLineForTeacher')
@login_required
def guildLineForTeacher():
    return render_template('teacher/guildLineForTeacher.html', title='Teacher_guildline', user_type=User_type.user_type)


@main.route('/create_course', methods=['GET', 'POST'])
@login_required
def create_course():
    lessons_len = ''
    form = create_course_form()
    user_type = User_type.user_type
    if request.method == "POST":
        confirm = created_course_form_db_insertion(form, user_type)
        if confirm:
            flash(
                f'{confirm}! Course successfully created, and sended to Admin, for authorization', 'success')
            return redirect(url_for('main.view_courses'))
    return render_template('teacher/create_course.html', title='Create_course', form=form, user_type=user_type)


# javascript kora
@main.route('/view_courses', methods=['GET', 'POST'])
@login_required
def view_courses():
    user_type = User_type.user_type
    usered = user_obj.e  # _P__alias
    # print(usered)
    if user_type == "teacher":
        teacher_view_courses(usered)
        return render_template('views/view_courses.html', title='View courses', user_type=user_type)
    else:
        student_view_courses(usered)
        return render_template('views/view_courses.html', title='View courses', user_type=user_type)


@main.route('/view_course_load_data')
@login_required
def view_course_load_data():
    time.sleep(0.2)

    response_to_browser = ""
    per_scrolling = int(5)
    counter = 0
    datalist = []
    print("Total :", len(course_model.objects()), " Courses registered")

    if request.args:
        c = request.args.get('c')
        count, user_typ = c.split("=")
        print(type(count), " ", count, "  ", user_typ)
        counter = int(count)
        user_type = user_typ
        data_teacher = temporary_model.objects()
        if user_type == 'teacher' and data_teacher is not None:
            if counter == 0:
                print(" first 5 ")
                response_to_browser = make_response(
                    jsonify(temporary_model.objects[:per_scrolling]))
                print(response_to_browser)
            elif counter == len(temporary_model.objects()):
                response_to_browser = make_response(jsonify({}), 200)
                print(response_to_browser)
                print("no more Courses")
            else:
                response_to_browser = make_response(
                    jsonify(temporary_model.objects[counter:counter + per_scrolling]))
                print(f"{counter} to {counter + per_scrolling}")
                print(response_to_browser)
        else:
            data_student = temporary_model.objects()
            if data_student is not None:
                if counter == 0:
                    print(" first 5 ")
                    response_to_browser = make_response(
                        jsonify(temporary_model.objects[:per_scrolling]))
                    print(response_to_browser)
                elif counter == len(temporary_model.objects()):
                    response_to_browser = make_response(jsonify({}), 200)
                    print(response_to_browser)
                    print("no more Courses")
                else:
                    response_to_browser = make_response(
                        jsonify(temporary_model.objects[counter:counter + per_scrolling]))
                    print(f"{counter} to {counter + per_scrolling}")
                    print(response_to_browser)

    return response_to_browser


@main.route('/question_view/<course_code>', methods=['GET', 'POST'])
@login_required
def question_view(course_code):
    course_data = ''
    print(course_code)
    if User_type.user_type == 'student':

        course_code, course_date = course_code.split("=")
        print(course_code, "  DAte", course_date)

        course_data = course_model.objects(
            course_code=course_code, course_duration=course_date).first()
    # questions = []
    # if request.args:
    # course_code = request.args.get("course_code")
    # questions_objects = machine_learning_mcq_model.objects(course_code=course_code)
    # print(questions_objects)
    # for i in mcqQuestion.objects(
    #         course_code=course_code):
    #     questions = i.question
    # print(questions)
    return render_template('question_view/view_questions.html', title='question_view', user_type=User_type.user_type, course_code=course_code, course_data=course_data, mcqQuestion=mcqQuestion)


@ main.route('/dashboard')
@ login_required
def student_dashboard():
    remove_junk()
    datalist = []
    course_code_list = []
    student_email = user_obj.e
    for i in enrol_students_model.objects(enrolled_students_id=student_email):
        if i.course_code not in course_code_list:
            course_code_list.append(i.course_code)

    return render_template('dashboard.html', course_code_list=course_code_list, set_exam_question_slot=set_exam_question_slot, title='Recent Exams', user_type=User_type.user_type)


@main.route('/courseRegisteredStudents', methods=['GET', 'POST'])
@login_required
def course_assigned_students():
    user_emails_total = list()
    students_name = list()
    usered = user_obj.e
    students = student_courses_model.objects()
    for student in students:
        print(student.student_registered_id)
        for enrolled in enrol_students_model.objects(enrolled_students_id=student.student_registered_id):
            # print(enrolled.course_code)
            for teacher in teacher_created_courses_model.objects(teacher_registered_id=usered):
                # print(teacher.course_code)
                if teacher.course_code == enrolled.course_code and \
                        student.course_code == enrolled.course_code:
                    # print(student.student_registered_id)
                    if student.student_registered_id not in user_emails_total:
                        user_emails_total.append(student.student_registered_id)

                    # print("matched")
    # print(user_emails_total)
    for user in user_emails_total:
        for user_s in user_student.objects(email=user):
            # print(user_s.user_name)
            if user_s.user_name not in students_name:
                students_name.append(user_s.user_name)
    print(students_name)
    return render_template('views/view_your_students.html', title="My Students", user_type=User_type.user_type, user_emails_total=user_emails_total, students_name=students_name, iter=itertools)


@main.route('/course_exams/<course_code>', methods=['GET', 'POST'])
@login_required
def course_exams(course_code):
    course_code, course_date = course_code.split("=")
    print(course_code, "  DAte", course_date)
    passed_course_exams = records_of_course_exams.objects(
        course_code=course_code).order_by("entry_date")

    return render_template('question_view/exams_view.html', title='Course Exams', course_code=course_code, passed_course_exams=passed_course_exams, user_type=User_type.user_type)


@main.route('/course_exams_students/<link_info>', methods=['GET', 'POST'])
@login_required
def course_exams_students(link_info):

    # course_code, exam_title = link_info.split("=")
    # print(" Exam tittle -------------------------- ",exam_title)
    print(link_info)
    attended_students = student_attendence.objects(exam_secret_code=link_info)
    # for i in attended_students:
    # objects_of_student = user_student.objects(email=i.student_email).first()
    # print(objects_of_student.profile_pic.read())
    # pic = BytesIO(objects_of_student.profile_pic.read())
    # print(type(pic))
    # print(pic)
    # try:
    #  with open(objects_of_student.profile_pic.filename, "wb+") as f:
    #   f.write(pic.getbuffer())
    #   #f.save()
    #   f.close()
    # except Exception as e:
    #      print(e)
    return render_template('question_view/students_of_exam_slots.html', title='Exams Attened_Students', link_info=link_info, attended_students=attended_students, user_student=user_student, BytesIO=BytesIO, base64=base64, user_type=User_type.user_type)


@main.route('/course_exams_students_answer_sheet/<link_info>', methods=['GET', 'POST'])
@login_required
def course_exams_students_answer_sheet(link_info):
    print(link_info)
    code, student_id = link_info.split("=")
    answer_sheets = mcq_answer_paper.objects(
        exam_secret_code=code, email=student_id).first()

    # for video_file_name in answer_sheets.surveilence_video_list:

    #     video_file_surveilence = Only_file.objects(
    #         v_id=video_file_name).first()
    #     vid = BytesIO(video_file_surveilence.binary_file.read())
    #     print(vid)
    #     v_file_name = "/home/b/Desktop/CLO_system/EXAM/static/files/"+video_file_name
    #     try:
    #         with open(v_file_name, "wb+") as f:
    #             f.write(vid.getbuffer())
    #             # f.save()
    #             f.close()
    #     except Exception as e:
    #         print(e)

    return render_template('question_view/students_answer_sheet.html', answer_sheets=answer_sheets, link_info=link_info, title='Exams-Answer sheet', user_type=User_type.user_type, iter=itertools)


@ main.route('/loading_students')
# @login_required
def loading_students():
    pass


# @main.route('/exam_slot_load')
# @login_required
# def exam_slot_load():
#     time.sleep(0.2)

#     response_to_browser = ""
#     per_scrolling = int(5)
#     counter = 0
#     datalist = []
#     student_email = user_obj.e
#     enrol_students_model.objects(enrolled_students_id=student_email)
#     # print(len(set_exam_question_slot.objects()))

#     if request.args:
#         counter = int(request.args.get('c'))

#         if counter == 0:
#             print(" first 5 ")
#             response_to_browser = make_response(
#                 jsonify(set_exam_question_slot.objects[:per_scrolling].filter_by())) #.order_by('exam_date')))
#             print(response_to_browser)

#         elif counter == len(set_exam_question_slot.objects()):
#             response_to_browser = make_response(jsonify({}), 200)
#             print(response_to_browser)
#             print("no more Schedule")
#         else:
#             response_to_browser = make_response(
#                 jsonify(set_exam_question_slot.objects[counter:counter + per_scrolling]))
#             print(f"{counter} to {counter + per_scrolling}")
#             print(response_to_browser)

#     return response_to_browser
