from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def task_create_view(request, pk):
    if request.user.is_teacher == True or request.user.is_superuser:
        if request.method == 'POST':
            form_task = TaskCreateForm(request.POST)

            if form_task.is_valid():
                das = form_task.save(commit=False)
                if das.link_youtube:
                    das.link_youtube = 'https://www.youtube.com/embed/' + das.link_youtube.split('=')[-1]

                das.user = request.user
                das.course_id_id = pk
                das.save()
                files = request.FILES.getlist('files')
                for i in files:
                    if str(i).split('.')[-1].lower() in 'pngjpegimgjpg':
                        qwe = Image(image=i, task_id=das)
                        qwe.save()
                    else:
                        qwe = File(file=i, task_id=das)
                        qwe.save()
                messages.success(request, "Yeeew, check it out on the home page!")
                return redirect('/')
            else:
                print(form_task.errors)

        task_form = TaskCreateForm()
        image_form = ImageCreateForm()
        file_form = FileCreateForm()
        return render(request, 'taskcreate.html', {'taskform': task_form, 'imageform': image_form, 'fileform': file_form})
    return HttpResponse('Error')


def register(request):  # функция регистрации
    print('da')
    if request.method == 'POST':  # Проверка запроса на пост
        form = UserRegisterForm(request.POST)  # присваиваем форму для данных
        print('POST')
        if form.is_valid():  # Проверка на валидность
            form.save()  # Сохранение в базу
            print('VAlid')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)  # авторизация юзера
            print('hz')
            login(request, user)  # авторизация юзера
            return redirect('/')  # переадресация на главную страничку
        else:
            print(form.errors)
    else:  # если это запрос не пост
        form = UserRegisterForm()  # Присваивание форму

    context = {'form': form}  # контекст для передачи данных для шаблона
    return render(request, 'register.html', context)


@login_required(login_url='login')
def application_create(request, pk):
    print('da')
    das = Application(student_id=request.user, course_id=pk)
    das.save()
    print('das')
    return redirect('/')


def applications_list(request):
    applications_list = Application.objects.all()
    return render(request, 'applicationslist.html', context={'applications_list': applications_list})


@login_required(login_url='login')
def application_accept(request, student_id, course_id, pk):
    print(student_id, course_id)
    das = CourseUser(user_id_id=student_id, course_id_id=course_id)
    das.save()
    Application.objects.get(pk=pk).delete()
    print(das)
    return redirect('/')


def courses_list(request):
    courselist = Course.objects.all()
    return render(request, 'courselist.html', {'courselist': courselist})


def my_courses(request):
    courses = CourseUser.objects.filter(user_id=request.user)
    print(courses)
    user_courses = []
    # for i in courses:
    #     user_courses.append(Course.objects.get(id=i))
    # print(my_courses)
    return render(request, 'my_courses.html', {'my_courses': [course.course_id for course in courses]})
    # return HttpResponse()


def detail(request, pk):
    course = Course.objects.get(id=pk)
    tasks = Task.objects.filter(course_id=pk)
    mycourses = 1
    in_course = False
    if str(request.user) != 'AnonymousUser':
        mycourses = CourseUser.objects.filter(course_id=pk, user_id=request.user)
        in_course = mycourses.exists()

    print(mycourses)
    print(in_course)
    return render(request, 'detail.html', {'course': course, 'tasks': tasks, 'in_course': in_course})


@login_required()
def task_detail(request, pk):
    task = Task.objects.get(id=pk)
    files = File.objects.filter(task_id=pk)
    images = Image.objects.filter(task_id=pk)
    return render(request, 'task_detail.html', {'task': task, 'files': files, 'images': images})


def index(request):
    return render(request, 'index.html')


@login_required()
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserRegisterForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserRegisterForm(instance=user)
    return render(request, 'register.html', {'form': form})