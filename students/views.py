
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from .forms import StudentForm


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
            return redirect("student_add")
    else:
        form = StudentForm()

    return render(request, "students/student_form.html", {"form": form})
