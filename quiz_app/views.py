from django.shortcuts import render
from accounts.models import account
from django.http import HttpResponse
from quiz.models import Quiz,Test
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from datetime import timedelta
import string
import random
from urllib.parse import urlencode
from quiz.models import TeacherInfo , CreateClass
from quiz.models import StudentInfo , JoinClass ,Test_quiz,Result,Teacher,Student
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Sum


def landing(request):
    return render(request, 'landing.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role')
        account.objects.create(username=username, password=password, email=email, role=role)
        return render(request, 'login.html')
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role')
        account.objects.create(username=username, password=password, email=email, role=role)
        return render(request, 'login.html')
    return render(request, 'login.html')

def quiz(request):
    return render(request, 'quiz.html')

def quiz_an(request):
    if request.method == 'POST':
        post_data = request.POST
        count = 0
        username = request.session.get('username')

        quiz_list = Quiz.objects.filter(test_id=post_data.get('test_id'))

        std_info = StudentInfo.objects.filter(username=username).first()
        if not std_info:
            return HttpResponse("Student info not found.")

        code = request.POST.get('code')

        class_info = JoinClass.objects.filter(student_id=std_info).first()
        if not class_info:
            return HttpResponse("Class info not found.")

        for q in quiz_list:
            answer_key = f'answer_{q.question_id}'
            selected_answer = post_data.get(answer_key)
            print(f"Question ID: {q.question_id}, Selected Answer: {selected_answer}")
            print(f"Correct Answer: {q.answer}")

            if selected_answer == q.answer:
                count += 1

            Test_quiz.objects.create(
                user_name=username,
                std_name=std_info.student_name,
                std_section=std_info.std_sec,
                question_id=q,
                option_click=selected_answer,
                PRN=std_info.std_prn
            )

        Result.objects.create(
            std_name=std_info.student_name,
            user_name = username,
            std_section=std_info.std_sec,
            subject_name=class_info.sub_name,
            marks=count,
            PRN=std_info.std_prn
        )

        print(f"Total Correct Answers: {count}")


        no_subject = StudentInfo.objects.filter(username=username).aggregate(Sum('no_subject'))['no_subject__sum'] or 0
        name_subject = JoinClass.objects.filter(student_id__username=username).values_list('sub_name', flat=True)

        return render(request, 'dashboard_student.html', {
            'no_subject': no_subject,
            'name_subject': name_subject,
            'username': username
        })



def dashboard_st(request):

    username = request.session.get('username')
    if not request.session.get('teacher_id'):
        return redirect('login_teach')
    

    teacher = Teacher.objects.get(teacher_id=request.session['teacher_id'])  

    try:
        teacher_info = TeacherInfo.objects.get(user_name=teacher.username)
    except TeacherInfo.DoesNotExist:
        return render(request, 'dashboard_st.html', {'error': 'Teacher profile not found.'})

    number = range(teacher_info.no_section)
    name = teacher_info.name_teacher

    classes = CreateClass.objects.filter(teacher_id=teacher_info.teacher_id)

    # Prepare lists of data
    sections = [cls.section for cls in classes]
    subjects = [cls.subject for cls in classes]

    class_data = [{'section': cls.section, 'subject': cls.subject} for cls in classes]

    return render(request, 'dashboard_st.html', {
        'number': number,
        'class_data': class_data,
        'name': name,
        'username': teacher.username
})


def dashboard_student(request):
    if not request.session.get('student_id'):
        return redirect('login')

    student_id = request.session.get('student_id')
    student = Student.objects.get(student_id=student_id)
    username = request.session.get('username')

    # Use filter() instead of get()
    std_classes = StudentInfo.objects.filter(username=username)

    # If you want to handle the case where no StudentInfo exists:
    if not std_classes.exists():
        no_subject = 0
        std_join_cla = []
    else:
        # You can combine the no_subject from all entries or take the latest
        no_subject = sum(c.no_subject for c in std_classes)

        # Assuming std_join_cla should get JoinClass entries for all StudentInfo records
        std_join_cla = JoinClass.objects.filter(student_id__in=std_classes)

    context = {
        'student': student,
        'no_subject': no_subject,
        'name_subject': [join.sub_name for join in std_join_cla],
        'username': username
    }

    return render(request, 'dashboard_student.html', context)


def result(request):
    username = request.session.get('username')
    subject_names = CreateClass.objects.filter(user_name=username).values_list('subject', flat=True)
    results = Result.objects.filter(subject_name__in=subject_names).order_by('-test_created_at')
    context ={
        'results': results,
        'username': username
    }
    return render(request, 'result.html', context)

def test_info(request):
    test_code = generate_test_code()

    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        number_of_question = request.POST.get('NofQ')
        test_time = request.POST.get('test_time')

        if not test_name or not number_of_question or not test_time:
            messages.error(request, "Please fill in all fields.")
            return render(request, 'test_info.html', {'test_code': test_code})

        duration = timedelta(minutes=int(test_time))

        Test.objects.create(
            test_name=test_name,
            number_of_questions=int(number_of_question),
            test_duration=duration,
            test_code=test_code
        )

        return redirect(f"/quiz_create/?test_code={test_code}&number_of_question={number_of_question}")

    return render(request, 'test_info.html', {'test_code': test_code})




def generate_test_code(length=10):
    characters = string.ascii_letters + '123456789'
    return ''.join(random.choices(characters, k=length))


def quiz_create(request):
    if request.method == 'GET':
        test_code = request.GET.get('test_code')
        number_of_question = request.GET.get('number_of_question')

        if not test_code or not number_of_question:
            messages.error(request, "Missing test code or number of questions.")
            return redirect('test_info')

        numbers = range(1, int(number_of_question) + 1)

        return render(request, 'quiz_create.html', {
            'test_code': test_code,
            'number_of_question': number_of_question,
            'numbers': numbers
        })

    elif request.method == 'POST':
        test_code = request.POST.get('test_code')

        try:
            test_instance = Test.objects.get(test_code=test_code)
        except Test.DoesNotExist:
            messages.error(request, "Test not found for the given code.")
            return redirect('test_info')

        number = int(test_instance.number_of_questions)

        for i in range(1, number + 1):
            question_text = request.POST.get(f'question_{i}')
            question_no = request.POST.get(f'question_no_{i}')
            option1 = request.POST.get(f'answer-{i}-1')
            option2 = request.POST.get(f'answer-{i}-2')
            option3 = request.POST.get(f'answer-{i}-3')
            option4 = request.POST.get(f'answer-{i}-4')
            correct_answer = request.POST.get(f'answer-{i}-5')

            Quiz.objects.create(
                question=question_text,
                question_no = question_no,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                answer=correct_answer,
                test_id=test_instance
            )

        messages.success(request, "Quiz successfully created!")
        return redirect('dashboard_st')

def create_class(request):
    class_code = generate_test_code()
    if request.method == 'POST':
        username = request.session.get('username')
        if not username:
            return HttpResponse("Session expired or user not logged in.", status=401)
        name_subject = request.POST.get('NofS')
        name_teacher = request.POST.get('NofT', '').strip()
        shortcut_sub = request.POST.get('SniS')
        section = request.POST.get('FwS')

        # Try to get or create TeacherInfo with correct defaults
        teacher, created = TeacherInfo.objects.get_or_create(
            name_teacher=name_teacher,
            defaults={'user_name': username, 'no_section': 0}
        )

        # Increment no_section if teacher exists or was just created
        teacher.no_section += 1
        teacher.save()

        # Create the class entry
        new_class = CreateClass.objects.create(
            user_name=username,
            name_teacher=name_teacher,
            subject=name_subject,
            Shortcut_sub=shortcut_sub,
            section=section,
            class_code=class_code,
            teacher_id=teacher
        )
        return redirect('dashboard_st')

    else:
        return render(request, "create_class.html", {'class_code': class_code})


    
def upload(request):
    return render(request,"upload.html")

def join_class(request):
    username = request.session.get('username')
    if request.method == 'POST': 
        student_name = request.POST.get('Nofs')
        std_prn = request.POST.get('PRN')
        std_sec = request.POST.get('section_cla')
        std_roll = request.POST.get('RollN')
        std_cla_code = request.POST.get('Class_code')

        # Check if class code is valid
        try:
            class_obj = CreateClass.objects.get(class_code=std_cla_code)
        except CreateClass.DoesNotExist:
            return redirect('dashboard_student')

        # Try to get existing student by PRN and section
        student, created = StudentInfo.objects.get_or_create(
            std_prn = std_prn,
            username = username,
            std_sec = std_sec,
            defaults={
                'student_name': student_name,
                'std_roll': std_roll,
                'no_subject': 1
            }
        )

        if not created:
            student.no_subject += 1
            student.save()

        # Add to JoinClass
        JoinClass.objects.create(
            std_cla_code=std_cla_code,
            sub_name=class_obj.subject,
            student_id=student
        )

        # Prepare context
        no_subject = student.no_subject
        name_subject = JoinClass.objects.filter(student_id=student).values_list('sub_name', flat=True)

        # Render dashboard_student.html with context
        return render(request, 'dashboard_student.html', {
            'no_subject': no_subject,
            'name_subject': name_subject
        })

    return render(request, 'join_class.html',{'username': username})


def join_test(request):
    username = request.session.get('username')
    if request.method == 'POST': 
        code = request.POST.get('test_code')

        # Check if test_code is provided
        if not code:
            messages.error(request, "Please provide a valid test code.")
            return redirect('join_test')

        try:
            testmodel = Test.objects.get(test_code=code)
        except Test.DoesNotExist:
            messages.error(request, "Test not found for the given code.")
            return redirect('join_test')  # Or handle this differently based on your requirements

        # Proceed to retrieve the quiz set if test is found
        quiz_set = Quiz.objects.filter(test_id=testmodel.test_id)
        test_du = testmodel.test_duration
        return render(request, 'quiz_an.html', {
            'quiz_list': quiz_set,
            'test_du': int(test_du.total_seconds()),
            'test_id': testmodel.test_id,
            'code': code
        })

    return render(request, 'join_test.html',{'username': username})


def file(request):
    test_code = generate_test_code()

    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        number_of_question = int(request.POST.get('NofQ'))
        test_time = request.POST.get('test_time')
        uploaded_file = request.FILES['file']
        submitted_test_code = request.POST.get('test_code')

        if not submitted_test_code:
            messages.error(request, "Test code is missing.")
            return render(request, 'file.html', {'test_code': test_code})

        file_content = uploaded_file.read().decode('utf-8')

        if not test_name or not number_of_question or not test_time:
            messages.error(request, "Please fill in all fields.")
            return render(request, 'file.html', {'test_code': test_code})

        duration = timedelta(minutes=int(test_time))


        test_instance = Test.objects.create(
            test_name=test_name,
            number_of_questions=int(number_of_question),
            test_duration=duration,
            test_code=submitted_test_code
        )

        input_lines = file_content.split("\n")
        i = 0
        for _ in range(number_of_question):
            if i >= len(input_lines):
                break

            question = input_lines[i].strip()
            i += 1
            while i < len(input_lines) and input_lines[i].strip() == "":
                i += 1

            option_1 = input_lines[i].strip(); i += 1
            while i < len(input_lines) and input_lines[i].strip() == "":
                i += 1

            option_2 = input_lines[i].strip(); i += 1
            while i < len(input_lines) and input_lines[i].strip() == "":
                i += 1

            option_3 = input_lines[i].strip(); i += 1
            while i < len(input_lines) and input_lines[i].strip() == "":
                i += 1

            option_4 = input_lines[i].strip(); i += 1
            while i < len(input_lines) and input_lines[i].strip() == "":
                i += 1

            answer = input_lines[i].strip(); i += 1
            while i < len(input_lines) and input_lines[i].strip() == "":
                i += 1

            Quiz.objects.create(
                question=question,
                option1=option_1,
                option2=option_2,
                option3=option_3,
                option4=option_4,
                answer=answer,
                test_id=test_instance
            )

        messages.success(request, "Test and quiz questions successfully created!")
        return redirect('dashboard_st')

    return render(request, 'file.html', {'test_code': test_code})


def result_student(request):
    username = request.session.get('username')
    std_info = StudentInfo.objects.get(username=username)
    results = Result.objects.filter(PRN=std_info.std_prn).order_by('-test_created_at')
    
    context = {
        'results': results,
        'username':username
    }
    return render(request, 'result_student.html', context)


def SignupPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        hashed_password = make_password(password)  # 🔒 Hash the password
        student = Student.objects.create(
            username=username,
            email=email,
            password=hashed_password,
        )

        # return HttpResponse("Student registered successfully!")
        return redirect('login')

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(email=email)
            if check_password(password, student.password):
                request.session['student_id'] = student.student_id
                request.session['username'] = student.username
                return redirect('dashboard_student')  
            else:
                return HttpResponse("Invalid password.")
        except Student.DoesNotExist:
            return HttpResponse("User not found.")

    return render(request, 'login.html')

def LogoutPage(request):
    request.session.flush()
    return redirect('landing')


def SignupPage_teacher(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        hashed_password = make_password(password)
        Teacher.objects.create(
            email=email,
            username=username,
            password=hashed_password,
        )
        return redirect('login_teach')
    return render(request, 'signup_teach.html')


def LoginPage_teacher(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            teacher = Teacher.objects.get(email=email)
            if check_password(password, teacher.password):
                # Use teacher_id here
                request.session['teacher_id'] = teacher.teacher_id
                request.session['username'] = teacher.username
                return redirect('dashboard_st')
            else:
                return render(request, 'login_teach.html', {'error': 'Invalid password'})
        except Teacher.DoesNotExist:
            return render(request, 'login_teach.html', {'error': 'User not found'})
    return render(request, 'login_teach.html')


def LogoutPage_teacher(request):
    request.session.flush()
    return redirect('landing')

