
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .forms import AdminLoginForm, StudentLoginForm
from students.models import Student


def get_logged_in_student(user):
    """
    Return the Student record linked to the authenticated user.

    A student must be non-staff and have an associated Student record.
    """
    if not user.is_authenticated or user.is_staff:
        return None

    try:
        return user.student
    except Student.DoesNotExist:
        return None


def get_safe_next_url(request):
    """
    Return the next URL only if it is safe for this host.
    """
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url

    return None


@never_cache
def admin_login(request):
    next_url = get_safe_next_url(request)

    # Already authenticated administrators can continue to their
    # originally requested protected page.
    if request.user.is_authenticated and request.user.is_staff:
        return redirect(next_url or "accounts:dashboard")

    form = AdminLoginForm(
        request=request,
        data=request.POST if request.method == "POST" else None,
    )

    if request.method == "POST" and form.is_valid():
        login(request, form.user)
        return redirect(next_url or "accounts:dashboard")

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
            "next": next_url or "",
        },
    )


@never_cache
def student_login(request):
    # Do not allow administrators to enter through student login.
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("accounts:dashboard")

        student = get_logged_in_student(request.user)

        if student is not None:
            return redirect("accounts:student_portal")

        return HttpResponseForbidden(
            "Your account is not associated with a student record."
        )

    form = StudentLoginForm(
        request=request,
        data=request.POST if request.method == "POST" else None,
    )

    if request.method == "POST" and form.is_valid():
        login(request, form.user)
        return redirect("accounts:student_portal")

    return render(
        request,
        "accounts/student_login.html",
        {"form": form},
    )


@never_cache
@login_required(login_url="accounts:student_login")
def student_portal(request):
    # Retrieve the Student record from the current session.
    student = get_logged_in_student(request.user)

    if student is None:
        return HttpResponseForbidden(
            "You do not have permission to access the student portal."
        )

    return render(
        request,
        "accounts/student_portal.html",
        {"student": student},
    )


@never_cache
@login_required
def dashboard(request):
    # Only administrators may access the admin dashboard.
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "You do not have permission to access this page."
        )

    students = Student.objects.all().order_by("-pk")

    context = {
        "total_students": Student.objects.count(),
        "department_count": (
            Student.objects.values("department").distinct().count()
        ),
        "academic_year_count": (
            Student.objects.values("academic_year").distinct().count()
        ),
        "recent_students": students[:5],
    }

    return render(
        request,
        "accounts/dashboard.html",
        context,
    )


@never_cache
@login_required
@require_POST
def admin_logout(request):
    logout(request)
    return redirect("accounts:login")


@never_cache
@login_required
@require_POST
def student_logout(request):
    # Only linked student accounts may use student logout.
    if get_logged_in_student(request.user) is None:
        return HttpResponseForbidden(
            "You do not have permission to use student logout."
        )

    logout(request)
    return redirect("accounts:student_login")
