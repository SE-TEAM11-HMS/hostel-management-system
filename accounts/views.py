from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .forms import AdminLoginForm


@never_cache
def admin_login(request):
    # Already-authenticated administrators can go straight
    # to the dashboard.
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("accounts:dashboard")

    next_url = (
        request.POST.get("next")
        or request.GET.get("next", "")
    )

    form = AdminLoginForm(
        request=request,
        data=request.POST if request.method == "POST" else None,
    )

    if request.method == "POST" and form.is_valid():
        login(request, form.user)

        # Redirect to a safe requested URL, if provided.
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)

        return redirect("accounts:dashboard")

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
            "next": next_url,
        },
    )


@never_cache
@login_required
def dashboard(request):
    # Enforce administrator access on the server.
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "You do not have permission to access this page."
        )

    return render(
        request,
        "accounts/dashboard.html",
    )


@never_cache
@login_required
@require_POST
def admin_logout(request):
    logout(request)
    return redirect("accounts:login")