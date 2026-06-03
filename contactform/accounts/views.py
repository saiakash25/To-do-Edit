
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .forms import RegisterForm
from django.http import HttpResponse

def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            employee_group = Group.objects.get(
                name="Employee"
            )

            user.groups.add(
                employee_group
            )
            

            return HttpResponse("User Created")
            #return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )

@login_required
def dashboard(request):

    return render(
        request,
        "accounts/dashboard.html"
    )