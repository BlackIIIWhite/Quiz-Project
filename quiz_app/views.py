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
from quiz.models import StudentInfo , JoinClass ,Test_quiz,Result,Teacher,Student,valid
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Sum
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import base64
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
from ultralytics import YOLO
import json
import cvzone
import math
from django.http import HttpResponse
from openpyxl import Workbook
from PIL import Image, UnidentifiedImageError

def generate_test_code(length=10):
    characters = string.ascii_letters + '123456789'
    return ''.join(random.choices(characters, k=length))
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
        username = request.session.get('username')
        test_id = post_data.get('test_id')
        code = request.POST.get('code')
        test = Test.objects.get(test_code = code)
        
        if not test_id:
            return HttpResponse("Test ID not provided.")

        quiz_list = Quiz.objects.filter(test_id=test_id)
        std_info = StudentInfo.objects.filter(username=username).first()
        if not std_info:
            return HttpResponse("Student info not found.")

        class_info = JoinClass.objects.filter(student_id=std_info).first()
        if not class_info:
            return HttpResponse("Class info not found.")

        count = 0
        test_quiz_entries = []

        for q in quiz_list:
            answer_key = f'answer_{q.question_id}'
            selected_answer = post_data.get(answer_key, "None")
            if selected_answer == q.answer:
                count += 1

            test_quiz_entries.append(
                Test_quiz(
                    user_name=username,
                    std_name=std_info.student_name,
                    std_section=std_info.std_sec,
                    question_id=q,
                    option_click=selected_answer,
                    PRN=std_info.std_prn
                )
            )

        Test_quiz.objects.bulk_create(test_quiz_entries)

        try:
            Result.objects.create(
                std_name=std_info.student_name,
                teach_username = test.teacher_username,
                user_name=username,
                std_section=std_info.std_sec,
                subject_name=test.subject_name,
                marks=count,
                PRN=std_info.std_prn
            )
        except Exception as e:
            return HttpResponse("Failed to save result.")

        no_subject = std_info.no_subject
        name_subject = JoinClass.objects.filter(student_id=std_info).values_list('sub_name', flat=True)
        valid_2=1
        valid.objects.create(
            username = username,
            sub_name = test.subject_name,
            PRN = std_info.std_prn,
            valid = valid_2,
            code = code,
            )
        return render(request, 'dashboard_student.html', {
            'no_subject': no_subject,
            'name_subject': name_subject,
            'username': username
        })

    return HttpResponse("Invalid request method.")

@csrf_exempt
def object_detect(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            img_base64 = data.get('image')
            code = data.get('code')

            if not img_base64 or not code:
                return JsonResponse({'error': 'Missing image or code'}, status=400)

            # Decode base64 image
            img_data = base64.b64decode(img_base64.split(',')[1])

            try:
                img = Image.open(BytesIO(img_data))
                img.verify()  # verify integrity
                img = Image.open(BytesIO(img_data))  # reopen for processing
            except UnidentifiedImageError:
                return JsonResponse({'error': 'Invalid image data'}, status=400)

            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

            model = YOLO("yolov8n.pt")

            username = request.session.get('username')
            if not username:
                return JsonResponse({'error': 'Unauthorized'}, status=403)

            test = Test.objects.get(test_code=code)
            std_info = StudentInfo.objects.filter(username=username).first()

            results = model(frame, verbose=False)

            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    conf = math.ceil((box.conf * 100)) / 100
                    print(f'Detected class: {cls}, Confidence: {conf}')

                    if conf > 0.7 and cls in [65, 67]:
                        if not valid.objects.filter(username=username, sub_name=test.subject_name, PRN=std_info.std_prn).exists():
                            valid.objects.create(
                                username=username,
                                sub_name=test.subject_name,
                                PRN=std_info.std_prn,
                                valid=1,
                                code=code
                            )
                        return JsonResponse({'redirect': True, 'url': '/dashboard_student/'})

            _, buffer = cv2.imencode('.jpg', frame)
            return HttpResponse(buffer.tobytes(), content_type='image/jpeg')

        except Exception as e:
            print(f"Internal Error: {e}")
            return JsonResponse({'error': 'Server error', 'details': str(e)}, status=500)

    return HttpResponse(status=400)

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
    username = request.session.get('username')
    print(username)
    return render(request, 'dashboard_st.html', {
        'number': number,
        'class_data': class_data,
        'name': name,
        'username':  username
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
    username = request.session.get('username')
    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        number_of_question = request.POST.get('NofQ')
        test_time = request.POST.get('test_time')
        test_code = request.POST.get('test_code')

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
    context ={
        'test_code': test_code,
        'username': username
    }
    test_code = generate_test_code()
    return render(request, 'test_info.html', {context})


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
    if request.method == 'POST':
        username = request.session.get('username')
        if not username:
            return HttpResponse("Session expired or user not logged in.", status=401)
        name_subject = request.POST.get('NofS')
        name_teacher = request.POST.get('NofT', '').strip()
        shortcut_sub = request.POST.get('SniS')
        section = request.POST.get('FwS')
        class_code_1 = request.POST.get('class_code')

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
            class_code=class_code_1,
            teacher_id=teacher
        )
        return redirect('dashboard_st')

    else:
        class_code_1 = generate_test_code()
        return render(request, "create_class.html", {'class_code': class_code_1})


    
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
        valid_username = valid.objects.filter(username = username , code =code, valid = 1 ).first()
        if valid_username:
            messages.error(request, "Test Already Given Or Tried to cheat ")
            return redirect('join_test')

        # Check if test_code is provided
        if not code:
            messages.error(request, "Please provide a valid test code.")
            return redirect('join_test')

        try:
            testmodel = Test.objects.get(test_code=code)
        except Test.DoesNotExist:
            messages.error(request, "Test not found for the given code.")
            return redirect('join_test')  # Or handle this differently based on your requirements


        quiz_set = Quiz.objects.filter(test_id=testmodel.test_id).order_by('?')
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
    username = request.session.get('username')
    # Fetch all classes created by this teacher
    class_list = CreateClass.objects.filter(user_name=username)

    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        number_of_question = int(request.POST.get('NofQ'))
        test_time = request.POST.get('test_time')
        uploaded_file = request.FILES['file']
        submitted_test_code = request.POST.get('test_code')
        subject_name = request.POST.get('class_option')

        if not submitted_test_code:
            messages.error(request, "Test code is missing.")
            return render(request, 'file.html', {'test_code': test_code, 'class_list': class_list})

        file_content = uploaded_file.read().decode('utf-8')

        if not test_name or not number_of_question or not test_time:
            messages.error(request, "Please fill in all fields.")
            return render(request, 'file.html', {'test_code': test_code, 'class_list': class_list})

        duration = timedelta(minutes=int(test_time))

        test_instance = Test.objects.create(
            test_name=test_name,
            number_of_questions=int(number_of_question),
            test_duration=duration,
            test_code=submitted_test_code,
            teacher_username=username,
            subject_name=subject_name
        )

        input_lines = file_content.split("\n")
        i = 0

        for _ in range(number_of_question):
            if i >= len(input_lines):
                break

            # Read question between question_open and question_clouse
            question_lines = []
            while i < len(input_lines):
                line = input_lines[i].strip()
                i += 1

                if line == "question_open":
            # Start capturing question
                    while i < len(input_lines) and input_lines[i].strip() != "question_closed":
                        question_lines.append(input_lines[i])
                        i += 1
                    i += 1  # Skip the 'question_clouse' line
                    break  # Done reading question

            question = "\n".join(question_lines).strip()

            # Skip empty lines
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

    context = {
        'class_list': class_list,
        'test_code': test_code
    }
    return render(request, 'file.html', context)





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
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        hashed_password = make_password(password)  # 🔒 Hash the password
        student = Teacher.objects.create(
            username=username,
            email=email,
            password=hashed_password,
        )

        # return HttpResponse("Student registered successfully!")
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

def export_results(request):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Student Results'

    # Define table headings
    headings = ['PRN', 'Student Name', 'Student Section', 'Subject Name', 'Marks', 'Time']
    worksheet.append(headings)

    # Fetch results (adjust filter if needed)
    username = request.session.get('username')
    subject_names = CreateClass.objects.filter(user_name=username).values_list('subject', flat=True)
    results = Result.objects.filter(subject_name__in=subject_names).order_by('-test_created_at')

    for result in results:
        worksheet.append([
            result.PRN,
            result.std_name,
            result.std_section,
            result.subject_name,
            result.marks,
            result.test_created_at.strftime('%d %b %Y ')
        ])

    # Prepare HTTP response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=student_results.xlsx'
    workbook.save(response)
    return response