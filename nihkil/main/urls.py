from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<int:report_id>/', views.delete_report, name='delete_report'),
]

