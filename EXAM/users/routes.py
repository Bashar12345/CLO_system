from flask.wrappers import Response
from EXAM import bcrypt
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import current_user, logout_user, login_required, login_user

from EXAM import bcrypt
from EXAM.configaration import User_type, user_obj
from EXAM.model import course_model, enrol_students_model, student_courses_model, temporary_model, user, user_student
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
    sending_mail_to_user_for_course_enroll_key,
)
import time

users = Blueprint("users", __name__)


@users.route("/registration", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.main_page"))
    form = registration_form()
    if request.method == "POST":
        check = ""
        try:
            check = register_method(form)
        except Exception as e:
            print("not connected    Hoy naiiiiiiiiiiii  ")
            print(str(e))
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
                else:
                    User_type.user_type = "teacher"
                    user_obj.e = usersd["email"]
                login_user(usersd, remember=form.remember.data)
                next_page = request.args.get("next")
                # return check
                flash(f"আপনার উপর শান্তি বর্ষিত হোক.... {usersd.user_name}", "success")
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


@users.route("/student_list/<course_code>", methods=["GET", "POST"])
# @login_required
def student_list(course_code):
    form = searchForm()
    selected_data = ""
    result_students = ""
    print(course_code)
    corse_code = course_code
    check = ""
    # students=''
    enroll = form.enroll_key.data
    if request.method == "POST":    
        print(enroll)
        organization_id = form.organization_id.data
        result_students = user_student.objects(organization_id=organization_id).first()
        if result_students:
            return render_template(
                "student/student_list.html",
                form=form,
                title="Students",
                user_type=User_type.user_type,
                result_students=result_students,
            )
        email_list = request.form.getlist('students_list_checkbox')
        
        sending_mail_to_user_for_course_enroll_key(email_list, enroll, corse_code)
    students = user_student.objects()
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
   
   #render_template("student/enrol.html", title=" Students", user_type=User_type.user_type)
"""


