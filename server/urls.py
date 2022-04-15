from django.urls import path
from .views import *
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('task/create/<int:pk>', task_create_view, name='taskcreate'),
    path('register', register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),  # авторизация
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),  # выйти
    path('application/create/<int:pk>', application_create, name='appl-create'),
    path('applications/accept/(P<student_id>\d+)/(P<course_id>\d+)/<int:pk>', application_accept, name='application_accept'),
    path('applications/list', applications_list, name='applicationslist'),
    path('my/courses/', my_courses, name='my_courses'),
    path('detail/<int:pk>', detail, name='detail'),
    path('task/detail/<int:pk>', task_detail, name='task_detail'),
    path('', courses_list, name='course/list'),
    path('user/edit/<int:pk>', user_edit, name='user_edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
