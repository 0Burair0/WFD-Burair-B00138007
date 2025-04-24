# urls for views like module, login, dashboards and uploads
# each route connects to a page or feature


from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('add-module/', views.add_module, name='add_module'),
    path('edit-module/<int:module_id>/', views.edit_module, name='edit_module'),
    path('delete-module/<int:module_id>/', views.delete_module, name='delete_module'),
    path('assign-trainer/', views.assign_trainer, name='assign_trainer'),
    path('trainer-modules/', views.trainer_modules, name='trainer_modules'),
    path('enroll-student/', views.enroll_student, name='enroll_student'),
    path('remove-student/', views.remove_student, name='remove_student'),
    path('update-notes/<int:module_id>/', views.update_notes, name='update_notes'),
    path('student-modules/', views.student_modules, name='student_modules'),
    path('self-enroll/', views.self_enroll, name='self_enroll'),
    path('browse-modules/', views.browse_modules, name='browse_modules'),
    path('module/<int:module_id>/', views.view_module_content, name='view_module'),
    path('redirect/', views.role_redirect, name='role_redirect'),  
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('trainer-module/<int:module_id>/', views.trainer_module_detail, name='trainer_module_detail'),
    path('trainer-module/<int:module_id>/', views.trainer_module_detail, name='trainer_view_module'),
    path('delete-file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('upload-file/<int:module_id>/<int:week>/', views.upload_file, name='upload_file'),
    path('student-module/<int:module_id>/', views.student_module_detail, name='student_module_detail'),



  
]
