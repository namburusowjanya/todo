from django.urls import path
from todoapp import views as v

urlpatterns=[
    path('',v.register,name='register'),
    path('login/',v.user_login,name='login'),
    path('logout/',v.user_logout,name='logout'),
    path('tasks/',v.task_list,name='task_list'),
    path('add/',v.add_task,name='add_task'),
    path('delete/<int:task_id>/',v.delete_task,name='delete_task')
]