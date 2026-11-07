import hashlib
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import redirect_to_login
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Prefetch, Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .forms import ContactForm, ProjectForm, StaffAuthenticationForm
from .models import BusinessFront, Project, Service, SiteContent


THEMES = {
    "golden-hour": {
        "key": "golden",
        "slug": "golden-hour",
        "label": "Golden Hour",
        "short_label": "Escuro",
        "theme_color": "#13171B",
    },
    "solar-editorial": {
        "key": "solar",
        "slug": "solar-editorial",
        "label": "Solar Editorial",
        "short_label": "Claro",
        "theme_color": "#FFF6E0",
    },
}
THEMES_BY_KEY = {theme["key"]: theme for theme in THEMES.values()}


def _resolve_theme(request, theme_slug=None):
    query_theme = request.GET.get("tema")
    explicit_value = theme_slug or query_theme

    if theme_slug:
        theme = THEMES.get(theme_slug)
        if not theme:
            raise Http404("Tema não encontrado.")
        return theme, True

    if query_theme:
        theme = THEMES.get(query_theme) or THEMES_BY_KEY.get(query_theme)
        if theme:
            return theme, True

    cookie_theme = request.COOKIES.get("prisma_theme")
    return THEMES_BY_KEY.get(cookie_theme, THEMES["golden-hour"]), False


def _contact_rate_limited(request):
    """Limite simples por IP anonimizado; a borda deve ser a primeira defesa."""
    remote_address = request.META.get("REMOTE_ADDR", "unknown")
    address_hash = hashlib.sha256(remote_address.encode("utf-8")).hexdigest()[:24]
    key = f"prisma:contact-rate:{address_hash}"
    limit = settings.CONTACT_RATE_LIMIT
    window = settings.CONTACT_RATE_WINDOW

    if cache.add(key, 1, timeout=window):
        return False
    try:
        attempts = cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=window)
        return False
    return attempts > limit


def _base_context(request, theme_slug=None):
    selected_theme, theme_explicit = _resolve_theme(request, theme_slug)
    return {
        "selected_theme": selected_theme,
        "theme_explicit": theme_explicit,
        "themes": THEMES.values(),
        "site_content": SiteContent.load(),
        "nav_fronts": BusinessFront.objects.filter(is_active=True).order_by(
            "sort_order", "title"
        ),
        "canonical_url": request.build_absolute_uri(request.path),
    }


def _set_theme_cookie(response, context):
    if context["theme_explicit"]:
        response.set_cookie(
            "prisma_theme",
            context["selected_theme"]["key"],
            max_age=60 * 60 * 24 * 365,
            samesite="Lax",
        )
    return response


def _has_panel_permission(user, permission):
    return bool(
        user.is_authenticated
        and user.is_active
        and user.is_staff
        and (user.is_superuser or user.has_perm(permission))
    )


def _panel_permission_required(permission):
    """Exige autenticação interna e uma permissão editorial específica."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(
                    request.get_full_path(),
                    reverse("portfolio:panel_login"),
                )
            if not _has_panel_permission(request.user, permission):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator


def _safe_panel_next_url(request):
    candidate = request.POST.get("next") or request.GET.get("next")
    if candidate and url_has_allowed_host_and_scheme(
        candidate,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return candidate
    return reverse("portfolio:panel_dashboard")


def home(request, theme_slug=None):
    context = _base_context(request, theme_slug)
    selected_theme = context["selected_theme"]
    published_projects = Project.objects.filter(
        status=Project.Status.PUBLISHED,
        front__is_active=True,
    ).select_related("front")
    fronts = BusinessFront.objects.filter(is_active=True).order_by(
        "sort_order", "title"
    ).prefetch_related(
        Prefetch(
            "services",
            queryset=Service.objects.filter(is_active=True).order_by(
                "sort_order", "title"
            ),
        ),
        Prefetch("projects", queryset=published_projects),
    )

    rate_limited = request.method == "POST" and _contact_rate_limited(request)
    response_status = 200

    if rate_limited:
        form = ContactForm()
        response_status = 429
        messages.error(
            request,
            "Muitas tentativas de envio. Aguarde alguns minutos antes de tentar novamente.",
        )
    elif request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.source_theme = selected_theme["key"]
            contact.save()
            messages.success(
                request,
                "Mensagem recebida. Obrigado pelo contato — retornaremos pelos dados informados.",
            )
            target = (
                reverse("portfolio:theme", kwargs={"theme_slug": selected_theme["slug"]})
                if theme_slug
                else reverse("portfolio:home")
            )
            return redirect(f"{target}#contato")
        messages.error(request, "Revise os campos destacados e tente novamente.")
    else:
        form = ContactForm()

    context.update(
        {
            "fronts": fronts,
            "projects": published_projects,
            "contact_form": form,
            "page_kind": "home",
        }
    )
    response = render(request, "portfolio/home.html", context, status=response_status)
    return _set_theme_cookie(response, context)


def front_detail(request, slug):
    published_projects = Project.objects.filter(
        status=Project.Status.PUBLISHED
    ).select_related("front")
    front = get_object_or_404(
        BusinessFront.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                "services",
                queryset=Service.objects.filter(is_active=True).order_by(
                    "sort_order", "title"
                ),
            ),
            Prefetch("projects", queryset=published_projects),
        ),
        slug=slug,
    )
    context = _base_context(request)
    context.update(
        {
            "front": front,
            "other_front": BusinessFront.objects.filter(is_active=True)
            .exclude(pk=front.pk)
            .order_by("sort_order", "title")
            .first(),
            "projects": front.projects.all(),
            "page_kind": "front",
            "active_front_slug": front.slug,
        }
    )
    response = render(request, "portfolio/front_detail.html", context)
    return _set_theme_cookie(response, context)


def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.select_related("front"),
        slug=slug,
        status=Project.Status.PUBLISHED,
        front__is_active=True,
    )
    context = _base_context(request)
    context.update(
        {
            "project": project,
            "page_kind": "project",
            "active_front_slug": project.front.slug,
        }
    )
    response = render(request, "portfolio/project_detail.html", context)
    return _set_theme_cookie(response, context)


@never_cache
def panel_login(request):
    if request.user.is_authenticated and request.user.is_active and request.user.is_staff:
        return redirect(_safe_panel_next_url(request))

    if request.method == "POST":
        form = StaffAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, "Acesso realizado. Bem-vindo ao painel da Prisma.")
            return redirect(_safe_panel_next_url(request))
    else:
        form = StaffAuthenticationForm(request=request)

    context = _base_context(request)
    context.update(
        {
            "form": form,
            "next": request.POST.get("next") or request.GET.get("next", ""),
            "page_kind": "panel",
            "panel_page": "login",
            "page_title": "Entrar no painel",
        }
    )
    response = render(request, "portfolio/panel/login.html", context)
    return _set_theme_cookie(response, context)


@never_cache
@require_POST
def panel_logout(request):
    auth_logout(request)
    messages.success(request, "Sua sessão no painel foi encerrada.")
    return redirect("portfolio:panel_login")


@never_cache
@_panel_permission_required("portfolio.view_project")
def panel_dashboard(request):
    projects = Project.objects.select_related("front")
    q = request.GET.get("q", "").strip()
    front_filter = request.GET.get("front", "").strip()
    requested_status = request.GET.get("status", "").strip()
    valid_statuses = {value for value, _label in Project.Status.choices}
    status_filter = requested_status if requested_status in valid_statuses else ""

    if q:
        projects = projects.filter(
            Q(title__icontains=q)
            | Q(category__icontains=q)
            | Q(summary__icontains=q)
            | Q(challenge__icontains=q)
            | Q(solution__icontains=q)
            | Q(deliverables__icontains=q)
            | Q(front__title__icontains=q)
        )
    if front_filter:
        projects = projects.filter(front__slug=front_filter)
    if status_filter:
        projects = projects.filter(status=status_filter)
    projects = projects.order_by("sort_order", "-featured", "-updated_at")

    status_counts = Project.objects.aggregate(
        total=Count("pk"),
        draft=Count("pk", filter=Q(status=Project.Status.DRAFT)),
        published=Count("pk", filter=Q(status=Project.Status.PUBLISHED)),
    )
    front_counts = BusinessFront.objects.annotate(
        total_cases=Count("projects", distinct=True),
        draft_cases=Count(
            "projects",
            filter=Q(projects__status=Project.Status.DRAFT),
            distinct=True,
        ),
        published_cases=Count(
            "projects",
            filter=Q(projects__status=Project.Status.PUBLISHED),
            distinct=True,
        ),
    ).order_by("sort_order", "title")
    front_totals = {front.slug: front.total_cases for front in front_counts}
    counts = {
        **status_counts,
        "marketing": front_totals.get(BusinessFront.Slug.MARKETING, 0),
        "technology": front_totals.get(BusinessFront.Slug.TECHNOLOGY, 0),
    }

    context = _base_context(request)
    context.update(
        {
            "projects": projects,
            "fronts": front_counts,
            "front_counts": front_counts,
            "status_counts": status_counts,
            "status_choices": Project.Status.choices,
            "counts": counts,
            "front_options": front_counts,
            "status_options": Project.Status.choices,
            "filters": {
                "q": q,
                "front": front_filter,
                "status": status_filter,
            },
            "can_add_project": _has_panel_permission(
                request.user, "portfolio.add_project"
            ),
            "can_change_project": _has_panel_permission(
                request.user, "portfolio.change_project"
            ),
            "page_kind": "panel",
            "panel_page": "dashboard",
            "page_title": "Painel de cases",
        }
    )
    response = render(request, "portfolio/panel/dashboard.html", context)
    return _set_theme_cookie(response, context)


@never_cache
@_panel_permission_required("portfolio.add_project")
def panel_project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            messages.success(
                request,
                f'O case “{project.title}” foi criado com sucesso.',
            )
            return redirect("portfolio:panel_dashboard")
        messages.error(request, "Revise os campos destacados antes de salvar o case.")
    else:
        form = ProjectForm()

    context = _base_context(request)
    context.update(
        {
            "form": form,
            "project": None,
            "is_editing": False,
            "is_create": True,
            "form_mode": "create",
            "cancel_url": reverse("portfolio:panel_dashboard"),
            "page_kind": "panel",
            "panel_page": "project_form",
            "page_title": "Novo case",
        }
    )
    response = render(request, "portfolio/panel/project_form.html", context)
    return _set_theme_cookie(response, context)


@never_cache
@_panel_permission_required("portfolio.change_project")
def panel_project_update(request, pk):
    project = get_object_or_404(Project.objects.select_related("front"), pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(
                request,
                f'O case “{project.title}” foi atualizado com sucesso.',
            )
            return redirect("portfolio:panel_project_update", pk=project.pk)
        messages.error(request, "Revise os campos destacados antes de salvar o case.")
    else:
        form = ProjectForm(instance=project)

    context = _base_context(request)
    context.update(
        {
            "form": form,
            "project": project,
            "is_editing": True,
            "is_create": False,
            "form_mode": "update",
            "cancel_url": reverse("portfolio:panel_dashboard"),
            "page_kind": "panel",
            "panel_page": "project_form",
            "page_title": f"Editar {project.title}",
        }
    )
    response = render(request, "portfolio/panel/project_form.html", context)
    return _set_theme_cookie(response, context)


def sitemap(request):
    urls = [
        request.build_absolute_uri(reverse("portfolio:home")),
        request.build_absolute_uri(
            reverse("portfolio:theme", kwargs={"theme_slug": "golden-hour"})
        ),
        request.build_absolute_uri(
            reverse("portfolio:theme", kwargs={"theme_slug": "solar-editorial"})
        ),
    ]
    urls.extend(
        request.build_absolute_uri(front.get_absolute_url())
        for front in BusinessFront.objects.filter(is_active=True).order_by(
            "sort_order", "title"
        )
    )
    urls.extend(
        request.build_absolute_uri(project.get_absolute_url())
        for project in Project.objects.filter(
            status=Project.Status.PUBLISHED,
            front__is_active=True,
        )
    )
    return render(
        request,
        "portfolio/sitemap.xml",
        {"urls": urls},
        content_type="application/xml",
    )


def robots(request):
    sitemap_url = request.build_absolute_uri(reverse("portfolio:sitemap"))
    return HttpResponse(
        f"User-agent: *\nAllow: /\nSitemap: {sitemap_url}\n",
        content_type="text/plain",
    )


def not_found(request, exception):
    context = _base_context(request)
    context["page_kind"] = "error"
    return render(request, "404.html", context, status=404)
