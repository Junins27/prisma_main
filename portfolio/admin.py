from django.contrib import admin
from django.db.models import Count, Q

from .models import BusinessFront, ContactMessage, Project, Service, SiteContent


class ServiceInline(admin.StackedInline):
    model = Service
    extra = 0
    fields = (
        "title",
        "slug",
        "description",
        "tags",
        "visual_key",
        "is_active",
        "sort_order",
    )
    ordering = ("sort_order", "title")
    prepopulated_fields = {"slug": ("title",)}
    show_change_link = True


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")
    readonly_fields = ("updated_at",)
    save_on_top = True
    fieldsets = (
        (
            "Busca e compartilhamento",
            {"fields": ("meta_title", "meta_description")},
        ),
        (
            "Destaque principal",
            {
                "fields": (
                    "hero_eyebrow",
                    "hero_title",
                    "hero_emphasis",
                    "hero_lead",
                    "hero_primary_cta_label",
                    "hero_primary_cta_target",
                    "hero_secondary_cta_label",
                    "hero_secondary_cta_target",
                    "hero_capabilities",
                )
            },
        ),
        (
            "Frentes principais",
            {
                "fields": (
                    "fronts_eyebrow",
                    "fronts_title",
                    "fronts_emphasis",
                    "fronts_intro",
                )
            },
        ),
        (
            "Serviços",
            {
                "fields": (
                    "services_eyebrow",
                    "services_title",
                    "services_emphasis",
                    "services_intro",
                )
            },
        ),
        (
            "Diferenciais",
            {
                "fields": (
                    "differences_eyebrow",
                    "differences_title",
                    "differences_emphasis",
                    "differences_body",
                )
            },
        ),
        (
            "Cases",
            {
                "fields": (
                    "cases_eyebrow",
                    "cases_title",
                    "cases_emphasis",
                    "cases_intro",
                )
            },
        ),
        (
            "Processo",
            {
                "fields": (
                    "process_eyebrow",
                    "process_title",
                    "process_emphasis",
                    "process_intro",
                )
            },
        ),
        (
            "Contato e rodapé",
            {
                "fields": (
                    "contact_eyebrow",
                    "contact_title",
                    "contact_emphasis",
                    "contact_intro",
                    "footer_summary",
                )
            },
        ),
        ("Histórico", {"fields": ("updated_at",)}),
    )

    def has_add_permission(self, request):
        return not SiteContent.objects.exists() and super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BusinessFront)
class BusinessFrontAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "is_active",
        "sort_order",
        "service_count",
        "published_case_count",
        "updated_at",
    )
    list_editable = ("is_active", "sort_order")
    list_filter = ("is_active", "visual_key")
    search_fields = ("title", "headline", "summary", "description")
    readonly_fields = ("slug", "updated_at")
    ordering = ("sort_order", "title")
    inlines = (ServiceInline,)
    save_on_top = True
    fieldsets = (
        (
            "Identificação",
            {"fields": ("title", "slug", "visual_key", "is_active", "sort_order")},
        ),
        (
            "Apresentação",
            {
                "fields": (
                    "eyebrow",
                    "headline",
                    "headline_emphasis",
                    "summary",
                    "description",
                    "cta_label",
                )
            },
        ),
        ("Histórico", {"fields": ("updated_at",)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _service_count=Count("services", distinct=True),
            _published_case_count=Count(
                "projects",
                filter=Q(projects__status=Project.Status.PUBLISHED),
                distinct=True,
            ),
        )

    @admin.display(description="serviços", ordering="_service_count")
    def service_count(self, obj):
        return obj._service_count

    @admin.display(description="cases publicados", ordering="_published_case_count")
    def published_case_count(self, obj):
        return obj._published_case_count

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "front", "visual_key", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    list_filter = ("front", "is_active", "visual_key")
    list_select_related = ("front",)
    search_fields = ("title", "description", "tags", "front__title")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("front",)
    ordering = ("front__sort_order", "sort_order", "title")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "front",
        "category",
        "status",
        "featured",
        "sort_order",
        "updated_at",
    )
    list_filter = ("front", "status", "featured", "category")
    list_editable = ("status", "featured", "sort_order")
    list_select_related = ("front",)
    search_fields = (
        "title",
        "front__title",
        "category",
        "summary",
        "deliverables",
    )
    autocomplete_fields = ("front",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    fieldsets = (
        (
            "Apresentação",
            {"fields": ("front", "title", "slug", "category", "summary")},
        ),
        ("Case", {"fields": ("challenge", "solution", "deliverables")}),
        ("Mídia e link", {"fields": ("image", "image_alt", "external_url")}),
        ("Publicação", {"fields": ("status", "featured", "sort_order")}),
        ("Histórico", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "project_type", "status", "created_at")
    list_filter = ("status", "project_type", "source_theme", "created_at")
    list_editable = ("status",)
    search_fields = ("name", "email", "company", "message")
    readonly_fields = (
        "name",
        "email",
        "company",
        "project_type",
        "message",
        "privacy_consent",
        "source_theme",
        "created_at",
    )
    fieldsets = (
        ("Contato", {"fields": ("name", "email", "company", "project_type")}),
        ("Mensagem", {"fields": ("message",)}),
        ("Registro", {"fields": ("privacy_consent", "source_theme", "created_at", "status")}),
    )

    def has_add_permission(self, request):
        return False


admin.site.site_header = "Prisma — Administração"
admin.site.site_title = "Prisma Admin"
admin.site.index_title = "Conteúdo e operação"
admin.site.index_template = "admin/prisma_index.html"
