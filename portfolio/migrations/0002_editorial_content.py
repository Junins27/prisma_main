import unicodedata

import django.db.models.deletion
from django.db import migrations, models


def _normalized(value):
    value = unicodedata.normalize("NFKD", value or "")
    return "".join(character for character in value if not unicodedata.combining(character)).casefold()


def seed_editorial_content(apps, schema_editor):
    BusinessFront = apps.get_model("portfolio", "BusinessFront")
    Project = apps.get_model("portfolio", "Project")
    Service = apps.get_model("portfolio", "Service")
    SiteContent = apps.get_model("portfolio", "SiteContent")

    marketing, _ = BusinessFront.objects.get_or_create(
        slug="marketing",
        defaults={
            "title": "Marketing",
            "eyebrow": "Estratégia, marca e comunicação",
            "headline": "Marcas com clareza para ocupar",
            "headline_emphasis": "seu espaço no mercado.",
            "summary": (
                "Estratégia, identidade e conteúdo conectados aos objetivos reais "
                "de cada negócio."
            ),
            "description": (
                "Organizamos posicionamento, linguagem visual e presença digital "
                "para que empresas comuniquem valor de forma coerente e reconhecível."
            ),
            "cta_label": "Conheça Marketing",
            "visual_key": "marketing",
            "is_active": True,
            "sort_order": 1,
        },
    )
    technology, _ = BusinessFront.objects.get_or_create(
        slug="tecnologia",
        defaults={
            "title": "Tecnologia",
            "eyebrow": "Produtos, dados e operações",
            "headline": "Tecnologia aplicada para transformar",
            "headline_emphasis": "complexidade em clareza.",
            "summary": (
                "Experiências digitais, sistemas, dados e integrações construídos "
                "para o contexto de cada operação."
            ),
            "description": (
                "Planejamos e desenvolvemos soluções digitais com atenção à "
                "experiência, à continuidade dos dados e à evolução do negócio."
            ),
            "cta_label": "Conheça Tecnologia",
            "visual_key": "technology",
            "is_active": True,
            "sort_order": 2,
        },
    )

    service_defaults = (
        (
            marketing,
            "marketing-design",
            {
                "title": "Marketing & Design",
                "description": (
                    "Identidade, conteúdo e presença digital alinhados ao "
                    "posicionamento e aos objetivos da empresa."
                ),
                "tags": "Branding\nConteúdo\nEstratégia",
                "visual_key": "brand",
                "is_active": True,
                "sort_order": 1,
            },
        ),
        (
            technology,
            "desenvolvimento-web",
            {
                "title": "Desenvolvimento Web",
                "description": (
                    "Sites institucionais, landing pages e e-commerces com "
                    "experiência cuidadosa, performance e conteúdo claro."
                ),
                "tags": "UX/UI\nFront-end\nCMS",
                "visual_key": "prism",
                "is_active": True,
                "sort_order": 1,
            },
        ),
        (
            technology,
            "sistemas-apps",
            {
                "title": "Sistemas & Apps",
                "description": (
                    "Produtos digitais sob medida para organizar operações e "
                    "transformar processos."
                ),
                "tags": "Web apps\nAPIs",
                "visual_key": "system",
                "is_active": True,
                "sort_order": 2,
            },
        ),
        (
            technology,
            "bi-dados",
            {
                "title": "BI & Dados",
                "description": (
                    "Indicadores, dashboards e análises que tornam decisões mais visíveis."
                ),
                "tags": "Dashboards\nAnalytics",
                "visual_key": "data",
                "is_active": True,
                "sort_order": 3,
            },
        ),
        (
            technology,
            "automacoes-integracoes",
            {
                "title": "Automações & Integrações",
                "description": (
                    "Fluxos conectados para reduzir tarefas repetitivas e melhorar "
                    "a continuidade dos dados."
                ),
                "tags": "Workflows\nIntegrações",
                "visual_key": "flow",
                "is_active": True,
                "sort_order": 4,
            },
        ),
    )
    for front, slug, defaults in service_defaults:
        Service.objects.get_or_create(front=front, slug=slug, defaults=defaults)

    SiteContent.objects.get_or_create(
        singleton_key=True,
        defaults={
            "meta_title": "Prisma — Tecnologia, inteligência e criatividade",
            "meta_description": (
                "Prisma: tecnologia, dados, design e estratégia para transformar "
                "desafios de negócio em soluções digitais claras."
            ),
            "hero_eyebrow": "Tecnologia · Dados · Design",
            "hero_title": "Tecnologia, inteligência e criatividade",
            "hero_emphasis": "sob uma nova luz.",
            "hero_lead": (
                "Criamos experiências digitais, sistemas e soluções orientadas por "
                "dados para transformar desafios complexos em caminhos claros para empresas."
            ),
            "hero_primary_cta_label": "Conversar sobre um projeto",
            "hero_primary_cta_target": "#contato",
            "hero_secondary_cta_label": "Explorar o portfólio",
            "hero_secondary_cta_target": "#portfolio",
            "hero_capabilities": "Web\nSistemas\nDados\nEstratégia",
            "fronts_eyebrow": "Duas frentes, uma direção",
            "fronts_title": "Marketing e tecnologia que trabalham",
            "fronts_emphasis": "em conjunto.",
            "fronts_intro": (
                "Estratégia, comunicação e engenharia conectadas para transformar "
                "necessidades de negócio em presença, produtos e operações mais claras."
            ),
            "services_eyebrow": "O que fazemos",
            "services_title": "Competências que se encontram para criar",
            "services_emphasis": "valor real.",
            "services_intro": (
                "Conectamos pensamento estratégico, design e engenharia para construir "
                "soluções adequadas ao contexto de cada negócio."
            ),
            "differences_eyebrow": "Por que Prisma",
            "differences_title": "Mais perspectivas.",
            "differences_emphasis": "Uma direção clara.",
            "differences_body": (
                "Um prisma não cria luz; ele revela o que já existe nela. Nosso papel é "
                "reunir sinais, ideias e necessidades para transformar complexidade em "
                "uma solução coerente."
            ),
            "cases_eyebrow": "Portfólio",
            "cases_title": "Projetos que colocam ideias",
            "cases_emphasis": "em movimento.",
            "cases_intro": (
                "Esta área recebe apenas trabalhos autorizados. Cases em preparação "
                "permanecem identificados até que sua publicação seja aprovada."
            ),
            "process_eyebrow": "Como trabalhamos",
            "process_title": "Da primeira pergunta à",
            "process_emphasis": "evolução contínua.",
            "process_intro": (
                "Um processo visível, colaborativo e ajustado à complexidade de cada desafio."
            ),
            "contact_eyebrow": "Vamos conversar",
            "contact_title": "Qual desafio precisa de",
            "contact_emphasis": "uma nova perspectiva?",
            "contact_intro": (
                "Compartilhe o contexto. A mensagem fica registrada com segurança no "
                "sistema para que a equipe possa dar continuidade ao contato."
            ),
            "footer_summary": (
                "Tecnologia, dados e criatividade transformados em soluções claras."
            ),
        },
    )

    marketing_keywords = (
        "marketing",
        "design",
        "brand",
        "marca",
        "identidade",
        "conteudo",
        "comunicacao",
        "campanha",
        "social",
        "presenca",
    )
    technology_keywords = (
        "tecnologia",
        "tech",
        "sistema",
        "aplicativo",
        "app",
        "web",
        "site",
        "ecommerce",
        "e-commerce",
        "api",
        "dados",
        "data",
        "bi",
        "automacao",
        "integracao",
        "software",
        "plataforma",
        "dashboard",
        "produto digital",
    )
    for project in Project.objects.filter(front__isnull=True).iterator():
        searchable = _normalized(
            " ".join(
                (
                    project.title,
                    project.category,
                    project.summary,
                    project.deliverables,
                )
            )
        )
        if any(word in searchable for word in marketing_keywords):
            front = marketing
        elif any(word in searchable for word in technology_keywords):
            front = technology
        else:
            # Não classifica silenciosamente um case ambíguo. A migração seguinte
            # explica como concluir manualmente a classificação antes de avançar.
            continue
        Project.objects.filter(pk=project.pk).update(front_id=front.pk)


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="BusinessFront",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=80, verbose_name="nome")),
                (
                    "slug",
                    models.SlugField(
                        choices=[("marketing", "Marketing"), ("tecnologia", "Tecnologia")],
                        max_length=32,
                        unique=True,
                        verbose_name="slug",
                    ),
                ),
                ("eyebrow", models.CharField(max_length=120, verbose_name="chamada curta")),
                ("headline", models.CharField(max_length=180, verbose_name="título")),
                (
                    "headline_emphasis",
                    models.CharField(blank=True, max_length=120, verbose_name="ênfase do título"),
                ),
                ("summary", models.CharField(max_length=300, verbose_name="resumo")),
                ("description", models.TextField(max_length=1200, verbose_name="descrição")),
                (
                    "cta_label",
                    models.CharField(
                        default="Conheça esta frente",
                        max_length=80,
                        verbose_name="texto do botão",
                    ),
                ),
                (
                    "visual_key",
                    models.CharField(
                        choices=[("marketing", "Marketing"), ("technology", "Tecnologia")],
                        max_length=16,
                        verbose_name="identidade visual",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="visível no site")),
                ("sort_order", models.PositiveSmallIntegerField(default=0, verbose_name="ordem")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="atualizado em")),
            ],
            options={
                "verbose_name": "frente de atuação",
                "verbose_name_plural": "frentes de atuação",
                "ordering": ("sort_order", "title"),
            },
        ),
        migrations.CreateModel(
            name="SiteContent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("singleton_key", models.BooleanField(default=True, editable=False, unique=True)),
                (
                    "meta_title",
                    models.CharField(
                        default="Prisma — Tecnologia, inteligência e criatividade",
                        max_length=160,
                        verbose_name="título para buscadores",
                    ),
                ),
                (
                    "meta_description",
                    models.CharField(
                        default=(
                            "Prisma: tecnologia, dados, design e estratégia para transformar "
                            "desafios de negócio em soluções digitais claras."
                        ),
                        max_length=300,
                        verbose_name="descrição para buscadores",
                    ),
                ),
                (
                    "hero_eyebrow",
                    models.CharField(
                        default="Tecnologia · Dados · Design",
                        max_length=120,
                        verbose_name="chamada curta do destaque",
                    ),
                ),
                (
                    "hero_title",
                    models.CharField(
                        default="Tecnologia, inteligência e criatividade",
                        max_length=180,
                        verbose_name="título do destaque",
                    ),
                ),
                (
                    "hero_emphasis",
                    models.CharField(
                        default="sob uma nova luz.",
                        max_length=120,
                        verbose_name="ênfase do destaque",
                    ),
                ),
                (
                    "hero_lead",
                    models.TextField(
                        default=(
                            "Criamos experiências digitais, sistemas e soluções orientadas por "
                            "dados para transformar desafios complexos em caminhos claros para empresas."
                        ),
                        max_length=600,
                        verbose_name="texto do destaque",
                    ),
                ),
                (
                    "hero_primary_cta_label",
                    models.CharField(
                        default="Conversar sobre um projeto",
                        max_length=80,
                        verbose_name="texto do botão principal",
                    ),
                ),
                (
                    "hero_primary_cta_target",
                    models.CharField(
                        default="#contato",
                        help_text="Use uma âncora, como #contato, ou uma URL.",
                        max_length=200,
                        verbose_name="destino do botão principal",
                    ),
                ),
                (
                    "hero_secondary_cta_label",
                    models.CharField(
                        default="Explorar o portfólio",
                        max_length=80,
                        verbose_name="texto do botão secundário",
                    ),
                ),
                (
                    "hero_secondary_cta_target",
                    models.CharField(
                        default="#portfolio",
                        help_text="Use uma âncora, como #portfolio, ou uma URL.",
                        max_length=200,
                        verbose_name="destino do botão secundário",
                    ),
                ),
                (
                    "hero_capabilities",
                    models.TextField(
                        default="Web\nSistemas\nDados\nEstratégia",
                        help_text="Informe uma competência por linha.",
                        verbose_name="competências em destaque",
                    ),
                ),
                (
                    "fronts_eyebrow",
                    models.CharField(
                        default="Duas frentes, uma direção",
                        max_length=120,
                        verbose_name="chamada curta das frentes",
                    ),
                ),
                (
                    "fronts_title",
                    models.CharField(
                        default="Marketing e tecnologia que trabalham",
                        max_length=180,
                        verbose_name="título das frentes",
                    ),
                ),
                (
                    "fronts_emphasis",
                    models.CharField(
                        default="em conjunto.",
                        max_length=120,
                        verbose_name="ênfase das frentes",
                    ),
                ),
                (
                    "fronts_intro",
                    models.TextField(
                        default=(
                            "Estratégia, comunicação e engenharia conectadas para transformar "
                            "necessidades de negócio em presença, produtos e operações mais claras."
                        ),
                        max_length=600,
                        verbose_name="introdução das frentes",
                    ),
                ),
                (
                    "services_eyebrow",
                    models.CharField(
                        default="O que fazemos",
                        max_length=120,
                        verbose_name="chamada curta dos serviços",
                    ),
                ),
                (
                    "services_title",
                    models.CharField(
                        default="Competências que se encontram para criar",
                        max_length=180,
                        verbose_name="título dos serviços",
                    ),
                ),
                (
                    "services_emphasis",
                    models.CharField(
                        default="valor real.",
                        max_length=120,
                        verbose_name="ênfase dos serviços",
                    ),
                ),
                (
                    "services_intro",
                    models.TextField(
                        default=(
                            "Conectamos pensamento estratégico, design e engenharia para construir "
                            "soluções adequadas ao contexto de cada negócio."
                        ),
                        max_length=600,
                        verbose_name="introdução dos serviços",
                    ),
                ),
                (
                    "differences_eyebrow",
                    models.CharField(
                        default="Por que Prisma",
                        max_length=120,
                        verbose_name="chamada curta dos diferenciais",
                    ),
                ),
                (
                    "differences_title",
                    models.CharField(
                        default="Mais perspectivas.",
                        max_length=180,
                        verbose_name="título dos diferenciais",
                    ),
                ),
                (
                    "differences_emphasis",
                    models.CharField(
                        default="Uma direção clara.",
                        max_length=120,
                        verbose_name="ênfase dos diferenciais",
                    ),
                ),
                (
                    "differences_body",
                    models.TextField(
                        default=(
                            "Um prisma não cria luz; ele revela o que já existe nela. Nosso papel é "
                            "reunir sinais, ideias e necessidades para transformar complexidade em "
                            "uma solução coerente."
                        ),
                        max_length=900,
                        verbose_name="texto dos diferenciais",
                    ),
                ),
                (
                    "cases_eyebrow",
                    models.CharField(
                        default="Portfólio",
                        max_length=120,
                        verbose_name="chamada curta dos cases",
                    ),
                ),
                (
                    "cases_title",
                    models.CharField(
                        default="Projetos que colocam ideias",
                        max_length=180,
                        verbose_name="título dos cases",
                    ),
                ),
                (
                    "cases_emphasis",
                    models.CharField(
                        default="em movimento.",
                        max_length=120,
                        verbose_name="ênfase dos cases",
                    ),
                ),
                (
                    "cases_intro",
                    models.TextField(
                        default=(
                            "Esta área recebe apenas trabalhos autorizados. Cases em preparação "
                            "permanecem identificados até que sua publicação seja aprovada."
                        ),
                        max_length=600,
                        verbose_name="introdução dos cases",
                    ),
                ),
                (
                    "process_eyebrow",
                    models.CharField(
                        default="Como trabalhamos",
                        max_length=120,
                        verbose_name="chamada curta do processo",
                    ),
                ),
                (
                    "process_title",
                    models.CharField(
                        default="Da primeira pergunta à",
                        max_length=180,
                        verbose_name="título do processo",
                    ),
                ),
                (
                    "process_emphasis",
                    models.CharField(
                        default="evolução contínua.",
                        max_length=120,
                        verbose_name="ênfase do processo",
                    ),
                ),
                (
                    "process_intro",
                    models.TextField(
                        default=(
                            "Um processo visível, colaborativo e ajustado à complexidade de cada desafio."
                        ),
                        max_length=600,
                        verbose_name="introdução do processo",
                    ),
                ),
                (
                    "contact_eyebrow",
                    models.CharField(
                        default="Vamos conversar",
                        max_length=120,
                        verbose_name="chamada curta do contato",
                    ),
                ),
                (
                    "contact_title",
                    models.CharField(
                        default="Qual desafio precisa de",
                        max_length=180,
                        verbose_name="título do contato",
                    ),
                ),
                (
                    "contact_emphasis",
                    models.CharField(
                        default="uma nova perspectiva?",
                        max_length=120,
                        verbose_name="ênfase do contato",
                    ),
                ),
                (
                    "contact_intro",
                    models.TextField(
                        default=(
                            "Compartilhe o contexto. A mensagem fica registrada com segurança no "
                            "sistema para que a equipe possa dar continuidade ao contato."
                        ),
                        max_length=600,
                        verbose_name="introdução do contato",
                    ),
                ),
                (
                    "footer_summary",
                    models.CharField(
                        default="Tecnologia, dados e criatividade transformados em soluções claras.",
                        max_length=240,
                        verbose_name="resumo do rodapé",
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="atualizado em")),
            ],
            options={
                "verbose_name": "conteúdo do site",
                "verbose_name_plural": "conteúdo do site",
            },
        ),
        migrations.AlterModelOptions(
            name="project",
            options={
                "ordering": ("sort_order", "-featured", "-created_at"),
                "verbose_name": "case",
                "verbose_name_plural": "cases",
            },
        ),
        migrations.AddField(
            model_name="project",
            name="front",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="projects",
                to="portfolio.businessfront",
                verbose_name="frente",
            ),
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=120, verbose_name="título")),
                ("slug", models.SlugField(blank=True, max_length=140, verbose_name="slug")),
                ("description", models.TextField(max_length=600, verbose_name="descrição")),
                (
                    "tags",
                    models.TextField(
                        blank=True,
                        help_text="Informe uma competência por linha.",
                        verbose_name="competências",
                    ),
                ),
                (
                    "visual_key",
                    models.CharField(
                        choices=[
                            ("prism", "Web e experiências digitais"),
                            ("system", "Sistemas e aplicativos"),
                            ("data", "Dados e BI"),
                            ("flow", "Automação e integrações"),
                            ("brand", "Marketing e design"),
                        ],
                        default="prism",
                        max_length=16,
                        verbose_name="identidade visual",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="visível no site")),
                ("sort_order", models.PositiveSmallIntegerField(default=0, verbose_name="ordem")),
                (
                    "front",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="services",
                        to="portfolio.businessfront",
                        verbose_name="frente",
                    ),
                ),
            ],
            options={
                "verbose_name": "serviço",
                "verbose_name_plural": "serviços",
                "ordering": ("front__sort_order", "sort_order", "title"),
                "constraints": [
                    models.UniqueConstraint(
                        fields=("front", "slug"),
                        name="unique_service_slug_per_front",
                    )
                ],
            },
        ),
        migrations.RunPython(seed_editorial_content, migrations.RunPython.noop),
    ]
