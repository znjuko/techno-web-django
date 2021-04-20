from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from .models import Question, Tag, User, Answer
from .forms import AuthForm, SignUpFrom, AddQuestionForm, AddAnswerForm, EditProfileForm
from django.contrib.auth.decorators import login_required


def get_tags_and_users():
    return Tag.objects.best_tags(), User.objects.best_users()


def paginate(objects_list, list_num, request):
    paginator = Paginator(objects_list, list_num)
    page = request.GET.get("page")

    contacts = paginator.get_page(page)

    return contacts


def index(request):
    if request.method == "POST":
        logout(request)

    q = paginate(Question.objects.get_question_by_date(), 10, request)
    tags, users = get_tags_and_users()
    return render(
        request,
        "questions/index.html",
        {"paginate": q, "tags": tags, "users": users},
    )


def question(request, id):
    try:
        q = Question.objects.get_question_by_id(id)
        if request.method == "POST":
            if not request.user.is_authenticated:
                return redirect("/login/")
            form = AddAnswerForm(
                request.POST, initial={"user": request.user, "question": q}
            )
            if form.is_valid():
                form.save()
                answers = paginate(
                    Answer.objects.get_answers_by_id(q.id), 4, request
                )
                return redirect(Answer.objects.get_absolute_url(q, answers))
        else:
            form = AddAnswerForm()
    except Question.DoesNotExist:
        return render(
            request,
            "404.html",
        )

    answers = paginate(Answer.objects.get_answers_by_id(q.id), 4, request)
    tags, users = get_tags_and_users()
    return render(
        request,
        "questions/question_page.html",
        {
            "form": form,
            "question": q,
            "tags": tags,
            "users": users,
            "paginate": answers,
        },
    )


def tag(request, tagname):
    try:
        questions = paginate(
            Question.objects.get_questions_by_tag(tagname), 10, request
        )
    except:
        return render(
            request,
            "404.html",
        )
    tags, users = get_tags_and_users()
    return render(
        request,
        "questions/question_tag.html",
        {"paginate": questions, "tag": tagname, "tags": tags, "users": users},
    )


def hot(request):
    q = paginate(Question.objects.get_question_by_popular(), 10, request)
    tags, users = get_tags_and_users()
    return render(
        request,
        "questions/index.html",
        {"paginate": q, "tags": tags, "users": users},
    )


def sign_in(request):
    if request.method == "POST":
        form = AuthForm(request.POST, initial={"request": request})
        if form.is_valid():
            return redirect("/")
        else:
            return render(request, "questions/auth.html", {"form": form})
    else:
        form = AuthForm()

    return render(request, "questions/auth.html", {"form": form})


def sign_up(request):
    if request.method == "POST":
        form = SignUpFrom(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
        else:
            return render(request, "questions/registration.html", {"form": form})
    else:
        form = SignUpFrom()

    return render(request, "questions/registration.html", {"form": form})


def sign_out(request):
    logout(request)
    return redirect("/")


@login_required(login_url="/login")
def profile(request, id):
    return render(request, "questions/profile.html", {})


@login_required(login_url="/login")
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(
            request.POST, request.FILES, initial={"user": request.user}
        )
        if form.is_valid():
            form.save()
            return redirect("/profile/edit")
        else:
            print(form.errors)
            return render(request, "questions/profile_edit.html", {"form": form})
    else:
        form = EditProfileForm()

    return render(request, "questions/profile_edit.html", {"form": form})


@login_required(login_url="/login")
def ask(request):
    if request.method == "POST":
        form = AddQuestionForm(request.POST, initial={"user": request.user})
        if form.is_valid():
            q = form.save()
            return redirect(Question.objects.get_absolute_url(q.id))

    else:
        form = AddQuestionForm()

    return render(request, "questions/question_form.html", {"form": form})


@login_required(login_url="/login")
def like_question(request):
    try:
        q = Question.objects.get_question_by_id(id)
        if request.method == "POST":
            form = AddQuestionForm(request.POST, initial={"user": request.user})
            if form.is_valid():
                q = form.save()
                return redirect(Question.objects.get_absolute_url(q.id))

        else:
            form = AddQuestionForm()

    except Question.DoesNotExist:
        return render(
            request,
            "404.html",
        )
