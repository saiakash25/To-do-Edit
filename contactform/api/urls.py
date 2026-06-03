from django.urls import path, include

from .views import complete_todo, contact_view, create_todo, edit_todo, register_view, todo_list

urlpatterns = [
    path("", contact_view, name="contact"),
    #path("register/", register_view, name="register"),
    path("todos/", todo_list, name="todo-list"),

    path(
        "create-todo/",
        create_todo,
        name="create-todo"
    ),
    path(
        "edit-todo/<int:id>/",
        edit_todo,
        name="edit-todo"
    ),

    path(
    "complete/<int:id>/",
    complete_todo,
    name="complete-todo"
    )
]