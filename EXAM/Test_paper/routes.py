import datetime

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file,
    Blueprint,
    jsonify,
    make_response,
)
from flask.wrappers import Response
from flask_login import current_user, login_required

from EXAM.Test_paper.forms import (
    Mcq_Question_generate_form,
    mcq_upload_form_part_1,
    writen_question_paper_Form,
    McqQuestion_Paper_Form_part1,
    McqQuestion_Paper_Form_part2,
    secret_Form,
    Written_question_answer_Form,
    Mcq_answer_form,
)
from EXAM.Test_paper.function import (
    generate_question,
    mcq_question_Upload_part1,
    mcq_question_Upload_part2,
    mcq_question_answer_submit,
    mcq_uploading_processsing,
    written_question_Upload,
    written_question_answer_submit,
)
from EXAM.configaration import secret_exam_key, object_of_something, User_type,sum_of_something
from EXAM.model import (
    machine_learning_mcq_model, course_model,
    exam_mcq_question_paper,
    exam_written_question_paper, required_for_generate,
)

"""@Test_paper.route('/')
def hello_world():
    return 'Hello World!'
"""

Test_paper = Blueprint("Test_paper", __name__)



@Test_paper.route("/examiner")
@login_required
def examiner():
    return render_template(
        "examiner.html", title="Examiner_Page", user_type=User_type.user_type
    )


# paginate kora
"""@Test_paper.route('/view_courses', methods=['GET', 'POST'])
# @login_required
def view_courses():
    page = request.args.get('page',1,type=int)
    # paginate_page
    paginated_course = course_model.objects.order_by('course_code').paginate(
            page=page, per_page=3)
    return render_template('teacher/view_courses.html', paginated_course=paginated_course, title='View courses', user_type=User_type.user_type)"""


@Test_paper.route("/wrqu", methods=["GET", "POST"])
@login_required
def wrqu():
    form = writen_question_paper_Form()
    written_question_Upload(form)
    return render_template(
        "wrqu.html", title="WrittenQu_Page", form=form, user_type=User_type.user_type
    )


@Test_paper.route("/wran", methods=["GET", "POST"])
@login_required
def wran():
    form = Written_question_answer_Form()
    written_question_answer_submit(form)
    written_question = object_of_something.a_object
    if written_question:
        time = datetime.datetime.now()
        print(time)

    return render_template(
        "wran.html",
        written_question=written_question,
        title="Writen_answer_Page",
        form=form,
        user_type=User_type.user_type,
    )


@Test_paper.route("/mcqqu_sub", methods=["GET", "POST"])
@login_required
def mcqqu_sub():
    # also you can add question type like School question or,
    form = McqQuestion_Paper_Form_part1()
    # Job interview or admission question.
    number_of_questions = request.form.get("numbers_of_questioned")
    # print(number_of_questions)
    global sum_of_something  # Which is in under construction
    sum_of_something = number_of_questions
    # print(op, type(op))
    if number_of_questions and request.method == "POST":
        exam_code = mcq_question_Upload_part1(form, sum_of_something)
        try:
            if exam_code:
                secret_exam_key.exam_code = exam_code
                return redirect(url_for("Test_paper.mcqqu"))
            else:
                return "" f"<h1><method Problem></h1>"
        except Exception as e:
            print(str(e))

            # return redirect(url_for('Test_paper.examiner'))
            # return render_template('mcqqu.html', title='MCQ_question_Page', form=fom, op=op)
        # print('database e jay niki')
    return render_template(
        "mcq/mcqqu_sub.html",
        title="MCQ_question_Page",
        form=form,
        user_type=User_type.user_type,
    )


@Test_paper.route("/mcqqu", methods=["GET", "POST"])
@login_required
def mcqqu():
    form = McqQuestion_Paper_Form_part2()
    # print(sum_of_something)
    exam_code = secret_exam_key.exam_code
    switch = mcq_question_Upload_part2(sum_of_something, exam_code)
    if switch == "ok":
        return redirect(url_for("Test_paper.examiner"))
    else:
        return render_template(
            "mcq/mcqqu.html",
            title="MCQ_question_Page",
            form=form,
            op=sum_of_something,
            user_type=User_type.user_type,
        )



@Test_paper.route("/mcqan", methods=["GET", "POST"])
@login_required
def mcqan():
    form = Mcq_answer_form()
    # mcq_question_answer_submit(form)
    mcq_questions = object_of_something.a_object
    exam_start_time = mcq_questions.exam_start_time
    exam_end_time = mcq_questions.exam_end_time
    exam_date = mcq_questions.exam_date
    # print(exam_start_time, exam_end_time, exam_date)
    year, month, day = exam_date.split("-")
    hour, minute = exam_start_time.split(":")
    end_hour, end_minute = exam_end_time.split(":")
    # print(time)      # print(hour, " minute ase ", minute)
    current_time = datetime.datetime.now()
    # current_time2 = current_time
    starting_time_of_exam = datetime.datetime(
        int(year), int(month), int(day), int(hour), int(minute)
    )
    ending_time_of_exam = datetime.datetime(
        int(year), int(month), int(day), int(end_hour), int(end_minute)
    )
    print(f"ending time {ending_time_of_exam}")
    print(f"starting time {starting_time_of_exam}")
    # print(mcq_question['mcq_question'])

    # if starting_time_of_exam <= current_time <= ending_time_of_exam:
    if starting_time_of_exam <= current_time <= ending_time_of_exam:
        print(current_time)
        if request.method == "POST":
            check = mcq_question_answer_submit(form)
            if check == "done":
                return redirect(url_for("users.student"))
        return render_template(
            "mcq/mcqan.html",
            mcq_questions=mcq_questions,
            title="MCQ_answer_Page",
            form=form,
            user_type=User_type.user_type,
        )
    return render_template(
        "count_Down.html",
        starting_time_of_exam=starting_time_of_exam,
        title="countdown",
    )


@Test_paper.route("/secret_code", methods=["GET", "POST"])
@login_required
def secret_code():
    content_type = ""
    form = secret_Form()
    # confirmation_of_question()
    if request.method == "POST":
        exam_code = form.exam_code.data
        # print(exam_code)
        # mongodb_written_question = exam_written_question_paper()
        # mongodb_mcq_question = exam_MCQ_question_paper()
        # written_question = exam_written_question_paper.objects(exam_code=exam_code)
        mcq_question = exam_mcq_question_paper.objects.filter(
            exam_code=exam_code
        ).first()
        written_question = exam_written_question_paper.objects.filter(
            exam_code=exam_code
        ).first()
        if written_question:
            for i in written_question:
                # print(written.binary_file)
                print(written_question.binary_file.tell())
                content_type = written_question.binary_file.content_type
                print(content_type)
                # fw = open("file.pdf", 'wb')  # eta thik korte hobe
                # fw.close()
                # print(i['exam_topic'])
                #  print(i['binary_file'])
                #  print(i['file_extension'])
                # file = i['binary_file']
                print(file)
                # binary_read(i['binary_file'])'''
            object_of_something.a_object = written_question
            return redirect(url_for("Test_paper.wran"))
            # return render_template('wran.html', written_question=written_question, content_type=content_type,
            # title='Written_answer_page')
        elif mcq_question:
            object_of_something.a_object = mcq_question
            # print(mcq_question)
            return redirect(url_for("Test_paper.mcqan"))
        else:
            flash(f"Re-Enter Exam code!!", "danger")
            return redirect(url_for("users.student"))
    else:
        return render_template(
            "secret_code.html",
            form=form,
            title="Identify",
            user_type=User_type.user_type,
        )
        # return redirect(url_for('Test_paper.secret_code'))


@Test_paper.route("/file/<filename>")
def file(filename):
    written = exam_written_question_paper.objects.filter(rename_file=filename).first()
    return send_file(
        written.binary_file,
        as_attachment=True,
        mimetype="Test_paperlication/pdf",
        attachment_filename=filename,
    )


course = ""
topic = ""
Complexity_label = ""
Course_outcome = ""
number_of_question = ""


@Test_paper.route("/mcqUpload", methods=["GET", "POST"])
# @login_required
def mcq_upload():
    form = mcq_upload_form_part_1()
    # seach course code and fetch the lessons
    # under construction
    course_title_list = course_model.objects.only("course_title")
    course_title = []
    for title in course_title_list:
        # print(title.course_title)
        if title.course_title not in course_title:
            course_title.append(title.course_title)
    if request.method == "POST":
        mcq_uploading_processsing(form)
    return render_template(
        "mcq/mcqupload.html",
        title="mcqUpload",
        form=form,
        user_type=User_type.user_type,
        course_title=course_title,
    )


@Test_paper.route("/mcqUpload_course_code_selection_load")
# @login_required
def mcqUpload_course_code_selection_load():
    response_to_browser = ""
    # print("Total :", len(course_model.objects()), " Courses registered")
    # course = course_model.objects(course_title=fetched).all()
    if request.args:
        # sentence = '  Thesis & project    '
        # str1= sentence.replace(" ", "")
        # print(str1)
        crse = request.args.get("c")
        corse = crse.replace(";", " ")
        print(corse)
        response_to_browser = make_response(
            jsonify(course_model.objects(course_title=corse).all())
        )
        print(response_to_browser)
        flash("Select a particular Course code ", "success")
    return response_to_browser


@Test_paper.route("/mcqUpload_lesson_selection_load")
# @login_required
def mcqUpload_lesson_selection_load():
    response_to_browser = ""
    if request.args:
        code = request.args.get("c")
        # print(code)
        lesn = course_model.objects(course_code=code).first()
        # print(type(lesn.course_lessons))
        lessons_list = []
        for lesson in lesn.course_lessons:
            # print(lesson)
            lessons_list.append(lesson)
        response_to_browser = make_response(jsonify(lessons_list))
        print(response_to_browser)
    return response_to_browser


"""@Test_paper.route('/countdown', methods=['GET', 'POST'])
def countdown():
    return render_template('count_Down.html', title='countdown')"""

"""@Test_paper.route('/mcqqu', methods=['GET', 'POST'])
def mcqqu():
    form = McqQuestion_Paper_Form()
    mcq_question_form(form)
    return render_template('mcqqu.html', posts=posts, title='MCQ_question_Page', form=form)"""
""" mcq = mcq_questions.mcq_question.question_dictionary
    for i in mcq:
        print(i + "\n")
        for j in mcq[i]:
            print(j)"""


@Test_paper.route("/generateMCQ", methods=["GET", "POST"])
# @login_required
def generateMCQ():
    form = Mcq_Question_generate_form()
    course_code = course_model.objects.only("course_code")
    if request.method == "POST":
        generate_question(form)
    return render_template(
        "mcq/generateMCQ.html",
        title="MCQgenerate",
        form=form,
        user_type=User_type.user_type,
        course_code=course_code,
    )


@Test_paper.route("/generateMCQ_lesson_load")
# @login_required
def generateMCQ_lesson_load():
    response_to_browser = ""
    if request.args:
        code = request.args.get("c")
        # print(code)
        lesn = course_model.objects(course_code=code).first()
        # print(type(lesn.course_lessons))
        lessons_list = []
        for lesson in lesn.course_lessons:
            # print(lesson)
            lessons_list.append(lesson)
        response_to_browser = make_response(jsonify(lessons_list))
        print(response_to_browser)
    return response_to_browser


@Test_paper.route("/mcqAnswerPaper", methods=["GET", "POST"])
# @login_required
def mcq_answer_paper():
    form = Mcq_answer_form()
    # mcq_question_answer_submit(form)
    mcq_questions = exam_mcq_question_paper.objects(exam_code="quiz-feb").first()
    exam_start_time = "14:17"
    exam_end_time = "20:17"
    exam_date = "2021-02-21"
    # print(exam_start_time, exam_end_time, exam_date)
    year, month, day = exam_date.split("-")
    hour, minute = exam_start_time.split(":")
    end_hour, end_minute = exam_end_time.split(":")
    # print(time)      # print(hour, " minute ase ", minute)
    current_time = datetime.datetime.now()
    # current_time2 = current_time
    starting_time_of_exam = datetime.datetime(
        int(year), int(month), int(day), int(hour), int(minute)
    )
    ending_time_of_exam = datetime.datetime(
        int(year), int(month), int(day), int(end_hour), int(end_minute)
    )
    print(f"ending time {ending_time_of_exam}")
    print(f"starting time {starting_time_of_exam}")
    # print(mcq_question['mcq_question'])

    # if starting_time_of_exam <= current_time <= ending_time_of_exam:
    if starting_time_of_exam <= current_time <= ending_time_of_exam:
        print(current_time)
        if request.method == "POST":
            check = mcq_question_answer_submit(form)
            if check == "done":
                return redirect(url_for("users.student"))
        return render_template("mcqan.html",
            exam_date=exam_date,
            exam_end_time=exam_end_time,
            mcq_questions=mcq_questions,
            title="MCQ_answer_Page",
            form=form,
            user_type=User_type.user_type,
        )
    return render_template(
        "count_Down.html",
        starting_time_of_exam=starting_time_of_exam,
        title="countdown",
    )

@Test_paper.route("/sample", methods=["GET", "POST"])
# @login_required
def sample():
    return render_template(
        "sample.html",
    )
























# form.course_title.choices=[(course_name,course_name)for course_name in course_title]
    # form.course_code.choices=[(codes.course_code,codes.course_code) for codes in course_model.objects(course_title='Thesis & project').all()]
    # form.lesson.choices=[(lessons.course_lessons,lessons.course_lessons) for lessons in course_model.objects(course_code='swe451').all()]

    # return '<h1> Course title : {}, Lesson : {}</h1>'.format(request.form.get('course'),form.lesson.data)
        # return redirect(url_for('Test_paper.meq_upload'))