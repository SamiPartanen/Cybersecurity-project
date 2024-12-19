from django.urls import path
from django.views.static import serve
from . import views
from django.conf import settings

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("question_details/", views.question_details, name="question_details"),
    path("malicious/", views.malicious_page, name="malicious"),
    path("deserialization_view/", views.deserialization_view, name="deserialization_view"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('trigger-error/', views.trigger_error, name='trigger_error'),
    path("sensitive_data/", views.sensitive_data, name="sensitive"),
    
]