from django.urls import path, re_path
from . import views

urlpatterns = [
    path('tasks/', views.task_proxy),
    # re_path(r'^tasks/(?P<path>\d+)/$', views.task_proxy),
    path('tasks/<int:task_id>/', views.task_proxy),
]