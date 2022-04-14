from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    year = models.DateField(blank=True, null=True)
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False, blank=True)
    fakultet = models.ForeignKey('Fakultet', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.username


class Fakultet(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100)
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    lang = models.CharField(max_length=100)
    image = models.ImageField(upload_to='course/')

    def __str__(self):
        return self.title


class Kafedra(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    kafedra_id = models.ForeignKey(Kafedra, on_delete=models.CASCADE, blank=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'{self.user}'


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    task_id = models.ForeignKey('Task', on_delete=models.CASCADE)


class File(models.Model):
    file = models.FileField(upload_to='files/')
    task_id = models.ForeignKey('Task', on_delete=models.CASCADE)


class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=('Пользователь'),
        related_name='posts'
    )
    title = models.CharField(
        max_length=100,
    )
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    link_youtube = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['-date']


class CourseUser(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id}: {self.course_id}"

    class Meta:
        verbose_name = 'Курс студента'
        verbose_name_plural = 'Курсы студента'
        ordering = ['-date']
        unique_together = ['user_id', 'course_id']


class Application(models.Model):
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заявка студента {self.student_id.first_name + self.student_id.name} на курс {self.course}'

    class Meta:
        verbose_name = 'Заявка на курс'
        verbose_name_plural = 'Заявки на курс'
        ordering = ['-date']
        unique_together = ['student_id', 'course']
