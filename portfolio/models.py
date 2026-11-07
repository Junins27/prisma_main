from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class SiteContent(models.Model):
    """Conteúdo institucional compartilhado pelos dois temas visuais."""

    singleton_key = models.BooleanField(default=True, unique=True, editable=False)
    meta_title = models.CharField(
        "título para buscadores",
        max_length=160,
        default="Prisma — Tecnologia, inteligência e criatividade",
    )
    meta_description = models.CharField(
        "descrição para buscadores",
        max_length=300,
        default=(
            "Prisma: tecnologia, dados, design e estratégia para transformar "
            "desafios de negócio em soluções digitais claras."
        ),
    )

    hero_eyebrow = models.CharField(
        "chamada curta do destaque",
        max_length=120,
        default="Tecnologia · Dados · Design",
    )
    hero_title = models.CharField(
        "título do destaque",
        max_length=180,
        default="Tecnologia, inteligência e criatividade",
    )
    hero_emphasis = models.CharField(
        "ênfase do destaque",
        max_length=120,
        default="sob uma nova luz.",
    )
    hero_lead = models.TextField(
        "texto do destaque",
        max_length=600,
        default=(
            "Criamos experiências digitais, sistemas e soluções orientadas por "
            "dados para transformar desafios complexos em caminhos claros para empresas."
        ),
    )
    hero_primary_cta_label = models.CharField(
        "texto do botão principal",
        max_length=80,
        default="Conversar sobre um projeto",
    )
    hero_primary_cta_target = models.CharField(
        "destino do botão principal",
        max_length=200,
        default="#contato",
        help_text="Use uma âncora, como #contato, ou uma URL.",
    )
    hero_secondary_cta_label = models.CharField(
        "texto do botão secundário",
        max_length=80,
        default="Explorar o portfólio",
    )
    hero_secondary_cta_target = models.CharField(
        "destino do botão secundário",
        max_length=200,
        default="#portfolio",
        help_text="Use uma âncora, como #portfolio, ou uma URL.",
    )
    hero_capabilities = models.TextField(
        "competências em destaque",
        default="Web\nSistemas\nDados\nEstratégia",
        help_text="Informe uma competência por linha.",
    )

    fronts_eyebrow = models.CharField(
        "chamada curta das frentes",
        max_length=120,
        default="Duas frentes, uma direção",
    )
    fronts_title = models.CharField(
        "título das frentes",
        max_length=180,
        default="Marketing e tecnologia que trabalham",
    )
    fronts_emphasis = models.CharField(
        "ênfase das frentes",
        max_length=120,
        default="em conjunto.",
    )
    fronts_intro = models.TextField(
        "introdução das frentes",
        max_length=600,
        default=(
            "Estratégia, comunicação e engenharia conectadas para transformar "
            "necessidades de negócio em presença, produtos e operações mais claras."
        ),
    )

    services_eyebrow = models.CharField(
        "chamada curta dos serviços",
        max_length=120,
        default="O que fazemos",
    )
    services_title = models.CharField(
        "título dos serviços",
        max_length=180,
        default="Competências que se encontram para criar",
    )
    services_emphasis = models.CharField(
        "ênfase dos serviços",
        max_length=120,
        default="valor real.",
    )
    services_intro = models.TextField(
        "introdução dos serviços",
        max_length=600,
        default=(
            "Conectamos pensamento estratégico, design e engenharia para construir "
            "soluções adequadas ao contexto de cada negócio."
        ),
    )

    differences_eyebrow = models.CharField(
        "chamada curta dos diferenciais",
        max_length=120,
        default="Por que Prisma",
    )
    differences_title = models.CharField(
        "título dos diferenciais",
        max_length=180,
        default="Mais perspectivas.",
    )
    differences_emphasis = models.CharField(
        "ênfase dos diferenciais",
        max_length=120,
        default="Uma direção clara.",
    )
    differences_body = models.TextField(
        "texto dos diferenciais",
        max_length=900,
        default=(
            "Um prisma não cria luz; ele revela o que já existe nela. Nosso papel é "
            "reunir sinais, ideias e necessidades para transformar complexidade em "
            "uma solução coerente."
        ),
    )

    cases_eyebrow = models.CharField(
        "chamada curta dos cases",
        max_length=120,
        default="Portfólio",
    )
    cases_title = models.CharField(
        "título dos cases",
        max_length=180,
        default="Projetos que colocam ideias",
    )
    cases_emphasis = models.CharField(
        "ênfase dos cases",
        max_length=120,
        default="em movimento.",
    )
    cases_intro = models.TextField(
        "introdução dos cases",
        max_length=600,
        default=(
            "Esta área recebe apenas trabalhos autorizados. Cases em preparação "
            "permanecem identificados até que sua publicação seja aprovada."
        ),
    )

    process_eyebrow = models.CharField(
        "chamada curta do processo",
        max_length=120,
        default="Como trabalhamos",
    )
    process_title = models.CharField(
        "título do processo",
        max_length=180,
        default="Da primeira pergunta à",
    )
    process_emphasis = models.CharField(
        "ênfase do processo",
        max_length=120,
        default="evolução contínua.",
    )
    process_intro = models.TextField(
        "introdução do processo",
        max_length=600,
        default=(
            "Um processo visível, colaborativo e ajustado à complexidade de cada desafio."
        ),
    )

    contact_eyebrow = models.CharField(
        "chamada curta do contato",
        max_length=120,
        default="Vamos conversar",
    )
    contact_title = models.CharField(
        "título do contato",
        max_length=180,
        default="Qual desafio precisa de",
    )
    contact_emphasis = models.CharField(
        "ênfase do contato",
        max_length=120,
        default="uma nova perspectiva?",
    )
    contact_intro = models.TextField(
        "introdução do contato",
        max_length=600,
        default=(
            "Compartilhe o contexto. A mensagem fica registrada com segurança no "
            "sistema para que a equipe possa dar continuidade ao contato."
        ),
    )
    footer_summary = models.CharField(
        "resumo do rodapé",
        max_length=240,
        default="Tecnologia, dados e criatividade transformados em soluções claras.",
    )
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "conteúdo do site"
        verbose_name_plural = "conteúdo do site"

    def __str__(self):
        return "Conteúdo global da Prisma"

    def clean(self):
        super().clean()
        if SiteContent.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Já existe um registro de conteúdo global.")

    def save(self, *args, **kwargs):
        self.singleton_key = True
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Retorna o único conteúdo, criando-o com os padrões quando necessário."""
        content, _ = cls.objects.get_or_create(singleton_key=True)
        return content

    @property
    def hero_capabilities_list(self):
        return [item.strip() for item in self.hero_capabilities.splitlines() if item.strip()]


class BusinessFront(models.Model):
    class Slug(models.TextChoices):
        MARKETING = "marketing", "Marketing"
        TECHNOLOGY = "tecnologia", "Tecnologia"

    class VisualKey(models.TextChoices):
        MARKETING = "marketing", "Marketing"
        TECHNOLOGY = "technology", "Tecnologia"

    title = models.CharField("nome", max_length=80)
    slug = models.SlugField("slug", max_length=32, unique=True, choices=Slug.choices)
    eyebrow = models.CharField("chamada curta", max_length=120)
    headline = models.CharField("título", max_length=180)
    headline_emphasis = models.CharField("ênfase do título", max_length=120, blank=True)
    summary = models.CharField("resumo", max_length=300)
    description = models.TextField("descrição", max_length=1200)
    cta_label = models.CharField("texto do botão", max_length=80, default="Conheça esta frente")
    visual_key = models.CharField(
        "identidade visual",
        max_length=16,
        choices=VisualKey.choices,
    )
    is_active = models.BooleanField("visível no site", default=True)
    sort_order = models.PositiveSmallIntegerField("ordem", default=0)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "frente de atuação"
        verbose_name_plural = "frentes de atuação"
        ordering = ("sort_order", "title")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("portfolio:front_detail", kwargs={"slug": self.slug})


class Service(models.Model):
    class VisualKey(models.TextChoices):
        PRISM = "prism", "Web e experiências digitais"
        SYSTEM = "system", "Sistemas e aplicativos"
        DATA = "data", "Dados e BI"
        FLOW = "flow", "Automação e integrações"
        BRAND = "brand", "Marketing e design"

    front = models.ForeignKey(
        BusinessFront,
        on_delete=models.PROTECT,
        related_name="services",
        verbose_name="frente",
    )
    title = models.CharField("título", max_length=120)
    slug = models.SlugField("slug", max_length=140, blank=True)
    description = models.TextField("descrição", max_length=600)
    tags = models.TextField(
        "competências",
        blank=True,
        help_text="Informe uma competência por linha.",
    )
    visual_key = models.CharField(
        "identidade visual",
        max_length=16,
        choices=VisualKey.choices,
        default=VisualKey.PRISM,
    )
    is_active = models.BooleanField("visível no site", default=True)
    sort_order = models.PositiveSmallIntegerField("ordem", default=0)

    class Meta:
        verbose_name = "serviço"
        verbose_name_plural = "serviços"
        ordering = ("front__sort_order", "sort_order", "title")
        constraints = (
            models.UniqueConstraint(
                fields=("front", "slug"),
                name="unique_service_slug_per_front",
            ),
        )

    def __str__(self):
        return f"{self.front}: {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "servico"
            candidate = base_slug
            suffix = 2
            queryset = Service.objects.exclude(pk=self.pk).filter(front_id=self.front_id)
            while queryset.filter(slug=candidate).exists():
                candidate = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    @property
    def tags_list(self):
        normalized = self.tags.replace(",", "\n")
        return [item.strip() for item in normalized.splitlines() if item.strip()]


class Project(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Rascunho"
        PUBLISHED = "published", "Publicado"

    front = models.ForeignKey(
        BusinessFront,
        on_delete=models.PROTECT,
        related_name="projects",
        verbose_name="frente",
    )
    title = models.CharField("título", max_length=120)
    slug = models.SlugField("slug", max_length=140, unique=True, blank=True)
    category = models.CharField("categoria", max_length=80)
    summary = models.CharField("resumo", max_length=240)
    challenge = models.TextField("desafio")
    solution = models.TextField("solução")
    deliverables = models.CharField(
        "entregáveis",
        max_length=220,
        help_text="Separe itens com vírgulas.",
    )
    image = models.ImageField(
        "imagem de capa",
        upload_to="projects/%Y/%m/",
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
    )
    image_alt = models.CharField(
        "texto alternativo da imagem",
        max_length=180,
        blank=True,
    )
    external_url = models.URLField("link externo", blank=True)
    status = models.CharField(
        "status", max_length=12, choices=Status.choices, default=Status.DRAFT
    )
    featured = models.BooleanField("projeto em destaque", default=False)
    sort_order = models.PositiveSmallIntegerField("ordem", default=0)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "case"
        verbose_name_plural = "cases"
        ordering = ("sort_order", "-featured", "-created_at")

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.status == self.Status.PUBLISHED and not self.front_id:
            raise ValidationError(
                {"front": "Selecione a frente antes de publicar este case."}
            )
        if self.image and not self.image_alt.strip():
            raise ValidationError(
                {"image_alt": "Descreva a imagem para torná-la acessível."}
            )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "projeto"
            candidate = base_slug
            suffix = 2
            while Project.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                candidate = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})

    @property
    def deliverables_list(self):
        return [item.strip() for item in self.deliverables.split(",") if item.strip()]


class ContactMessage(models.Model):
    class ProjectType(models.TextChoices):
        WEBSITE = "website", "Site ou e-commerce"
        SYSTEM = "system", "Sistema ou aplicativo"
        DATA = "data", "BI e dados"
        AUTOMATION = "automation", "Automação e integrações"
        BRAND = "brand", "Marketing e design"
        OTHER = "other", "Outro desafio"

    class Status(models.TextChoices):
        NEW = "new", "Nova"
        IN_PROGRESS = "in_progress", "Em atendimento"
        CLOSED = "closed", "Concluída"

    name = models.CharField("nome", max_length=120)
    email = models.EmailField("e-mail")
    company = models.CharField("empresa", max_length=120, blank=True)
    project_type = models.CharField(
        "tipo de projeto", max_length=20, choices=ProjectType.choices
    )
    message = models.TextField("mensagem", max_length=3000)
    privacy_consent = models.BooleanField("consentimento de privacidade")
    source_theme = models.CharField("tema de origem", max_length=24, blank=True)
    status = models.CharField(
        "status", max_length=16, choices=Status.choices, default=Status.NEW
    )
    created_at = models.DateTimeField("recebida em", auto_now_add=True)

    class Meta:
        verbose_name = "mensagem de contato"
        verbose_name_plural = "mensagens de contato"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} — {self.get_project_type_display()}"
