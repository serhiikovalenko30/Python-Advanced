from mongoengine import *

connect('students')


class Group(Document):
    group_name = StringField(max_length=128)


class Marks(Document):
    marks = IntField(min_value=0)


class Curator(Document):
    curator_name = StringField(max_length=128)


class Faculty(Document):
    faculty_name = StringField(max_length=128)


class Student(Document):
    name = StringField(max_length=128)
    group_name = ReferenceField(Group)  # fixed. was  ListField(ReferenceField(Group))
    marks = ListField(ReferenceField(Marks))
    curator_name = ReferenceField(Curator)  # fixed. was  ListField(ReferenceField(Curator))
    faculty_name = ReferenceField(Faculty)  # fixed. was  ListField(ReferenceField(Faculty))

    def avg_marks(self):
        # amount, count = 0, 0
        # for mark in self.marks:
        #     amount += mark.marks
        #     count += 1
        # return sum(self.marks) / len(self.marks)
        return sum(self.marks) / len(self.marks)

    @classmethod
    def get_top_star_students_by_faculty(cls, faculty=None):
        if faculty is None:
            star_student = {}
            for student in cls.objects():
                star_student[student.id] = student.avg_marks()
            return dict(sorted(star_student.items(), key=lambda item: item[1], reverse=True)[:3])
        else:
            star_student = {}
            for student in cls.objects(faculty_name=faculty):
                star_student[student.id] = student.avg_marks()
            return dict(sorted(star_student.items(), key=lambda item: item[1], reverse=True)[:3])

    @classmethod
    def get_students_by_curator(cls, curator=None):
        if curator is None:
            return cls.objects
        return cls.objects(curator_name=curator)
