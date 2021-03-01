from EXAM import nosql
from EXAM.model import user, user_teacher


class data(nosql.Document):
    exam_code = nosql.StringField()
    name = nosql.StringField()


# dic_ques = nosql.DictField()
#  list_ques =nosql.ListFeild()
# embed_ques =nosql.istField(EmbeddedDocumentField())
# def __repr__(self):
# return f"McqQuestion('{self.exam_code}','{self.name}'"


'''data3 = data(exam_code='234', name='bashar')
data1 = data(exam_code='123', name='aysha')
data2 = data(exam_code='456', name='salehin')
data3.save()
data1.save()
data2.save()

for i in user.objects.get(id):
    print(i)

    name = 'bashar'
nm = set_exam_question_slot.objects()
t = datetime.datetime.now()
date = t.strftime("%Y-%m-%d")
print(date)
for i in set_exam_question_slot.objects():
    print(i['exam_date'])
    if i['exam_date'] < date:
        expire_date = i['exam_date']
        set_exam_question_slot.objects(exam_date=expire_date).delete()
        print("old")

for i in set_exam_question_slot.objects():
    print(i['exam_date'])'''


# n = nm['exam_code']
# n = nm.exam_code
# print(n)
# dic = {"name": "bashar"}
# li = []


class user_object:
    def __fun(self):
        print("Private method")
        print(self)

        # Calling private method via

    # another method
    def Help(self, e):
        self.__fun()
        return 'yes'

    # Driver's code


users = user_teacher.objects(email="bashar@example.com").first()

obj = user_object()
# obj.__fun(users['email'])
r = obj.Help('bashar@example.com')
print(r)

user_ob = user_object()
# user_ob.user_object = users['email']
# print(user_ob)
