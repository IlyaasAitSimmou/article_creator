from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    # path("articles/", views.articles, name="articles"),
    # path("articles/<int:article_id>/", views.article, name="article"),
    # path("articles/new/", views.new_article, name="new_article"),
    # path("articles/<int:article_id>/edit/", views.edit_article, name="edit_article"),
    # path("articles/<int:article_id>/delete/", views.delete_article, name="delete_article"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("forgot_password/", views.forgot_password_view, name="forgot_password"),
    path("password_reset/<str:access_code>/", views.password_reset_view, name="password_reset"),
    # path("articles/", views.articles, name="articles"),
    path("verify_email/<str:VerificationCode>/", views.verify_email, name="verify_email"),

    path("create_aritcle/", views.create_article, name="create_article"),
    path("edit_article/<str:article_name>/", views.edit_article, name="edit_article"),
    path("delete_article/<str:article_name>/", views.delete_article, name="delete_article"),

    path("create_project/", views.create_project, name="create_project"),
    path("edit_project/<str:project_name>/", views.edit_project, name="edit_project"),
    path("delete_project/<str:project_name>/", views.delete_project, name="delete_project"),

    path("view_article/<str:article_name>/", views.view_article, name="view_article"),
    path("project/<str:project_name>", views.view_project, name="project"),
    path('password_confirmation/', views.password_confirmation_view, name='password_confirmation'),
    path('settings', views.account_settings_view, name='account_settings'),
    
    path('api/fetch-articles/', views.fetch_articles, name='fetch_articles'),
    path('api/fetch-project-articles/', views.fetch_project_articles, name='fetch_projects_articles'),
    path('api/fetch-article/', views.fetch_view_article, name='fetch_article'),

]
