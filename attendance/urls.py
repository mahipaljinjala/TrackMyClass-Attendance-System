from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('view/', views.view_attendance, name='view_attendance'),
    path('search/', views.search_attendance, name='search_attendance'),  # ✅ Search page
    path('export/', views.export_attendance_excel, name='export_attendance'),
    path('delete/<int:record_id>/', views.delete_attendance, name='delete_attendance'),
]
