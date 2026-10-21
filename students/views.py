
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import StudentForm
from .models import Student


@login_required
def add_student(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to add students.")

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully.")
            return redirect("student_list")
    else:
        form = StudentForm()

    return render(request, "students/student_form.html", {"form": form})


@login_required
def student_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to view students.")

    query = request.GET.get("q", "").strip()
    students = Student.objects.all().order_by("name")

    if query:
        students = students.filter(
            Q(usn__icontains=query)
            | Q(name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
            | Q(department__icontains=query)
        )

    return render(request, "students/student_list.html", {"students": students, "query": query})


@login_required
def student_detail(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to view student details.")

    student = get_object_or_404(Student, pk=pk)

    return render(request, "students/student_detail.html", {"student": student})


@login_required
def student_update(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to update students.")

    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully.")
            return redirect("student_detail", pk=student.pk)
    else:
        form = StudentForm(instance=student)

    return render(request, "students/student_update.html", {"form": form, "student": student})


@login_required
def student_confirm_delete(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to delete students.")

    student = get_object_or_404(Student, pk=pk)

    return render(request, "students/student_confirm_delete.html", {"student": student})


@login_required
@require_POST
def student_delete(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to delete students.")

    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.success(request, "Student deleted successfully.")

    return redirect("student_list")
