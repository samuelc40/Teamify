from django.urls import path
from core.views import *


app_name = 'core'

urlpatterns = [
    path("", index, name='index'),
    path('task/<int:task_id>/', task_view, name='task'),
    path('new-task/', create_task, name='new-task')
    # path('signup/', register, name='signup'),
    # path('signin/', login, name='signin'),
]