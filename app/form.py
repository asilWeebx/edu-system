from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.transaction import atomic
from app.models import *


class RegisterForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=55)
    role = forms.CharField(max_length=155)
    phone_number = forms.CharField(max_length=13)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    text = forms.CharField(max_length=2000)
    date_of_birth = forms.CharField(max_length=155)
    place_of_birth = forms.CharField(max_length=155)
    city = forms.CharField(max_length=100)
    photo = forms.ImageField()
    grade = forms.CharField(max_length=55)
    password = forms.CharField(max_length=155)
    confirm_password = forms.CharField(max_length=155)

    def clean_email(self):
        email = self.data.get('email')
        if CustomUser.objects.filter(email=email).first():
           raise ValidationError("Bu email bazada bor !")
        return email

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')

        if password != confirm_password:
            return ValidationError('Confirm password xato kiritildi !')

        return password

    @atomic
    def save(self):
        user = CustomUser.objects.create_user(email=self.cleaned_data.get('email'),
                                              username=self.cleaned_data.get('username'),
                                              role=self.cleaned_data.get('role'),
                                              phone_number=self.cleaned_data.get('phone_number'),
                                              first_name=self.cleaned_data.get('first_name'),
                                              last_name=self.cleaned_data.get('last_name'),
                                              text=self.cleaned_data.get('text'),
                                              date_of_birth=self.cleaned_data.get('date_of_birth'),
                                              place_of_birth=self.cleaned_data.get('place_of_birth'),
                                              city=self.cleaned_data.get('city'),
                                              photo=self.cleaned_data.get('photo'),
                                              )

        grade_name = self.cleaned_data.get('grade')
        try:
            grade = Grade.objects.get(name=grade_name)
        except Grade.DoesNotExist:
            # Handle the case where the grade doesn't exist
            raise ValidationError("The specified grade does not exist")

        # Assign the School instance to the user's grade field
        user.grade = grade

        user.set_password(raw_password=self.cleaned_data.get('password'))
        user.save()


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=False)
    email = forms.EmailField()
    password = forms.CharField(max_length=55)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class TeachersGradeForm(forms.ModelForm):
    class Meta:
        model = TeacherGrades
        fields = ['grade', 'teacher']

    def clean_grade(self):
        grade_name = self.cleaned_data['grade']
        try:
            grade = Grade.objects.get(name=grade_name)
        except Grade.DoesNotExist:
            raise ValidationError("The specified grade does not exist")
        return grade

    def clean_teacher(self):
        teacher_name = self.cleaned_data['teacher']
        try:
            teacher = CustomUser.objects.get(email=teacher_name)
        except CustomUser.DoesNotExist:
            raise ValidationError("The specified teacher does not exist")
        return teacher