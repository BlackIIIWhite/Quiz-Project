from django.contrib import admin
from .models import Quiz, Test, CreateClass ,TeacherInfo, StudentInfo, JoinClass ,Test_quiz,Result,Student,Teacher # Make sure models are correctly named

class QuizAdmin(admin.ModelAdmin):
    list_display = ( 'question_id',
        'question', 'answer',
        'option1', 'option2', 'option3', 'option4',
        'option1_click', 'option2_click', 'option3_click', 'option4_click',
        'created_at', 'updated_at','test_id'
    )
    search_fields = ('question', 'answer', 'option1', 'option2', 'option3', 'option4')
    list_filter = ('created_at', 'updated_at')
    list_per_page = 100
    list_editable = ('option1', 'option2', 'option3', 'option4','test_id')
    list_display_links = ('question', 'answer')
    list_max_show_all = 100

admin.site.register(Quiz, QuizAdmin)


class TestAdmin(admin.ModelAdmin):  
    list_display = ('test_id', 'test_name','test_code','number_of_questions','test_duration', 'test_created_at', 'test_updated_at')
    search_fields = ('test_name',)
    list_filter = ('test_created_at', 'test_updated_at')
    list_per_page = 10
    list_display_links = ('test_name',)
    list_max_show_all = 100

admin.site.register(Test, TestAdmin)



class TeacherInfoAdmin(admin.ModelAdmin):
    list_display = ('user_name' ,'name_teacher','teacher_id','created_at','updated_at','year')
    search_fields = ('user_name','teacher_id')
    list_filter = ('created_at','updated_at')
    list_per_page = 10
    list_max_show_all = 100    
    
admin.site.register(TeacherInfo,TeacherInfoAdmin)    


class CreateClassAdmin(admin.ModelAdmin):
    list_display = ('user_name','name_teacher','subject','Shortcut_sub','section','class_code')
    search_fields = ('user_name','subject','Shortcut_sub','class_code')
    list_filter = ('created_at', 'updated_at')
    list_per_page = 10
    list_max_show_all = 100
     
admin.site.register(CreateClass,CreateClassAdmin)    
# Register your models here.

class StudentInfoAdmin(admin.ModelAdmin):
    list_display = ('std_id','student_name','username','std_prn','std_sec','no_subject','std_created_at','std_updated_at','std_roll')
    search_fields = ('std_prn', 'student_name', 'std_id')
    list_per_page = 10
    list_max_show_all = 100

admin.site.register(StudentInfo, StudentInfoAdmin)

class JoinClassAdmin(admin.ModelAdmin):
    list_display = ('std_cla_code','sub_name','student_id','std_created_at','std_updated_at')
    search_fields = ('student_id__student_name', 'student_id__std_prn')
    list_editable = ('sub_name',)
    list_per_page = 10
    list_max_show_all = 100


admin.site.register(JoinClass, JoinClassAdmin)


class TestQuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'std_name', 'PRN','std_section','question_id', 'option_click', 'test_created_at', 'test_updated_at')
    search_fields = ('user_name', 'std_name', 'PRN', 'question_id__question')
    list_filter = ('test_created_at', 'test_updated_at')
    ordering = ('-test_created_at',)
    
admin.site.register(Test_quiz, TestQuizAdmin)

class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'std_name','user_name', 'PRN','std_section','marks','subject_name', 'test_created_at', 'test_updated_at')
    search_fields = ( 'std_name', 'PRN')
    list_filter = ('test_created_at', 'test_updated_at')
    ordering = ('-test_created_at',)
    
admin.site.register(Result, ResultAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

admin.site.register(Student, StudentAdmin)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('username', 'email') 

admin.site.register(Teacher, TeacherAdmin)   
