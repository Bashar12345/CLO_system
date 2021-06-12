from flask.wrappers import Response
from EXAM import bcrypt
from flask import render_template, request, redirect, url_for, flash, Blueprint, session
from flask_login import current_user, logout_user, login_required, login_user

from EXAM import bcrypt
from EXAM.configaration import User_type, user_obj
from EXAM.model import admin_notice_model, course_model, enrol_students_model, student_courses_model, temp_student_collection, temporary_model, user, user_student
from EXAM.users.forms import (
    enrolForm,
    registration_form,
    LoginForm,
    forgetPasswordForm,
    resetPasswordForm,
    searchForm,
)
from EXAM.users.utils import (
    register_method,
    sending_email_to_user,
    sending_mail_to_user_for_course_enroll_key, delete_temporary_collection
)
import time
import datetime

users = Blueprint("users", __name__)


@users.route("/registration", methods=["GET", "POST"])
def register():
    form = registration_form()
    if current_user.is_authenticated:
        return redirect(url_for("main.main_page"))
    

    #if request.method == "POST":
    if form.validate_on_submit():
        check = register_method(form)
        if check == "done":
            return redirect(url_for("users.login"))
    return render_template("registration.html", title="Registration", form=form)


# klasd@gmail.com
# 4306985567


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.main_page"))
    form = LoginForm()
    # email = form.email.data
    # password = form.password.data
    # print(form.password.data)
    if request.method == "POST":
        if form.email.data:
            # if form.validate_on_submit():
            # print('email'+student_usersd.email, student_usersd['password'])
            usersd = user.objects.filter(
                email=form.email.data
            ).first()  # eta NOSQL er part
            if usersd and bcrypt.check_password_hash(
                usersd.password, form.password.data
            ):
                # print(usersd['email'], usersd['password'])
                if usersd.user_category == "student":
                    User_type.user_type = "student"
                    user_obj.e = usersd["email"]
                    session['email'] = usersd["email"]
                elif usersd.user_category == "admin":
                    session['email'] = ''
                    User_type.user_type = "admin"
                    user_obj.e = usersd["email"]
                    #session['email'] = usersd["email"]
                else:
                    session['email'] = ''
                    User_type.user_type = "teacher"
                    user_obj.e = usersd["email"]
                    session['course_date'] = ''
                login_user(usersd, remember=form.remember.data)
                next_page = request.args.get("next")
                # return check
                flash(
                    f"আপনার উপর শান্তি বর্ষিত হোক.... {usersd.user_name}", "success")
                if usersd.user_category == "admin":
                    return (
                        redirect(next_page)
                        if next_page
                        else redirect(url_for("main.admin"))
                    )
                else:
                    return (
                        redirect(next_page)
                        if next_page
                        else redirect(url_for("main.main_page"))
                    )
                # return check
            else:
                flash(f"Login Unsuccessful !!!", "danger")
                print("Data NAi")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    collection = temporary_model.objects().all()
    collection.delete()
    return redirect(url_for("main.main_page"))


@users.route("/account")
@login_required
def account():
    return redirect(url_for("main.main_page"))


@users.route("/reset_password", methods=(["GET", "POST"]))
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for("main.main_page"))
    form = forgetPasswordForm()
    # if request.method == 'POST':
    if form.validate_on_submit():
        User = user.objects(email=form.email.data).first()
        # print(jsonify(User))
        sending_email_to_user(User)
        flash("An Email has been sent with instruction to reset your password ", "info")
    return render_template("reset_password.html", title="change_password", form=form)


@users.route("/reset_password/<token>", methods=(["GET", "POST"]))
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.main_page"))
    User = user.verify_reset_token(token)
    if User is None:
        flash("that is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_password"))
    form = resetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        User.password = hashed_password
        User.save()
        flash("Your Password has been updated ! Now you can login with new password")
        return redirect(url_for("users.login"))
    return render_template(
        "reset_token.html", title="Verify_password_for_user", form=form
    )


@users.route("/create_notice", methods=(["GET", "POST"]))
@login_required
def create_notice():
    notice_title = request.form.get('title')
    notice_announcement = request.form.get('announcement')
    notice_time = datetime.datetime.now()
    if request.method == "POST":
        if notice_title:
            upload_notice = admin_notice_model()
            upload_notice.notice_title = notice_title
            upload_notice.notice_announcement = notice_announcement
            upload_notice.notice_time = notice_time
            upload_notice.save()

    return render_template(
        "admin_notice.html", title="Examiner_Page", user_type=User_type.user_type)


@users.route("/examiner")
@login_required
def examiner():
    # kaz ase -=---------------------------------------------------
    notices = admin_notice_model.objects().order_by("-notice_time")
    return render_template(
        "examiner.html", title="Examiner_Page", notices=notices, user_type=User_type.user_type)


@users.route("/student_list/<course_code>", methods=["GET", "POST"])
# @login_required
def student_list(course_code):
    form = searchForm()
    students = ''
    selected_data = ""
    result_students = ""
    corse_code, course_date = course_code.split("=")
    print(course_code, "  DAte", course_date)
    #corse_code = course_code
    check = ""
    # students=''
    enroll_key = form.enroll_key.data
    if request.method == "POST":
        delete_temporary_collection()
        print(enroll_key)
        organization_id = form.organization_id.data
        result_students = user_student.objects(
            organization_id=organization_id).first()
        if result_students:
            return render_template(
                "student/student_list.html",
                form=form,
                title="Students",
                user_type=User_type.user_type,
                result_students=result_students,
            )
        email_list = request.form.getlist('students_list_checkbox')
        sending_mail_to_user_for_course_enroll_key(
            email_list, enroll_key, corse_code)
    delete_temporary_collection()
    enrolled = enrol_students_model.objects(course_code=corse_code)
    if enrolled:
        delete_temporary_collection()
        for userStudents in user_student.objects():
            for students_enrolled in enrolled:
                if userStudents.email == students_enrolled.enrolled_students_id:
                    print(f"already ase {userStudents.email}")
                else:
                    student_temp_class = temp_student_collection()
                    student_temp_class.user_name = userStudents.user_name
                    student_temp_class.email = userStudents.email
                    student_temp_class.organization_id = userStudents.organization_id
                    student_temp_class.save()
    students = temp_student_collection.objects()
    return render_template(
        "student/student_list.html",
        form=form,
        title="Students",
        user_type=User_type.user_type,
        students=students,
        course_code=course_code,
    )


# '''if request.args:
#    c = request.args.get('c')
#         # selected_data = json.loads(request.args.get("email_list"))
#   flash(f'A mail with a enroll Has been send to the Students', 'success')
#       return redirect(url_for('main.main_page'))'''
"""@users.route("/enrol", methods=["GET", "POST"])
# @login_required
def enrol():
   eroll_key=request.form['enroll_key']
   enroll_students(eroll_key,User_type.user_type)
   return redirect(url_for("main.main_page"))
   
   # render_template("student/enrol.html", title=" Students", user_type=User_type.user_type)
"""
