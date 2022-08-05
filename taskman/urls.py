from django.urls import path
from .views import LoginView, TaskDetail, TaskUpdate, TaskCreate, TaskList, TaskDelete, register, ListTask, DeleteTask, ActivityFeed
from django.contrib.auth.views import LogoutView
from taskman import views

urlpatterns= [
    path('login/',LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/', register, name='register'),
    path('tasks/', ListTask.as_view()),
    path('tasks/<int:pk>/',DeleteTask.as_view()),
    path('',TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/',TaskDetail.as_view(), name='task'),
    path('activityfeed/', views.activityFeeds,name='activity-feed'),
    path('search/',views.search, name='search'),
    path('task-create/',TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/',TaskDelete.as_view(), name='task-delete'),
]