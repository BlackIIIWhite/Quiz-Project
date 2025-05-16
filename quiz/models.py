from django.db import models
from datetime import timedelta
from django.utils import timezone

class Test(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=255)
    test_created_at = models.DateTimeField(auto_now_add=True)
    test_updated_at = models.DateTimeField(auto_now=True)
    number_of_questions = models.IntegerField(default=0)
    test_duration = models.DurationField(default=timedelta(minutes=30))
    test_code= models.CharField(max_length=255, default='TES5TA56BX')
    

    def __str__(self):
        return str(self.test_id)


class Quiz(models.Model):
    question_id = models.AutoField(primary_key = True)
    question = models.TextField()
    answer = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()
    option1_click = models.IntegerField(default=0)
    option2_click = models.IntegerField(default=0)
    option3_click = models.IntegerField(default=0)
    option4_click = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Reference the Test model correctly
    test_id = models.ForeignKey('Test', on_delete=models.CASCADE, null=True)
  # null=True just to allow migration for now

    def __str__(self):
        return str(self.question_id)


class TeacherInfo(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=225)
    name_teacher = models.CharField(max_length=225 , unique=True)
    no_section = models.IntegerField(default=0)  
    year = models.CharField(max_length=25 , default= 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.teacher_id)
      
      
class CreateClass(models.Model):
    user_name = models.CharField(max_length=225)
    name_teacher = models.CharField(max_length=225)
    subject = models.TextField()
    Shortcut_sub = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    class_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    teacher_id = models.ForeignKey(
        TeacherInfo,
        on_delete=models.CASCADE,
        db_column='teacher_id_id',
        to_field='teacher_id'  
    )

    def __str__(self):
        return f"{self.subject} - {self.section} (Teacher ID: {self.teacher_id_id})"
    
class StudentInfo(models.Model):
    username = models.TextField(max_length=225,default=0)
    std_id = models.AutoField(primary_key = True)
    student_name = models.TextField(max_length=225)
    std_prn = models.IntegerField()
    std_sec = models.CharField(max_length=225)
    std_roll = models.CharField(default=0)
    no_subject = models.IntegerField(default=0)
    std_created_at = models.DateTimeField(auto_now_add=True)
    std_updated_at = models.DateTimeField(auto_now=True)
    
    def __int__(self):
        return str(self.std_id)
    
class JoinClass(models.Model):
    std_cla_code = models.CharField(max_length=225)
    sub_name = models.TextField(max_length=225)
    std_created_at = models.DateTimeField(auto_now_add=True)
    std_updated_at = models.DateTimeField(auto_now=True)
    
    student_id = models.ForeignKey(
        StudentInfo,
        on_delete=models.CASCADE,
        db_column='student_id_id'
    ) 
     
class Test_quiz (models.Model):
    user_name = models.CharField(max_length=225,default=0)
    std_name = models .CharField(max_length = 225,default=0)
    # marks = models.IntegerField(default=0)
    std_section = models .CharField(max_length = 225,default=0)
    question_id = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        db_column='question_id_id'
    )
    option_click = models.CharField(max_length=225)
    PRN =models.CharField(max_length=225,default=0)
    test_created_at = models.DateTimeField(auto_now_add=True)
    test_updated_at = models.DateTimeField(auto_now=True)

class Result(models.Model):
    std_name = models .CharField(max_length = 225,default=0)
    user_name = models .CharField(max_length = 225,default=0)
    std_section = models .CharField(max_length = 225,default=0)
    subject_name =models .CharField(max_length = 225,default=0)
    marks = models.IntegerField(default=0)
    PRN =models.CharField(max_length=225,default=0)
    test_created_at = models.DateTimeField(auto_now_add=True)
    test_updated_at = models.DateTimeField(auto_now=True)
    
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 

    def __str__(self):
        return self.username    
    
class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  

    def __str__(self):
        return self.username  
    
    
    

    
      
  


