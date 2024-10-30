from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index.html", views.index, name="index"),
    path("addtodo", views.addtodo, name="addtodo"),
    path("deletetodo/", views.deletetodo, name="deletetodo"),
    path("viewall/", views.viewall, name="viewall"),
    path('viewtodo/<int:todo_id>/', views.viewtodo, name='viewtodo'),
]