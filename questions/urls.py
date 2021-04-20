from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("question/<int:id>/", views.question, name="question"),
    path("tag/<tagname>/", views.tag, name="tag"),
    path("hot/", views.hot, name="hot"),
    path("login/", views.sign_in, name="signIn"),
    path("signup/", views.sign_up, name="signUp"),
    path("ask/", views.ask, name="ask"),
    path("signout/", views.sign_out, name="signOut"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("profile/edit", views.edit_profile, name="editProfile"),
    # path("question/<int:id>/like", views.like_question, name="likeQuestion")
]
