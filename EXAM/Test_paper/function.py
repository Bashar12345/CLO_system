# import json
# import fileinput
# from PIL import Image
from EXAM.configaration import user_obj
from flask import render_template, request, redirect, url_for, flash

from EXAM.model import Machine_learning_mcq_model, course_model, exam_written_question_paper, exam_mcq_question_paper, \
    set_exam_question_slot, McqQuestion, teacher_created_courses_model, user, \
    mcq_answer_paper
from EXAM.users.utils import saveFormFile_in_Filesystem

# from mongoengine import *

# test purpose
exam_code = ''


# binary style e data database e dhukanor jonno If needed in some scenario


# end binary style block


def mcq_question_Upload_part1(get_form, option):
    form = get_form
    exam_code = form.exam_code.data

    if request.method == "POST":
        exam_title = form.exam_title.data
        exam_course = form.exam_course.data
        exam_topic = form.exam_topic.data
        exam_start_time = request.form.get('start_time')
        # exam_start_time = form.exam_start_time.data
        # print(" form time ", exam_start_time)
        exam_end_time = request.form.get("end_time")
        t = form.exam_date.data
        exam_date = t.strftime('%Y-%m-%d')
        # print(t," change kora time ",exam_date)
        caption = request.form.get('Note:captions')
        # caption = form.caption.data
        try:
            if exam_code:
                mongodb_data_class_ins = exam_mcq_question_paper()
                mongodb_data_class_ins.exam_code = exam_code
                mongodb_data_class_ins.exam_title = exam_title
                mongodb_data_class_ins.exam_course = exam_course
                mongodb_data_class_ins.exam_topic = exam_topic
                mongodb_data_class_ins.exam_start_time = exam_start_time
                mongodb_data_class_ins.exam_end_time = exam_end_time
                mongodb_data_class_ins.exam_date = exam_date
                mongodb_data_class_ins.caption = caption

                mongodb_data_class_ins.save()
                mongodb_data_class_slot_ins = set_exam_question_slot()
                mongodb_data_class_slot_ins.exam_title = exam_title
                mongodb_data_class_slot_ins.exam_topic = exam_topic
                mongodb_data_class_slot_ins.exam_course = exam_course
                mongodb_data_class_slot_ins.exam_start_time = exam_start_time
                mongodb_data_class_slot_ins.exam_end_time = exam_end_time
                mongodb_data_class_slot_ins.exam_date = exam_date
                mongodb_data_class_slot_ins.save()
                print("question_info_Data_Entered in nosql successfully")
        except Exception as e:
            print('Data dhuke  NAiiiiii')
            print(str(e))
    return exam_code


def mcq_question_Upload_part2(number_of_questions, code):
    if request.method == "POST":
        mcq_question_options_tuple = list()
        mcq_question_dictionary = dict()
        length = 0
        op = number_of_questions  # question publishing count
        if op:
            for i in range(int(op)):
                length = length + 1
        # print(length)
        count = [1]
        for i in range(length):
            # print(i)
            template_name_of_question = "question" + str(i)
            # print(question)
            mcq_Question = request.form.get(template_name_of_question)
            # mcq_Question = form.question.data
            for j in range(4):
                # print('j = ', j)
                template_name_of_questions_options = "op" + str(count)
                # print(option)
                mcq_options = request.form.get(
                    template_name_of_questions_options)
                count.append(count.pop() + 1)
                mcq_question_options_tuple.append(mcq_options)
            print(mcq_question_options_tuple)
            mcq_question_dictionary.update(
                {mcq_Question: mcq_question_options_tuple})
            # print(mcq_question_dictionary)
            mcq_question_options_tuple = []
            # print(mcq_question_options_tuple)
        else:
            print('checking mcqqu html Finished ')
        print('eta function er exam code', code)
        MCQ = McqQuestion(exam_code=code, question_dictionary=mcq_question_dictionary,
                          list_of_mcq_option=mcq_question_options_tuple)
        exam_mcq_question_paper.objects(
            exam_code=code).update(mcq_question=MCQ)

        '''q = McqQuestion.objects(exam_code='swe421')
        for i in q:
            c = i["exam_code"]
            d = i['dic_ques']
            l = i['list_ques']
        print(c, d, l)
        lis = d['question']
        op = d['question'].strip("][").split(",")  # covert str to list
        print(op, type(op))'''
        # print(question_dictionary)
        flash(f'Question Uploaded Successfully.', 'success')
        return "ok"
    else:
        flash(f'Set up a Question please!', 'danger')
        return " "


def mcq_uploading_processsing(course, topic, Course_outcome, Complexity_label, number_of_question):
    mcq_question_options_tuple = list()
    mcq_question_dictionary = dict()
    op = number_of_question  # question publishing
    length = 0
    if op:
        for i in range(int(op)):
            length = length + 1
        # print(length)
    count = [1]
    for i in range(length):
        # print(i)
        template_name_of_question = "question" + str(i)
        # print(question)
        mcq_Question = request.form.get(template_name_of_question)
        # mcq_Question = form.question.data
        template_name_of_answer = "answer" + str(i)
        mcq_answer = request.form.get(template_name_of_answer)
        for j in range(4):
            # print('j = ', j)
            template_name_of_questions_options = "op" + str(count)
            # print(option)
            mcq_options = request.form.get(
                template_name_of_questions_options)
            count.append(count.pop() + 1)
            mcq_question_options_tuple.append(mcq_options)
        mcq_question_options_tuple.append(mcq_answer)
        print(mcq_question_options_tuple)
        mcq_question_dictionary.update(
            {mcq_Question: mcq_question_options_tuple})
        # print(mcq_question_dictionary)
        mcq_question_options_tuple = []
    else:
        print('checking mcqqu html Finished ')

    mcq_model = Machine_learning_mcq_model()
    mcq_model.course = course
    mcq_model.topic = topic
    mcq_model.course_outcome = Course_outcome
    mcq_model.complexity_label = Complexity_label
    mcq_model.mcq = mcq_question_dictionary
    mcq_model.save()


# ekhane machine learnibg er kaz baki ase
# under construction


def generate_question(get_form):
    form = get_form
    exam_title = form.exam_title.data
    exam_course = request.form.get("course")
    # exam_course = form.exam_course.data
    exam_topic = form.exam_topic.data
    # topic = form.exam_topic.data
    exam_CLO = form.exam_CLO.data
    Complexity_label = request.form.get("complex_level")
    exam_marks = form.exam_marks.data
    number_of_question = request.form.get("numbers_of_questioned")
    exam_start_time = request.form.get('start_time')
    # exam_start_time = form.exam_start_time.data
    # print(" form time ", exam_start_time)
    exam_end_time = request.form.get("end_time")
    t = form.exam_date.data
    exam_date = t.strftime('%Y-%m-%d')
    # print(t," change kora time ",exam_date)
    caption = request.form.get('Note:captions')
    exam_code = form.exam_code.data


def confirmation_of_question(get_form):
    form = get_form
    exam_code = form.exam_code.data
    print(exam_code)
    # mongodb_written_question = exam_written_question_paper()
    # mongodb_mcq_question = exam_MCQ_question_paper()
    written_question = exam_written_question_paper.objects(
        exam_code=exam_code).first()
    mcq_question = exam_mcq_question_paper.objects(exam_code=exam_code).first()
    if written_question:
        print(written_question)
        return render_template('wran.html', written_question=written_question, title='Writen_answer_Page')
    elif mcq_question:
        print(mcq_question)
        return render_template('mcqan.html', mcq_question=mcq_question, title='MCQ_answer_Page')
    else:
        flash(f'Wrong code!!', 'danger')
        # return redirect(url_for('Test_paper.secret_code'))


# Written question can be also modify in this function like ssc exam, hsc exam ,bcs exam
# the concept is ""already included pattern"" of different types of question
def written_question_Upload(get_form):
    form = get_form
    if request.method == "POST":
        exam_code = form.exam_code.data
        exam_title = form.exam_title.data
        exam_course = form.exam_course.data
        exam_topic = form.exam_topic.data
        exam_start_time = request.form.get('start_time')
        # exam_start_time = form.exam_start_time.data
        # print(" time", exam_start_time)
        exam_end_time = request.form.get("end_time")
        t = form.exam_date.data
        exam_date = t.strftime('%Y-%m-%d')
        rename_file = form.rename_file.data
        # print(rename)
        uploadFile = form.file.data
        print(uploadFile)
        doc_file_name, file_path, f_ext, random_name_file = saveFormFile_in_Filesystem(
            uploadFile)  # Akane filer name ase ar location
        print(f_ext)
        # print(doc_fileSystem)
        # binary_data, f_ext = binary_read(uploadFile)
        # print(binary_data)
        try:
            mongodb_data_class_ins = exam_written_question_paper()
            mongodb_data_class_ins.exam_code = exam_code
            mongodb_data_class_ins.exam_title = exam_title
            mongodb_data_class_ins.exam_course = exam_course
            mongodb_data_class_ins.exam_topic = exam_topic
            mongodb_data_class_ins.exam_start_time = exam_start_time
            mongodb_data_class_ins.exam_end_time = exam_end_time
            mongodb_data_class_ins.exam_date = exam_date
            mongodb_data_class_ins.rename_file = rename_file + f_ext
            # new_name = random_hex + f_ext
            # mongodb_data_class_ins.file_extension = f_ext
            # binary_data = open(file_path, "rb")    # file binary te khule database e disi
            # mongodb_data_class_ins.binary_file.put(binary_data, filename=doc_file_name,
            #    metadata={"a": "b"})  # new_name dewa jabee
            fd = open(file_path, "rb")
            mongodb_data_class_ins.binary_file.put(debug 
            mongodb_data_class_slot_ins.exam_topic = exam_topic
            mongodb_data_class_slot_ins.exam_course = exam_course
            mongodb_data_class_slot_ins.exam_start_time = exam_start_time
            mongodb_data_class_slot_ins.exam_end_time = exam_end_time
            mongodb_data_class_slot_ins.exam_date = exam_date
            mongodb_data_class_slot_ins.save()
            print("Data_Entered in nosql successfully")
            flash(f'Question Uploaded Successfully.', 'success')
            return redirect(url_for('Test_paper.examiner'))
            # return redirect(url_for('main.main_page'))
        except Exception as e:
            flash(f'Try again!', 'danger')
            print(str(e))


def written_question_answer_submit(get_form):
    form = get_form
    if request.method == "POST":
        student_id = form.student_id.data
        answer = form.answer.data


# ekhane sob question ane rakte hobe


def mcq_question_answer_submit(get_form):
    form = get_form
    answer_dictionary = {}
    ques_counter = 1
    count = [1]
    fullname = form.fullname.data
    exam_organization_id = form.organization_id.data
    get_answer = 'answer' + str(count)
    while request.form.get(get_answer):
        answer = request.form.get(get_answer)
        if answer is not None:
            print(answer)
            dictionary = {str(ques_counter): answer}
            answer_dictionary.update(dictionary)
            ques_counter = ques_counter + 1
            count.append(count.pop() + 1)
            get_answer = 'answer' + str(count)
        else:
            break
    print(answer_dictionary)
    Exam_attender = user.objects.filter(
        organization_id=exam_organization_id).first()
    if Exam_attender:
        mcq_answer_paper_ins = mcq_answer_paper()
        mcq_answer_paper_ins.name = fullname
        mcq_answer_paper_ins.organization_id = Exam_attender['organization_id']
        mcq_answer_paper_ins.user_name = Exam_attender['user_name']
        mcq_answer_paper_ins.email = Exam_attender['email']
        # mcq_answer_paper_ins.photo = Exam_attender['profile_pic']
        mcq_answer_paper_ins.answer = answer_dictionary
        mcq_answer_paper_ins.save()
    return 'done'


def paginate_page():
    previous_page = ""
    next_page = ""
    top = ""
    bottom = ""
    page = 2
    per_page = 5
    # Only the first 5 people
    exam_question_slot = set_exam_question_slot.objects[:5]

    # All except for the first 5 people
    exam_question_slot = set_exam_question_slot.objects[5:]

    # 5 users, starting from the 11th user found
    exam_question_slot = set_exam_question_slot.objects[10:15]
    # 404 if object doesn't exist
    paginated_course = course_model.objects.paginate(page=page, per_page=per_page)
    print(paginated_course)

    # paginated_slots = set_exam_question_slot.objects.paginate(
    #    page=page, per_page=per_page)
    # print(paginated_slots)
