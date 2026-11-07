from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.test import Client, TestCase
from django.test import override_settings
from django.urls import reverse

from .models import BusinessFront, ContactMessage, Project, Service, SiteContent


class PortfolioDataMixin:
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.marketing = BusinessFront.objects.get(slug="marketing")
        cls.technology = BusinessFront.objects.get(slug="tecnologia")

    def make_project(
        self,
        title,
        front=None,
        status=Project.Status.PUBLISHED,
        **kwargs,
    ):
        defaults = {
            "front": front or self.technology,
            "category": "Sistema",
            "summary": "Resumo autorizado do projeto.",
            "challenge": "Descrição do desafio.",
            "solution": "Descrição da solução.",
            "deliverables": "UX, Desenvolvimento, Integração",
            "status": status,
        }
        defaults.update(kwargs)
        return Project.objects.create(title=title, **defaults)

    @staticmethod
    def service_visual_key():
        return next(
            value
            for value, _label in Service._meta.get_field("visual_key").flatchoices
            if value
        )

    def make_service(self, title, front=None, **kwargs):
        defaults = {
            "front": front or self.technology,
            "slug": title.lower().replace(" ", "-"),
            "description": "Descrição pública do serviço.",
            "tags": "Estratégia, Execução",
            "visual_key": self.service_visual_key(),
            "is_active": True,
            "sort_order": 90,
        }
        defaults.update(kwargs)
        return Service.objects.create(title=title, **defaults)


class PortfolioPagesTests(PortfolioDataMixin, TestCase):
    def setUp(self):
        cache.clear()

    def test_home_highlights_both_business_fronts_in_both_themes(self):
        themes = (
            ("golden-hour", "golden"),
            ("solar-editorial", "solar"),
        )

        for theme_slug, theme_key in themes:
            with self.subTest(theme=theme_slug):
                response = self.client.get(
                    reverse(
                        "portfolio:theme",
                        kwargs={"theme_slug": theme_slug},
                    )
                )

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, f'data-theme="{theme_key}"')
                self.assertContains(response, 'class="section front-gateway"')
                self.assertContains(
                    response,
                    "front-card front-card--marketing",
                    count=1,
                )
                self.assertContains(
                    response,
                    "front-card front-card--tecnologia",
                    count=1,
                )
                self.assertContains(response, self.marketing.get_absolute_url())
                self.assertContains(response, self.technology.get_absolute_url())
                self.assertNotContains(response, "Cliente exemplo")

    def test_each_theme_has_a_direct_url_and_sets_preference_cookie(self):
        cases = (
            ("golden-hour", "golden"),
            ("solar-editorial", "solar"),
        )
        for slug, key in cases:
            with self.subTest(slug=slug):
                response = self.client.get(
                    reverse("portfolio:theme", kwargs={"theme_slug": slug})
                )
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, f'data-theme="{key}"')
                self.assertEqual(response.cookies["prisma_theme"].value, key)

    def test_editing_site_content_is_reflected_on_home(self):
        site_content = SiteContent.load()
        site_content.fronts_title = "Duas especialidades que trabalham juntas"
        site_content.save(update_fields=("fronts_title",))

        response = self.client.get(reverse("portfolio:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Duas especialidades que trabalham juntas",
        )

    def test_unknown_theme_returns_404(self):
        response = self.client.get(
            reverse("portfolio:theme", kwargs={"theme_slug": "desconhecido"})
        )
        self.assertEqual(response.status_code, 404)

    @override_settings(DEBUG=False)
    def test_invalid_theme_query_falls_back_without_breaking_404_handler(self):
        response = self.client.get("/?tema=desconhecido")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-theme="golden"')

        missing_response = self.client.get("/pagina-inexistente/?tema=desconhecido")
        self.assertEqual(missing_response.status_code, 404)
        self.assertContains(
            missing_response,
            "Esta perspectiva ainda não existe",
            status_code=404,
        )

    def test_valid_contact_is_persisted_with_source_theme(self):
        response = self.client.post(
            reverse("portfolio:theme", kwargs={"theme_slug": "solar-editorial"}),
            {
                "name": "Pessoa Interessada",
                "email": "pessoa@example.com",
                "company": "Empresa",
                "project_type": ContactMessage.ProjectType.SYSTEM,
                "message": "Precisamos organizar um fluxo interno com um novo sistema.",
                "privacy_consent": "on",
                "website": "",
            },
        )

        self.assertRedirects(
            response,
            reverse("portfolio:theme", kwargs={"theme_slug": "solar-editorial"})
            + "#contato",
        )
        contact = ContactMessage.objects.get()
        self.assertEqual(contact.source_theme, "solar")
        self.assertTrue(contact.privacy_consent)

    def test_contact_post_without_csrf_is_rejected(self):
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post(
            reverse("portfolio:home"),
            {
                "name": "Pessoa",
                "email": "pessoa@example.com",
                "project_type": ContactMessage.ProjectType.WEBSITE,
                "message": "Tentativa sem token CSRF.",
                "privacy_consent": "on",
                "website": "",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(ContactMessage.objects.exists())

    def test_contact_requires_consent(self):
        response = self.client.post(
            reverse("portfolio:home"),
            {
                "name": "Pessoa",
                "email": "pessoa@example.com",
                "project_type": ContactMessage.ProjectType.WEBSITE,
                "message": "Quero conversar sobre um novo site institucional.",
                "website": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "É necessário aceitar o uso dos dados")
        self.assertFalse(ContactMessage.objects.exists())

    def test_honeypot_rejects_automated_submission(self):
        response = self.client.post(
            reverse("portfolio:home"),
            {
                "name": "Robô",
                "email": "bot@example.com",
                "project_type": ContactMessage.ProjectType.OTHER,
                "message": "Mensagem automatizada.",
                "privacy_consent": "on",
                "website": "https://spam.example",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("website", response.context["contact_form"].errors)
        self.assertContains(response, "Revise os campos destacados")
        self.assertFalse(ContactMessage.objects.exists())

    @override_settings(CONTACT_RATE_LIMIT=2, CONTACT_RATE_WINDOW=600)
    def test_contact_rate_limit_blocks_excess_attempts(self):
        payload = {
            "name": "Pessoa",
            "email": "pessoa@example.com",
            "project_type": ContactMessage.ProjectType.WEBSITE,
            "message": "Mensagem sem consentimento apenas para contar tentativas.",
            "website": "",
        }

        self.client.post(reverse("portfolio:home"), payload)
        self.client.post(reverse("portfolio:home"), payload)
        response = self.client.post(reverse("portfolio:home"), payload)

        self.assertEqual(response.status_code, 429)
        self.assertContains(
            response,
            "Muitas tentativas de envio",
            status_code=429,
        )


class BusinessFrontPagesTests(PortfolioDataMixin, TestCase):
    def test_front_pages_filter_projects_by_front_and_status(self):
        marketing_case = self.make_project(
            "Campanha pública",
            front=self.marketing,
            category="Marketing",
        )
        marketing_draft = self.make_project(
            "Campanha ainda privada",
            front=self.marketing,
            category="Marketing",
            status=Project.Status.DRAFT,
        )
        technology_case = self.make_project(
            "Plataforma pública",
            front=self.technology,
        )

        marketing_response = self.client.get(
            reverse(
                "portfolio:front_detail",
                kwargs={"slug": self.marketing.slug},
            )
        )
        technology_response = self.client.get(
            reverse(
                "portfolio:front_detail",
                kwargs={"slug": self.technology.slug},
            )
        )

        self.assertEqual(marketing_response.status_code, 200)
        self.assertContains(
            marketing_response,
            f"front-page--{self.marketing.visual_key}",
        )
        self.assertContains(marketing_response, marketing_case.title)
        self.assertNotContains(marketing_response, marketing_draft.title)
        self.assertNotContains(marketing_response, technology_case.title)

        self.assertEqual(technology_response.status_code, 200)
        self.assertContains(
            technology_response,
            f"front-page--{self.technology.visual_key}",
        )
        self.assertContains(technology_response, technology_case.title)
        self.assertNotContains(technology_response, marketing_case.title)

    def test_front_page_only_lists_active_services_from_that_front(self):
        active_service = self.make_service(
            "Consultoria ativa",
            front=self.marketing,
            slug="consultoria-ativa",
        )
        inactive_service = self.make_service(
            "Consultoria oculta",
            front=self.marketing,
            slug="consultoria-oculta",
            is_active=False,
        )
        other_front_service = self.make_service(
            "Arquitetura técnica",
            front=self.technology,
            slug="arquitetura-tecnica",
        )

        response = self.client.get(self.marketing.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, active_service.title)
        self.assertNotContains(response, inactive_service.title)
        self.assertNotContains(response, other_front_service.title)


class ProjectTests(PortfolioDataMixin, TestCase):

    def test_only_published_projects_appear_on_site(self):
        published = self.make_project("Projeto publicado")
        draft = self.make_project("Projeto em rascunho", status=Project.Status.DRAFT)

        response = self.client.get(reverse("portfolio:home"))

        self.assertContains(response, published.title)
        self.assertNotContains(response, draft.title)
        self.assertNotContains(response, "Case em preparação")
        self.assertEqual(
            self.client.get(published.get_absolute_url()).status_code, 200
        )
        self.assertEqual(self.client.get(draft.get_absolute_url()).status_code, 404)

    def test_project_slug_is_generated_and_kept_unique(self):
        first = self.make_project("Painel de dados")
        second = self.make_project("Painel de dados")

        self.assertEqual(first.slug, "painel-de-dados")
        self.assertEqual(second.slug, "painel-de-dados-2")

    def test_sitemap_contains_published_project_only(self):
        published = self.make_project("Visível no mapa")
        draft = self.make_project("Oculto do mapa", status=Project.Status.DRAFT)

        response = self.client.get(reverse("portfolio:sitemap"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertContains(response, self.marketing.get_absolute_url())
        self.assertContains(response, self.technology.get_absolute_url())
        self.assertContains(response, published.get_absolute_url())
        self.assertNotContains(response, draft.get_absolute_url())

    def test_published_project_requires_a_business_front(self):
        project = Project(
            title="Case sem frente",
            category="Sistema",
            summary="Este case não pode ser publicado sem uma frente.",
            challenge="Descrição do desafio.",
            solution="Descrição da solução.",
            deliverables="Estratégia, Desenvolvimento",
            status=Project.Status.PUBLISHED,
        )

        with self.assertRaises(ValidationError) as raised:
            project.full_clean()

        self.assertIn("front", raised.exception.message_dict)

    def test_deliverables_are_normalized_for_template(self):
        project = self.make_project(
            "Entregáveis", deliverables="UX,  API, , Painel "
        )
        self.assertEqual(project.deliverables_list, ["UX", "API", "Painel"])


class AdminPanelTests(PortfolioDataMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.admin_user = get_user_model().objects.create_superuser(
            username="admin-tests",
            email="admin@example.com",
            password="senha-forte-para-testes",
        )

    def setUp(self):
        self.client.force_login(self.admin_user)

    @staticmethod
    def admin_payload(instance):
        payload = {}
        for field in instance._meta.fields:
            if field.primary_key or not field.editable:
                continue
            value = field.value_from_object(instance)
            if isinstance(field, models.BooleanField):
                if value:
                    payload[field.name] = "on"
            elif isinstance(field, models.ForeignKey):
                payload[field.name] = str(value) if value is not None else ""
            else:
                payload[field.name] = "" if value is None else str(value)
        return payload

    def test_admin_index_and_content_changelists_are_available(self):
        index_response = self.client.get(reverse("admin:index"))

        self.assertEqual(index_response.status_code, 200)
        for url_name in (
            "admin:portfolio_businessfront_changelist",
            "admin:portfolio_service_changelist",
            "admin:portfolio_sitecontent_changelist",
            "admin:portfolio_project_changelist",
        ):
            with self.subTest(url_name=url_name):
                url = reverse(url_name)
                self.assertContains(index_response, url)
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)

    def test_business_front_change_view_and_site_content_edit_are_available(self):
        front_response = self.client.get(
            reverse(
                "admin:portfolio_businessfront_change",
                args=(self.marketing.pk,),
            )
        )

        self.assertEqual(front_response.status_code, 200)
        self.assertContains(front_response, self.marketing.headline)
        self.assertContains(front_response, "Serviços")

        site_content = SiteContent.load()
        content_payload = self.admin_payload(site_content)
        content_payload["hero_title"] = "Uma nova mensagem institucional"
        content_response = self.client.post(
            reverse(
                "admin:portfolio_sitecontent_change",
                args=(site_content.pk,),
            ),
            content_payload,
        )

        self.assertEqual(content_response.status_code, 302)
        site_content.refresh_from_db()
        self.assertEqual(
            site_content.hero_title,
            "Uma nova mensagem institucional",
        )

    def test_service_crud_through_admin(self):
        add_url = reverse("admin:portfolio_service_add")
        add_response = self.client.post(
            add_url,
            {
                "front": self.marketing.pk,
                "title": "Planejamento editorial",
                "slug": "planejamento-editorial",
                "description": "Planejamento de conteúdo por canais.",
                "tags": "Conteúdo, Canais",
                "visual_key": self.service_visual_key(),
                "is_active": "on",
                "sort_order": 50,
            },
        )

        self.assertEqual(add_response.status_code, 302)
        service = Service.objects.get(slug="planejamento-editorial")

        change_url = reverse(
            "admin:portfolio_service_change",
            args=(service.pk,),
        )
        change_response = self.client.post(
            change_url,
            {
                "front": self.marketing.pk,
                "title": service.title,
                "slug": service.slug,
                "description": "Descrição revisada no painel.",
                "tags": service.tags,
                "visual_key": service.visual_key,
                "is_active": "on",
                "sort_order": service.sort_order,
            },
        )

        self.assertEqual(change_response.status_code, 302)
        service.refresh_from_db()
        self.assertEqual(service.description, "Descrição revisada no painel.")

        delete_response = self.client.post(
            reverse("admin:portfolio_service_delete", args=(service.pk,)),
            {"post": "yes"},
        )

        self.assertEqual(delete_response.status_code, 302)
        self.assertFalse(Service.objects.filter(pk=service.pk).exists())

    def test_project_can_be_created_with_a_front_in_admin(self):
        response = self.client.post(
            reverse("admin:portfolio_project_add"),
            {
                "front": self.technology.pk,
                "title": "Case cadastrado pelo painel",
                "slug": "case-cadastrado-pelo-painel",
                "category": "Sistema",
                "summary": "Resumo autorizado do projeto.",
                "challenge": "Descrição do desafio.",
                "solution": "Descrição da solução.",
                "deliverables": "UX, Desenvolvimento",
                "image_alt": "",
                "external_url": "",
                "status": Project.Status.DRAFT,
                "sort_order": 0,
            },
        )

        self.assertEqual(response.status_code, 302)
        project = Project.objects.get(slug="case-cadastrado-pelo-painel")
        self.assertEqual(project.front, self.technology)


class EditorialPanelTests(PortfolioDataMixin, TestCase):
    password = "senha-segura-do-painel"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        user_model = get_user_model()
        cls.superuser = user_model.objects.create_superuser(
            username="painel-superuser",
            email="painel-superuser@example.com",
            password=cls.password,
        )
        cls.non_staff_user = user_model.objects.create_user(
            username="usuario-sem-acesso",
            email="sem-acesso@example.com",
            password=cls.password,
        )
        cls.staff_without_permissions = user_model.objects.create_user(
            username="staff-sem-permissoes",
            is_staff=True,
        )
        cls.viewer = user_model.objects.create_user(
            username="staff-visualizacao",
            is_staff=True,
        )
        cls.creator = user_model.objects.create_user(
            username="staff-criacao",
            is_staff=True,
        )
        cls.editor = user_model.objects.create_user(
            username="staff-edicao",
            is_staff=True,
        )

        permissions = {
            permission.codename: permission
            for permission in Permission.objects.filter(
                content_type__app_label="portfolio",
                content_type__model="project",
                codename__in=(
                    "view_project",
                    "add_project",
                    "change_project",
                ),
            )
        }
        cls.viewer.user_permissions.add(permissions["view_project"])
        cls.creator.user_permissions.add(permissions["add_project"])
        cls.editor.user_permissions.add(permissions["change_project"])

    def project_form_payload(self, title, front=None, **overrides):
        payload = {
            "front": (front or self.technology).pk,
            "title": title,
            "category": "Sistema",
            "summary": "Resumo autorizado do case.",
            "challenge": "Descrição do desafio.",
            "solution": "Descrição da solução.",
            "deliverables": "UX, Desenvolvimento",
            "image_alt": "",
            "external_url": "",
            "status": Project.Status.DRAFT,
            "sort_order": 0,
        }
        payload.update(overrides)
        return payload

    def test_anonymous_user_is_redirected_to_panel_login(self):
        dashboard_url = reverse("portfolio:panel_dashboard")
        login_url = reverse("portfolio:panel_login")

        response = self.client.get(dashboard_url)

        self.assertRedirects(
            response,
            f"{login_url}?next={dashboard_url}",
        )

    def test_panel_login_rejects_authenticated_non_staff_user(self):
        response = self.client.post(
            reverse("portfolio:panel_login"),
            {
                "username": self.non_staff_user.username,
                "password": self.password,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertTrue(response.context["form"].non_field_errors())

    def test_superuser_opens_custom_dashboard(self):
        self.client.force_login(self.superuser)

        response = self.client.get(reverse("portfolio:panel_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portfolio/panel/dashboard.html")
        self.assertContains(response, "Marketing")
        self.assertContains(response, "Tecnologia")

    def test_dashboard_filters_cases_by_query_front_and_status(self):
        marketing_published = self.make_project(
            "Campanha Aurora",
            front=self.marketing,
            category="Marketing",
        )
        marketing_draft = self.make_project(
            "Calendário editorial reservado",
            front=self.marketing,
            category="Marketing",
            status=Project.Status.DRAFT,
        )
        technology_published = self.make_project(
            "Portal Orion",
            front=self.technology,
        )
        self.client.force_login(self.superuser)
        dashboard_url = reverse("portfolio:panel_dashboard")

        query_response = self.client.get(dashboard_url, {"q": "Aurora"})
        self.assertContains(query_response, marketing_published.title)
        self.assertNotContains(query_response, marketing_draft.title)
        self.assertNotContains(query_response, technology_published.title)

        front_response = self.client.get(
            dashboard_url,
            {"front": self.marketing.slug},
        )
        self.assertContains(front_response, marketing_published.title)
        self.assertContains(front_response, marketing_draft.title)
        self.assertNotContains(front_response, technology_published.title)

        status_response = self.client.get(
            dashboard_url,
            {"status": Project.Status.DRAFT},
        )
        self.assertContains(status_response, marketing_draft.title)
        self.assertNotContains(status_response, marketing_published.title)
        self.assertNotContains(status_response, technology_published.title)

    def test_superuser_creates_case_linked_to_selected_front(self):
        self.client.force_login(self.superuser)

        response = self.client.post(
            reverse("portfolio:panel_project_create"),
            self.project_form_payload(
                "Case criado no painel editorial",
                front=self.marketing,
            ),
        )

        self.assertRedirects(response, reverse("portfolio:panel_dashboard"))
        project = Project.objects.get(title="Case criado no painel editorial")
        self.assertEqual(project.front, self.marketing)
        self.assertEqual(project.slug, "case-criado-no-painel-editorial")

    def test_superuser_edits_case_in_custom_panel(self):
        project = self.make_project(
            "Case antes da revisão",
            status=Project.Status.DRAFT,
        )
        self.client.force_login(self.superuser)
        update_url = reverse(
            "portfolio:panel_project_update",
            kwargs={"pk": project.pk},
        )

        response = self.client.post(
            update_url,
            self.project_form_payload(
                "Case depois da revisão",
                front=self.marketing,
                summary="Resumo revisado pelo painel.",
            ),
        )

        self.assertRedirects(response, update_url)
        project.refresh_from_db()
        self.assertEqual(project.title, "Case depois da revisão")
        self.assertEqual(project.summary, "Resumo revisado pelo painel.")
        self.assertEqual(project.front, self.marketing)

    def test_logout_requires_post_and_get_keeps_session_active(self):
        self.client.force_login(self.superuser)
        logout_url = reverse("portfolio:panel_logout")

        get_response = self.client.get(logout_url)

        self.assertEqual(get_response.status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)
        self.assertEqual(
            self.client.get(reverse("portfolio:panel_dashboard")).status_code,
            200,
        )

        post_response = self.client.post(logout_url)

        self.assertEqual(post_response.status_code, 302)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_staff_without_permissions_receives_forbidden(self):
        project = self.make_project(
            "Case protegido por permissão",
            status=Project.Status.DRAFT,
        )
        self.client.force_login(self.staff_without_permissions)

        protected_urls = (
            reverse("portfolio:panel_dashboard"),
            reverse("portfolio:panel_project_create"),
            reverse(
                "portfolio:panel_project_update",
                kwargs={"pk": project.pk},
            ),
        )
        for url in protected_urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 403)

    def test_staff_with_matching_permission_can_perform_each_action(self):
        project = self.make_project(
            "Case para editor autorizado",
            status=Project.Status.DRAFT,
        )

        self.client.force_login(self.viewer)
        self.assertEqual(
            self.client.get(reverse("portfolio:panel_dashboard")).status_code,
            200,
        )

        self.client.force_login(self.creator)
        create_response = self.client.post(
            reverse("portfolio:panel_project_create"),
            self.project_form_payload(
                "Case criado por usuário autorizado",
                front=self.marketing,
            ),
        )
        self.assertEqual(create_response.status_code, 302)
        self.assertTrue(
            Project.objects.filter(
                title="Case criado por usuário autorizado",
                front=self.marketing,
            ).exists()
        )

        self.client.force_login(self.editor)
        update_url = reverse(
            "portfolio:panel_project_update",
            kwargs={"pk": project.pk},
        )
        update_response = self.client.post(
            update_url,
            self.project_form_payload(
                "Case editado por usuário autorizado",
                front=project.front,
            ),
        )
        self.assertEqual(update_response.status_code, 302)
        project.refresh_from_db()
        self.assertEqual(project.title, "Case editado por usuário autorizado")
