from django import forms
from django.contrib.auth import authenticate, login
from .models import User, Question, Answer


class AuthForm(forms.Form):
    login = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        user = authenticate(
            self.initial["request"],
            username=self.cleaned_data["login"],
            password=self.cleaned_data["password"],
        )
        if user is None:
            raise forms.ValidationError("Login/Password are incorrect")

        login(self.initial["request"], user)


class SignUpFrom(forms.Form):
    login = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    nickname = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    photo = forms.ImageField(initial="uploads/default_image.jpg", required=False)

    def clean(self):
        if self.cleaned_data["password"] != self.cleaned_data["password_confirmation"]:
            raise forms.ValidationError("Password are not same")

        return self.cleaned_data

    def clean_login(self):
        login = self.cleaned_data["login"]
        if User.objects.filter(username=login).exists():
            raise forms.ValidationError("User with such login already exist")

        return login

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with such email already exist")

        return email

    def save(self):
        user = User.objects.create_user(
            login=self.cleaned_data["login"],
            email=self.cleaned_data["email"],
            nickname=self.cleaned_data["nickname"],
            password=self.cleaned_data["password"],
            photo=self.cleaned_data["photo"],
        )
        return user


class EditProfileForm(forms.Form):
    email = forms.EmailField(max_length=100, required=False)
    nickname = forms.CharField(max_length=100, required=False)
    photo = forms.ImageField(required=False)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with such email already exist")

        return email

    def save(self):
        user = self.initial["user"]
        usr = User.objects.edit_user(
            user=user,
            email=self.cleaned_data["email"],
            nickname=self.cleaned_data["nickname"],
            photo=self.cleaned_data["photo"],
        )
        return usr


class AddQuestionForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(max_length=100)

    def save(self):
        user = self.initial["user"]
        question = Question.objects.create_question(
            user,
            self.cleaned_data["title"],
            self.cleaned_data["text"],
            self.cleaned_data["tags"],
        )

        return question


class AddAnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

    def save(self):
        user = self.initial["user"]
        question = self.initial["question"]

        answer = Answer.objects.create_answer(user, question, self.cleaned_data["text"])

        return answer
