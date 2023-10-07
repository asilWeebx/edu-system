from datetime import date
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from app.form import LoginForm, RegisterForm
from app.models import CustomUser, Grade, Notifications, Attendance, Mark, TeacherGrades


def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        first_name = request.user.first_name
        last_name = request.user.last_name
        users = CustomUser.objects.all().count()
        user = request.user
        teacher = CustomUser.objects.filter(role="O'qituvchi")
        student = CustomUser.objects.filter(role="O'quvchi")
        mark_5 = Mark.objects.filter(mark=5).count()
        mark_4 = Mark.objects.filter(mark=4).count()
        mark_3 = Mark.objects.filter(mark=3).count()
        mark_2 = Mark.objects.filter(mark=2).count()
        notifications = Notifications.objects.all().order_by('-id')[:3]
        return render(request, 'index.html', {'username': username, 'first_name': first_name, 'last_name': last_name,
                                              "teacher": teacher, "student": student, 'users': users, 'user': user,
                                              'mark_5': mark_5, 'mark_4': mark_4, 'mark_3': mark_3, 'mark_2': mark_2,
                                              'notifications': notifications})

    else:
        return redirect('student-login')


def notifications(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        user = request.user
        n = Notifications()
        n.text = text
        n.user = user
        n.save()

    user = request.user
    notification = Notifications.objects.all().order_by('-id')
    return render(request, 'notification.html', {'user': user, 'notifications': notification})


def teacher_details(request):
    if request.user.role == "O'quvchi":
        detail = CustomUser.objects.filter(grade_id=request.user.grade_id).first()
        return render(request, 'teacher-details.html', {'detail': detail})
    elif request.user.role == "O'qituvchi":
        return redirect('index')


def students(request):
    if request.user.role == "O'qituvchi":
        user = request.user
        users = CustomUser.objects.all()
        classes = TeacherGrades.objects.filter(teacher_id=request.user.id)
        filter_class = TeacherGrades.objects.filter(teacher_id=request.user.id)
        students = CustomUser.objects.filter(role="O'quvchi",
                                             grade__teachergrades__teacher_id=request.user.id).order_by('grade__name')
        return render(request, 'students.html', {'classes': classes, 'users': users, 'students': students,
                                                 'user': user, 'filter_class': filter_class})

    else:
        students = CustomUser.objects.filter(grade_id=request.user.grade_id, role="O'quvchi")

        return render(request, 'students.html', {'students': students})


def filter_class(request, id):
    if request.user.role == "O'qituvchi":
        user = request.user
        users = CustomUser.objects.all()
        students = CustomUser.objects.filter(role="O'quvchi",
                                             grade_id=id).order_by('grade__name')
        return render(request, 'filter_class.html', {'users': users, 'students': students,
                                                     'user': user, 'filter_class': filter_class})

    else:
        students = CustomUser.objects.filter(grade_id=request.user.grade_id, role="O'quvchi")

        return render(request, 'filter_class.html', {'students': students})


def user(request):
    detail = request.user
    return render(request, 'user.html', {'detail': detail})


def chat(request):
    return render(request, 'chat.html')


def loginPage(request):
    if request.method == 'POST':
        form = LoginForm(request=request,
                         data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(user=user,
                  request=request)
            return redirect('index')
        else:
            messages.error(request, "Email yoki parol xato!")
            return redirect('student-login')

    form = LoginForm()
    context = {'form': form}

    return render(request, 'auth/student_login.html', context)


def TeacherLoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "CustomUsername yoki parol xato!")

    return render(request, 'auth/teacher_login.html')


def registerPage(request):
    if request.user.role == "O'qituvchi":
        user = request.user
        if request.method == "POST":
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('index')
        form = RegisterForm()

        grade = Grade.objects.all()

        if user.is_superuser:
            role = CustomUser.Role
        else:
            role = CustomUser.Role.oquvchi

        context = {'grade': grade,
                   'role': role,
                   'form': form,
                   'user': user}

        return render(request, 'add_user.html', context)

    else:
        return redirect('index')


def base(request):
    owner = request.user
    context = {
        'user': owner
    }
    return render(context)


def student_details(request, id):
    mark_5 = Mark.objects.filter(mark=5, user_id=id).count()
    mark_4 = Mark.objects.filter(mark=4, user_id=id).count()
    mark_3 = Mark.objects.filter(mark=3, user_id=id).count()
    mark_2 = Mark.objects.filter(mark=2, user_id=id).count()
    marks = Mark.objects.all().filter(user_id=id).order_by('-id')
    teacher_role = request.user.role == "O'qituvchi"
    if request.method == "POST":
        attendance = request.POST.get('attendance')
        mark = request.POST.get('mark')
        user = CustomUser.objects.filter(role="O'quvchi", id=id).first()
        if attendance:

            if attendance == 'on':
                attendance = True
            else:
                attendance = False

                # Create an Attendance object and save it to the database
            a = Attendance(attendance=attendance, user=user)
            a.save()
            return redirect('students')
        elif mark:

            m = Mark(mark=mark, user=user)
            m.save()
            return redirect('students')

    user = request.user
    detail = CustomUser.objects.filter(id=id).first()
    return render(request, 'student-details.html', {'detail': detail, 'user': user, 'marks': marks,
                                                    'mark_5': mark_5, 'mark_4': mark_4,
                                                    'mark_3': mark_3, 'mark_2': mark_2, 'taecher_role': teacher_role})


def marksheet(request):
    if request.user.role == "O'quvchi":
        data = date.today()
        students = Mark.objects.filter(user__grade_id=request.user.grade_id, user__role="O'quvchi", date=data).order_by('-id')
        return render(request, 'marksheet.html', {'students': students})
    else:
        return redirect('index')


def teachers_grade(request):
    if request.user.is_superuser:
        grades = Grade.objects.all()
        teachers = CustomUser.objects.filter(role="O'qituvchi")

        if request.method == "POST":
            grade = request.POST.get('grade')
            teacher = request.POST.get('teacher')
            grade_name = Grade.objects.get(name=grade)
            teacher_name = CustomUser.objects.get(username=teacher)
            t = TeacherGrades(grade=grade_name, teacher=teacher_name)
            t.save()
            return redirect('index')

        context = {
            'grades': grades,
            'teachers': teachers,
        }

        return render(request, 'teachers_grade.html', context)

    else:
        return redirect('index')


def test(request):
    classes = TeacherGrades.objects.filter(teacher_id=request.user.id)
    return render(request, 'test.html', {'classes': classes})
