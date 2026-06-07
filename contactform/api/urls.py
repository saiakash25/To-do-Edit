from django.urls import path, include

from .views import complete_todo, contact_view, create_todo, delete_todo, edit_todo, register_view, search_todos, todo_list, todo_list_partial

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
    ),

    path(
    "delete/<int:id>/",
    delete_todo,
    name="delete-todo"
    ),

    path(
    "todos/partial/",
    todo_list_partial,
    name="todo-list-partial"
),
    path(
    "search-todos/",
    search_todos,
    name="search-todos"
)


]