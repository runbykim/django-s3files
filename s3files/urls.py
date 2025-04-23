from django.urls import path
from . import views

urlpatterns = [
    path('browse', views.list_s3_files, name='s3_files'),
    path('delete/<path:delete_path>', views.delete_file, name='delete_s3_file'),
]