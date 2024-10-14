from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.process_repayment, name='upload-repayment'),
    path('download-template/', views.download_template, name='download-template'),
]
