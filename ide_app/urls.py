from django.urls import path
from ide_app.views import (
    index, register_user, 
    profile, code_ide, create_project, 
    project_detail, file_detail,
    create_file,
    login_user, logout_user,
    delete_project,
    update_code,
    about_us,
)
urlpatterns = [
    path('', index, name = 'home'),
    path('register/', register_user, name = 'register_user'),
    path('login/', login_user, name = 'login_user'),
    path('logout/', logout_user, name = 'logout_user'),
    path('profile/', profile, name = 'profile_page'),
    path('create_project/', create_project, name = 'create_project'),
    path('project/<int:project_id>/create_file/', create_file, name='create_file'),
    path('delete_project/<int:project_id>/', delete_project, name = 'delete_project'),
    path('project_detail/<int:project_id>/', project_detail, name = 'project_detail'),
    path('file_detail/<int:file_id>/', file_detail, name = 'file_detail'),
    path('ide/', code_ide, name = 'ide'),
    path('update/<int:code_id>/', update_code, name = 'update_code'),
    path('about/',about_us,name='about'),
]
