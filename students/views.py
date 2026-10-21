
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from .forms import StudentForm
from .models import Student


@login_required
def add_student(request):
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "You do not have permission to add students."
        )

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully.")
            return redirect("student_list")
    else:
        form = StudentForm()

    return render(
        request,
        "students/student_form.html",
        {"form": form},
    )


@login_required
def student_list(request):
    students = Student.objects.all().order_by("name")

    return render(
        request,
        "students/student_list.html",
        {"students": students},
    )
