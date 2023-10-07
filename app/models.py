from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class School(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Maktab"
        verbose_name_plural = "Maktab"


class Grade(models.Model):
    name = models.CharField(max_length=155)
    school = models.ForeignKey(to=School, on_delete=models.CASCADE, related_name='school')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sinf"
        verbose_name_plural = "Sinf"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        oquvchi = "O'quvchi"
        oqituvchi = "O'qituvchi"

    role = models.CharField(max_length=155, choices=Role.choices, default=Role.oquvchi)
    username = models.CharField(max_length=155, unique=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=13)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    text = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='teachers photo/', null=True, blank=True)
    date_of_birth = models.CharField(max_length=100)
    place_of_birth = models.CharField(max_length=155)
    grade = models.ForeignKey(to=Grade, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    city = models.CharField(max_length=155, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = "O'ituvchi va o'quvchilar"
        verbose_name_plural = "O'ituvchi va o'quvchilar"

    def __str__(self):
        return self.username


class TeacherGrades(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='teacher')

    def __str__(self):
        return self.grade.name


class Notifications(models.Model):
    text = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Attendance(models.Model):
    attendance = models.BooleanField(default=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.attendance


class Mark(models.Model):
    mark = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mark')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user
