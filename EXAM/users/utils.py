import datetime
import os
import secrets

from flask import render_template, url_for, flash

# import json
# import fileinput
# from PIL import Image
from flask_mail import Message

from EXAM import bcrypt, mail
from EXAM.model import enrol_students_model, records_of_course_exams, required_for_generate, set_exam_question_slot, temp_student_collection, user, user_student, user_teacher
import time

exam_code = ""
instance_path = "/home/b/Desktop/project/CLO_System/EXAM"


def go(op):
    op = op
    return render_template("mcqqu.html", op=op)


def mcq_bypass(get_form):
    form = get_form


def delete_temporary_collection():
    collection = temp_student_collection.objects().all()
    collection.delete()
    print("temp cleaned")


def remove_junk():
    # all = set_exam_question_slot._objects()
    t = datetime.datetime.now()
    date = t.strftime("%Y-%m-%d")
    print(date)
    for i in set_exam_question_slot.objects():
        print(i["exam_date"])
        if i["exam_date"] < date:
            expire_date = i["exam_date"]
            getting_exam_secret_key = required_for_generate.objects(
                exam_title=i.exam_title, exam_course=i.exam_course, course_code=i.exam_course_code, lesson=i.exam_topic, exam_start_time=i.exam_start_time, exam_end_time=i.exam_end_time)

            if getting_exam_secret_key:
                exams_records = records_of_course_exams()
                exams_records.exam_secret_code = getting_exam_secret_key.exam_secret_code
                exams_records.exam_title = i["exam_title"]
                exams_records.course_code = i["exam_course_code"]
                exams_records.entry_date = t
                exams_records.save()
            set_exam_question_slot.objects(exam_date=expire_date).delete()
            print("old")
    for i in set_exam_question_slot.objects():
        print(i["exam_date"])

   


def saveFormFile_in_Filesystem(form_file):
    random_hex = secrets.token_hex(8)
    print(form_file)
    f_name, f_ext = os.path.splitext(form_file.filename)
    file_original_name = f_name + f_ext
    # file_fn = random_hex + f_ext
    # file_fn2 = "DefaultPaper"+f_ext
    # instance_path = "/home/b/Desktop/project/CLO_System/EXAM"
    file_path = os.path.join(instance_path, "static/files", file_original_name)
    form_file.save(file_path)
    #   mongodb_data_class_ins.file.new_file()
    #   mongodb_data_class_ins.file.write(b"its streaming method")
    #   mongodb_data_class_ins.binary_file.close()
    #   mongodb_data_class_ins.save()
    # file.save()
    # fw =open("file.txt","wb")
    # fw= fh.read()
    # fh.close()
    return file_original_name, file_path, f_ext, random_hex
    # return file_fn
    # return file_fn2


def sending_email_to_user(model_er_user):
    token = model_er_user.get_reset_token()
    msg = Message(
        "Password Reset Verification",
        sender="bravebashar112@gmail.com",
        recipients=[model_er_user.email],
    )
    msg.body = f"""For password reset visit the following link: 
{url_for('users.reset_token', token=token, _external=True)}
    thank you
    """
    mail.send(msg)


def sending_mail_to_user_for_course_enroll_key(email_list, Enrol_key, course_code):
    # print(email_list)
    # print(type(email_list))
    delete_temporary_collection()
    if email_list:
        fw = open("file.txt", "w+")
        for index in email_list:
            students_enrol_ins = enrol_students_model()
            fw.write(index+"\n")

            students_enrol_ins.enrolled_students_id = index
            if students_enrol_ins.enrolled_students_id:
                students_enrol_ins.enrol_key = Enrol_key
                students_enrol_ins.course_code = course_code
                students_enrol_ins.save()
            time.sleep(1.0)
            print(students_enrol_ins.enrolled_students_id)
        fw.close()
    # ''' for i in email_list:
#  msg = Message('"Enroll key" for the course_entry',
#                sender='bravebashar112@gmail.com', recipients=i)
# msg.body = fFor Joining the course, Enter the key below :
# {Enroll_key}
# thank you
# This is an developing app for Testing purpose we send this email
# So, please calm down and be patient

# mail.send(msg)'''

# if current_user.is_authenticated:
# return redirect(url_for("main.base"))

def register_method(get_form):
   
    form = get_form
    name = form.user_name.data
    print(f"form er data ayse {name}")
    organization_id = form.organization_id.data
    user_category = form.user_category.data
    email = form.email.data
    # password = form.password.data # here is the password, by-chance if it needed
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
        "utf-8"
    )  # hashing
    # upload_profile_pic = form.profile_pic.data
    # if upload_profile_pic:
    #     print("photo ayse")
    upload_profile_pic, ext = binary_read(form.profile_pic.data)
    # doc_file_name, file_path, f_ext, random_file_name = saveFormFile_in_Filesystem(form.profile_pic.data)
    if user_category == "student":
        mongo_user = user_student()
        mongo_user.user_name = name
        mongo_user.organization_id = organization_id
        mongo_user.email = email
        # mongo_user.password = hashed_password
        mongo_user.user_category = user_category
        with open(upload_profile_pic, 'rb')as fd:
            #print(fd.read())
            mongo_user.profile_pic.put(
                fd, filename=name + ext, content_type="image/jpeg")
        #mongo_user.profile_pic = upload_profile_pic
        mongo_user.save()
        mongo_user_info = user()  # this is for 'not override email complication'
        mongo_user_info.user_name = name
        mongo_user_info.email = email
        mongo_user_info.password = hashed_password
        mongo_user_info.organization_id = organization_id
        mongo_user_info.user_category = user_category
        mongo_user_info.save()
    else:
        mongo_user = user_teacher()
        mongo_user.user_name = name
        mongo_user.organization_id = organization_id
        mongo_user.email = email
        # mongo_user.password = hashed_password
        mongo_user.user_category = user_category
        with open(upload_profile_pic, 'rb')as fd:
            #print(fd.read())
            mongo_user.profile_pic.put(
                fd, filename=name + ext, content_type="image/jpeg")
        #mongo_user.profile_pic = upload_profile_pic
        mongo_user.save()
        mongo_user_info = user()  # this is for 'not override email complication'
        mongo_user_info.user_name = name
        mongo_user_info.email = email
        mongo_user_info.password = hashed_password
        mongo_user_info.organization_id = organization_id
        mongo_user_info.user_category = user_category
        mongo_user_info.save()

    flash(f"Account has been created for {form.user_name.data} !", "success")
    print("Hoice")
    return "done"


def binary_read(form_pic_file):
    f_name, f_ext = os.path.splitext(form_pic_file.filename)

    pic_fn = f_name + f_ext

    instance_path = "/home/b/Desktop/project/EXAM"

    pic_path = os.path.join(instance_path, "static/temp", pic_fn)

    # binary mode e file khuila data mongodb te disi
    form_pic_file.save(pic_path)

    #img_or_file_binary = open(pic_path, "rb")

    img = pic_path

    print(img)

    return img, f_ext
