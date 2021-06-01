import datetime
import random

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file,
    Blueprint,
    jsonify,
    make_response, session
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
from EXAM.Test_paper.function import answer_submit, generate_question, machine_process_data, mcq_question_Upload_part1, mcq_question_Upload_part2, mcq_question_answer_submit, mcq_uploading_processing, question_paper_for_current_session, written_question_Upload, written_question_answer_submit
from EXAM.configaration import secret_exam_key, object_of_something, User_type, sum_of_something, user_obj
from EXAM.model import course_model, exam_mcq_question_paper, exam_written_question_paper, machine_learning_mcq_model, marksheet, mcqQuestion, required_for_generate, teacher_created_courses_model
from flask.templating import render_template_string

"""@Test_paper.route('/')
def hello_world():
    return 'Hello World!'
"""

Test_paper = Blueprint("Test_paper", __name__)


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


@Test_paper.route("/file/<filename>")
def file(filename):
    written = exam_written_question_paper.objects.filter(
        rename_file=filename).first()
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


@Test_paper.route("/mcqUpload/<course_code>", methods=["GET", "POST"])
@login_required
def mcq_upload(course_code):
    form = mcq_upload_form_part_1()
    course_code, course_date = course_code.split("=")
    session['course_date'] = course_date

    # seach course code and fetch the lessons
    # under construction
    # course_title_list = course_model.objects.only("course_title")
    # course_title = []
    # for title in course_title_list:
    #     # print(title.course_title)
    #     if title.course_title not in course_title:
    #         course_title.append(title.course_title)

    lessons_of_current_course_code = []
    user_email = user_obj.e
    couse_code_list = teacher_created_courses_model.objects(
        teacher_registered_id=user_email)
    
    corse_code = course_code
    if corse_code == "teacher":
        course_code = []
        for crse_code in couse_code_list:
            # print(title.course_title)
            if crse_code.course_code not in course_code:
                course_code.append(crse_code.course_code)
    else:
        lsns = teacher_created_courses_model.objects(
            course_code=corse_code, teacher_registered_id=user_email, course_duration=course_date).first()
        # course_title_of_current_course = lsns.course_title
        lessons_of_current_course_code = lsns.course_lessons
        # clo=lsns.course_co
        print(lessons_of_current_course_code)
    if request.method == "POST":
        mcq_uploading_processing(form, corse_code)
    return render_template(
        "mcq/mcqupload.html",
        title="mcqUpload",
        form=form,
        user_type=User_type.user_type,
        course_code=course_code,
        corse_code=corse_code,
        lessons_of_current_course_code=lessons_of_current_course_code
        # course_title_of_current_course=course_title_of_current_course
        # ,clo=clo
        # course_title=course_title,
    )


# @Test_paper.route("/mcq_upload_option_check")
# @login_required
# def mcq_upload_option_check():
#     response_to_browser = ""
#     option_empty=''
#     if request.args:
#         option = request.args.get("op")
#         print(option)
#         print(request.form.get(option))
#         if request.args.get(option):
            
#             option_empty="data_ase"
#         response_to_browser = make_response(jsonify(option_empty))
#         print(response_to_browser)
#     return response_to_browser









@Test_paper.route("/mcqUpload_course_code_selection_load")
@login_required
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
@login_required
def mcqUpload_lesson_selection_load():
    response_to_browser = ""
    if request.args:
        code = request.args.get("c")
        # print(code)
        
        lesn = course_model.objects(
            course_code=code).first()
        # print(type(lesn.course_lessons))
        lessons_list = []
        for lesson in lesn.course_lessons:
            print(lesson)
            lessons_list.append(lesson)
        response_to_browser = make_response(jsonify(lessons_list))
        print(response_to_browser)
    return response_to_browser


@Test_paper.route("/mcqUpload_clo_selection_load")
@login_required
def mcqUpload_clo_selection_load():
    response_to_browser = ""
    if request.args:
        code = request.args.get("c")
        # print(code)
        course_date = session['course_date']
        clo_list = []
        crse_clo = course_model.objects(course_code=code,course_duration=course_date).first()
        print(type(crse_clo.course_co))
        clo_list = crse_clo.course_co
        response_to_browser = make_response(jsonify(clo_list))
        print(response_to_browser)
    return response_to_browser


@Test_paper.route("/generateMCQ/<course_code>", methods=["GET", "POST"])
@login_required
def generateMCQ(course_code):
    form = Mcq_Question_generate_form()
    # if course_code:
    corse_code = course_code
    if course_code == "teacher":
        course_code = course_model.objects.only("course_code")
    if request.method == "POST":
        generate_question(form, corse_code)
    return render_template(
        "mcq/generateMCQ.html",
        title="MCQgenerate",
        form=form,
        user_type=User_type.user_type,
        course_code=course_code,
        corse_code=corse_code)


@Test_paper.route("/generateMCQ_lesson_load")
@login_required
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


@Test_paper.route("/generateMCQ_clo_load")
@login_required
def generateMCQ_clo_load():
    response_to_browser = ""
    if request.args:
        code = request.args.get("c")
        # print(code)
        clo_list = []
        crse_clo = course_model.objects(course_code=code).first()
        print(type(crse_clo.course_co))
        clo_list = crse_clo.course_co
        response_to_browser = make_response(jsonify(clo_list))
        print(response_to_browser)
    return response_to_browser


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
        check_attence = marksheet.objects(exam_code=exam_code).first()
        if check_attence:
            flash(f"You already attend the Exam!!!!", "danger")
            #return redirect(url_for("main.main_page"))
        session['exam_code']=exam_code
        mcq_question = exam_mcq_question_paper.objects.filter(
            exam_code=exam_code).first()
        written_question = exam_written_question_paper.objects.filter(
            exam_code=exam_code).first()
        generated_question = required_for_generate.objects.filter(
            exam_secret_code=exam_code).first()
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
        elif generated_question:
            secret_exam_key.exam_code = exam_code
            return redirect(url_for("Test_paper.mcq_answer_paper_auto_generated"))
        else:
            flash(f"Re-Enter Exam code!!", "danger")
            return redirect(url_for("main.main_page"))
    else:
        return render_template(
            "secret_code.html",
            form=form,
            title="Identify",
            user_type=User_type.user_type,
        )
        # return redirect(url_for('Test_paper.secret_code'))


@Test_paper.route("/mcq_answer_paper", methods=["GET", "POST"])
@login_required
def mcq_answer_paper_auto_generated():
    # mcq_question_answer_submit(form)
    exam_code = secret_exam_key.exam_code
    requirement_for_mcq_questions = required_for_generate.objects(
        exam_secret_code=exam_code).first()
    exam_title = requirement_for_mcq_questions.exam_title
    exam_course = requirement_for_mcq_questions.exam_course
    exam_start_time = requirement_for_mcq_questions.exam_start_time
    exam_end_time = requirement_for_mcq_questions.exam_end_time
    exam_date = requirement_for_mcq_questions.exam_date
    print(exam_start_time, exam_end_time, exam_date)
    year, month, day = exam_date.split("-")
    hour, minute = exam_start_time.split(":")
    end_hour, end_minute = exam_end_time.split(":")
    # print(time)      # print(hour, " minute ase ", minute)
    current_time = datetime.datetime.now()
    # for demo  testing
    current_time2 = current_time
    starting_time_of_exam = datetime.datetime(
        int(year), int(month), int(day), int(hour), int(minute)
    )
    ending_time_of_exam = datetime.datetime(
        int(year), int(month), int(day), int(end_hour), int(end_minute)
    )
    print(f"ending time {ending_time_of_exam}")
    print(f"starting time {starting_time_of_exam}")
    # print(mcq_question['mcq_question'])
    # final showdown e if uncomment krte hobe................................................
    # if starting_time_of_exam <= current_time <= ending_time_of_exam:
    # if starting_time_of_exam <= current_time <= ending_time_of_exam:
    if current_time == current_time2:
        print(current_time)
        # ekahne mcq question object produce krte hobe -------------------------------------------
        question_mcq_for_current_session = question_paper_for_current_session(
            requirement_for_mcq_questions)
        # print(question_mcq_for_current_session)
        session['exam_title'] = exam_title
        session['exam_course'] = exam_course
        session['session_question'] = question_mcq_for_current_session
        session['count'] = 0
        session['total_question'] = requirement_for_mcq_questions.number_of_question
        return render_template_string("""
        {% extends 'layout.html' %}

        {% block body %}
        <div class="card text-center">
              <div class="card-header">

                     <div class="card-body">
                            <h5 class="card-title">Are you mentally prepared for the exam ,and do you accept all the term and
                                   conditions
                                   then Click the Attempt button...</h5>

                            <a href="{{url_for('Test_paper.answer_session')}}" class='btn btn-sm btn-success ' id="btn_next_question" > Attempt</a>
                            <p class="card-text"><br>
                                   If you want to leave..
                            </p>
                            <a href="{{url_for('main.main_page')}}" class="btn btn-warning btn-sm">Turn back</a>
                     </div>
              </div>
       </div>
       {% endblock body %}
       """)

        # return render_template("mcq/mcq_answer_session.html", exam_date=exam_date, exam_end_time=exam_end_time,
        #                        # custom object for answer from the machine learning method
        #                        question_mcq_for_current_session=question_mcq_for_current_session,
        #                        title="MCQ_answer_Page", form=form, user_type=User_type.user_type)
    return render_template(
        "count_Down.html",
        starting_time_of_exam=starting_time_of_exam,
        title="countdown",
    )


selectd_answers = list()
correct_answers = list()
corrected = 0
answer_count = 1


@Test_paper.route("/answer_session", methods=["GET", "POST"])
@login_required
def answer_session():
    form = Mcq_answer_form()
    global correct_answers
    global corrected
    global selectd_answers
    global answer_count
    count = session['count']
    total_question = session['total_question']
    exam_title = session['exam_title']
    exam_course = session['exam_course']
    session_question = session['session_question']
    question_part = ''
    option_list = list()
    shuffled_option_list = list()
    selected_option = ''
    exam_code = secret_exam_key.exam_code
    # print(type(session_question))
    #print("Foooooooooooor testing", len(session_question[count]))
    if answer_count == total_question:  # session['total_question']
        flash(f'Your fiinished the exam ', 'success')
        return redirect(url_for("main.main_page"))
    for i in session_question[count]:
        # print(i)
        question_part = i
    for j in session_question[count][i]:
        # print(j)
        option_list.append(j)
    # print(option_list)
    shuffled_option_list = random.sample(option_list, len(option_list))
    # print(shuffled_option_list)

    db_question = mcqQuestion.objects(question=question_part).first()

    if db_question:
        correct_answers.append(db_question['q_answer'])
        # print(db_question.q_answer)
        print(db_question['q_answer'])


    
    if request.method == "POST":
        # if form.validate_on_submit:
        selected_option = request.form.get('selected_option')
        print(selected_option)
        answer_count+=1
        print(answer_count)
        selectd_answers.append(selected_option)
    session['count'] = count+1
    # print(session['count'])
    # session['count'] # session['session_question']):
    if answer_count == len(session['session_question']):
        #print("correct --------", correct_answers)
        #print("selected ----------", selectd_answers)
        i = 0
        for selected in selectd_answers:
            if selected == correct_answers[i]:
                print("Wright answer")
                corrected += 1
            i += 1  
        total_score = marksheet()
        total_score.exam_code = session['exam_code']
        total_score.student_email = user_obj.e
        total_score.exam_course = exam_course  # session['exam_course']
        total_score.exam_title = exam_title        # session['exam_title']
        total_score.get_score = corrected
        total_score.save()
    
    total = total_question  # session['total_question']

    return render_template("mcq/mcq_answer_session.html", question_part=question_part,  option_list=shuffled_option_list, title="MCQ_answer_Page", form=form, user_type=User_type.user_type)


# @Test_paper.route("/answer_session_load", methods=["GET", "POST"])
# # @login_required
# def answer_session_load():
#     if request.args:
#         count = request.args.get('c')
#     print(count)
#     print(type(count))
#     next_count=3
#     response_to_browser = make_response(jsonify(next_count))
#     print(response_to_browser)
#     return response_to_browser





@Test_paper.route("/model_test", methods=["GET", "POST"])
# @login_required
def model_test():
    post_count = 0
    if request.method == "POST":
        count = 0
        total_question = 15

        course_code = request.form.get("course_code")
        difficulty = request.form.get("question_difficulty")
        model_test_question_paper = machine_process_data(
            course_code, difficulty)
        session['model_test_question'] = model_test_question_paper
        session['count'] = 0
        session['total_question'] = 15
        session['exam_title'] = 'Model_test'
        session['exam_course'] = course_code
        return redirect(url_for('Test_paper.model_test_answer_session'))

    return render_template(
        "student/model_test.html", post_count=post_count, title="MCQ_Model_Test", user_type=User_type.user_type)  # question_part=question_part,  option_list=shuffled_option_list,


selectd_answers = list()
correct_answers = list()
corrected = 0
answer_count = 1



@Test_paper.route("/model_test_answer_session", methods=["GET", "POST"])
@login_required
def model_test_answer_session():
    form = Mcq_answer_form()
    global correct_answers
    global corrected
    global selectd_answers
    global answer_count
    title_count = 1
    count = session['count']
    total_question = session['total_question']
    exam_title = session['exam_title']
    exam_course = session['exam_course']
    session_question = session['model_test_question']
    question_part = ''
    option_list = list()
    shuffled_option_list = list()
    selected_option = ''
    # print(type(session_question))
    #print("Foooooooooooor testing", len(session_question[count]))
    if answer_count == total_question:  # session['total_question']
        flash(f'Your fiinished the exam ', 'success')
        return redirect(url_for("main.main_page"))

    for i in session_question[count]:
        # print(i)
        question_part = i
    for j in session_question[count][i]:
        # print(j)
        option_list.append(j)
    # print(option_list)
    shuffled_option_list = random.sample(option_list, len(option_list))
    # print(shuffled_option_list)

    db_question = mcqQuestion.objects(question=question_part).first()

    if db_question:
        correct_answers.append(db_question['q_answer'])
        # print(db_question.q_answer)
        print(db_question['q_answer'])

    if request.method == "POST":
        # if form.validate_on_submit:
        selected_option = request.form.get('selected_option')
        answer_count +=1
        print(selected_option)

        selectd_answers.append(selected_option)
    session['count'] = count+1
    # print(session['count'])
    # session['count'] # session['session_question']):
    if answer_count == len(session['model_test_question']):
        #print("correct --------", correct_answers)
        #print("selected ----------", selectd_answers)
        i = 0
        for selected in selectd_answers:
            if selected == correct_answers[i]:
                print("Wright answer")
                corrected += 1
            i += 1

        total_score = marksheet()
        total_score.student_email = user_obj.e
        total_score.exam_course = exam_course  # session['exam_course']
        total_score.exam_title = exam_title +"-"+ str(title_count)   # session['exam_title']
        total_score.get_score = corrected
        total_score.save()
        title_count += 1
        print("answer saved")
    total = total_question  # session['total_question']

    return render_template("mcq/model_test_answer_session.html", question_part=question_part,  option_list=shuffled_option_list, title="Model_test_answer", form=form, user_type=User_type.user_type)


@Test_paper.route("/sample", methods=["GET", "POST"])
# @login_required
def sample():
    return render_template(
        "sample.html",
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


# form.course_title.choices=[(course_name,course_name)for course_name in course_title]
# form.course_code.choices=[(codes.course_code,codes.course_code) for codes in course_model.objects(course_title='Thesis & project').all()]
# form.lesson.choices=[(lessons.course_lessons,lessons.course_lessons) for lessons in course_model.objects(course_code='swe451').all()]

# return '<h1> Course title : {}, Lesson : {}</h1>'.format(request.form.get('course'),form.lesson.data)
# return redirect(url_for('Test_paper.meq_upload'))
