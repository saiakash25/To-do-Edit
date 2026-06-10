from urllib import response

from django.contrib import messages

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from .forms import ContactForm, RegisterForm, TodoForm

from .models import Todo

# views.py
def is_manager(user):
    return user.groups.filter(
        name="Manager"
    ).exists()

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            # Save data, send email, etc.

            return redirect("register")  # URL name of registration page
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            print("Valid Form")

    else:
        form = RegisterForm()

    return render(request, "registration.html", {"form": form})


def todo_list(request):

    if request.user.groups.filter(
        name="Manager"
    ).exists():

        todos = request.user.created_todos.all()

    else:

        todos = request.user.assigned_todos.all()

    return render(
        request,
        "todo_list.html",
        {"todos": todos}
    )

@login_required
def create_todo(request):

    if not request.user.groups.filter(
        name="Manager"
    ).exists():

       messages.error(
        request,
        "You do not have permission to create tasks."
        )
       return redirect("todo-list")

        

    if request.method == "POST":

        form = TodoForm(request.POST)

        if form.is_valid():

            todo = form.save(commit=False)

            todo.created_by = request.user

            todo.save()

            response = render(
                request,
                "todo_row.html",
                {
                    "todo": todo
                }
            )
            response["HX-Trigger"] = "todo-created"
            response["HX-Trigger"] = "todoCreated"

            return response

    else:

        form = TodoForm()

    return render(
    request,
    "todo_create_form.html",
    {
        "form": form
    }
    )

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

def edit_todo(request, id):

    todo = get_object_or_404(
        Todo,
        pk=id
    )

    if (
    todo.assigned_to != request.user
    and
    todo.created_by != request.user
    ):

        return HttpResponseForbidden(
            "Access Denied"
        )

    if request.method == "POST":

        form = TodoForm(
            request.POST,
            instance=todo
        )

        if form.is_valid():

            todo = form.save()

            can_view = (
                todo.assigned_to == request.user
                or
                todo.created_by == request.user
            )

            if not can_view:
                return HttpResponse("")

            return render(
                request,
                "todo_row.html",
                {
                    "todo": todo
                }
            )

    else:

        form = TodoForm(
            instance=todo
        )

    

    return render(
        request,
        "todo_edit_form.html",
        {
            "todo": todo,
            "form": form,
        }
    )

@login_required
def search_todos(request):

    q = request.GET.get("q", "")

    todos = Todo.objects.filter(
        title__icontains=q
    )

    return render(
        request,
        "todo_list_partial.html",
        {
            "todos": todos
        }
    )
#akash
@login_required
def complete_todo(request, id):

    todo = get_object_or_404(
        Todo,
        pk=id
    )

    if todo.assigned_to != request.user:

        return HttpResponseForbidden()

    todo.completed = True

    todo.save()

    return render(
        request,
        "todo_row.html",
        {"todo": todo}
    )

@login_required
def delete_todo(request, id):

    todo = get_object_or_404(
        Todo,
        pk=id
    )

    if (
        todo.assigned_to != request.user
        and
        todo.created_by != request.user
    ):
        return HttpResponseForbidden()

    todo.delete()

    return HttpResponse("")

@login_required
def todo_list_partial(request):

    if request.user.groups.filter(
        name="Manager"
    ).exists():

        todos = request.user.created_todos.all()

    else:

        todos = request.user.assigned_todos.all()

    return render(
        request,
        "todo_list_partial.html",
        {
            "todos": todos
        }
    )