from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import BusinessFront, ContactMessage, Project


class StaffAuthenticationForm(AuthenticationForm):
    """Autenticação do painel editorial, restrita à equipe interna."""

    error_messages = {
        **AuthenticationForm.error_messages,
        "not_staff": "Esta conta não possui acesso ao painel editorial.",
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "panel-control",
                "autocomplete": "username",
                "placeholder": "Seu usuário",
                "autofocus": True,
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "panel-control",
                "autocomplete": "current-password",
                "placeholder": "Sua senha",
            }
        )

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise forms.ValidationError(
                self.error_messages["not_staff"],
                code="not_staff",
            )


class ProjectForm(forms.ModelForm):
    """Edição de cases sem expor o slug técnico ao editor."""

    class Meta:
        model = Project
        fields = (
            "front",
            "title",
            "category",
            "summary",
            "challenge",
            "solution",
            "deliverables",
            "image",
            "image_alt",
            "external_url",
            "status",
            "featured",
            "sort_order",
        )
        widgets = {
            "front": forms.Select(attrs={"class": "panel-control panel-select"}),
            "title": forms.TextInput(
                attrs={
                    "class": "panel-control",
                    "placeholder": "Nome do case",
                    "autocomplete": "off",
                }
            ),
            "category": forms.TextInput(
                attrs={
                    "class": "panel-control",
                    "placeholder": "Ex.: Produto digital, Marca ou Dados",
                }
            ),
            "summary": forms.Textarea(
                attrs={
                    "class": "panel-control",
                    "rows": 3,
                    "placeholder": "Resumo curto para os cards e buscadores",
                }
            ),
            "challenge": forms.Textarea(
                attrs={
                    "class": "panel-control",
                    "rows": 6,
                    "placeholder": "Contexto e desafio real do projeto",
                }
            ),
            "solution": forms.Textarea(
                attrs={
                    "class": "panel-control",
                    "rows": 6,
                    "placeholder": "Como a Prisma abordou o desafio",
                }
            ),
            "deliverables": forms.TextInput(
                attrs={
                    "class": "panel-control",
                    "placeholder": "UX, Desenvolvimento, Integração",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "panel-control panel-file",
                    "accept": ".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp",
                }
            ),
            "image_alt": forms.TextInput(
                attrs={
                    "class": "panel-control",
                    "placeholder": "Descrição objetiva da imagem",
                }
            ),
            "external_url": forms.URLInput(
                attrs={
                    "class": "panel-control",
                    "placeholder": "https://",
                    "inputmode": "url",
                }
            ),
            "status": forms.Select(attrs={"class": "panel-control panel-select"}),
            "featured": forms.CheckboxInput(attrs={"class": "panel-checkbox"}),
            "sort_order": forms.NumberInput(
                attrs={"class": "panel-control", "min": 0, "inputmode": "numeric"}
            ),
        }
        help_texts = {
            "front": "Escolha entre Marketing e Tecnologia.",
            "deliverables": "Separe cada entregável com vírgulas.",
            "image": "Formatos permitidos: JPG, PNG ou WebP.",
            "image_alt": "Obrigatório quando uma imagem de capa for usada.",
            "featured": "Cases em destaque recebem maior ênfase na listagem.",
            "sort_order": "Números menores aparecem primeiro.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["front"].queryset = BusinessFront.objects.order_by(
            "sort_order", "title"
        )
        self.fields["front"].empty_label = "Selecione uma frente"


class ContactForm(forms.ModelForm):
    website = forms.CharField(
        required=False,
        label="Não preencha este campo",
        widget=forms.TextInput(
            attrs={
                "tabindex": "-1",
                "autocomplete": "off",
                "aria-hidden": "true",
            }
        ),
    )

    class Meta:
        model = ContactMessage
        fields = (
            "name",
            "email",
            "company",
            "project_type",
            "message",
            "privacy_consent",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"autocomplete": "name", "placeholder": "Seu nome"}
            ),
            "email": forms.EmailInput(
                attrs={"autocomplete": "email", "placeholder": "voce@empresa.com"}
            ),
            "company": forms.TextInput(
                attrs={
                    "autocomplete": "organization",
                    "placeholder": "Nome da empresa (opcional)",
                }
            ),
            "project_type": forms.Select(),
            "message": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "Conte um pouco sobre o contexto, o desafio e o que você espera construir.",
                }
            ),
            "privacy_consent": forms.CheckboxInput(),
        }
        labels = {
            "name": "Nome",
            "email": "E-mail",
            "company": "Empresa",
            "project_type": "Como podemos ajudar?",
            "message": "Sobre o projeto",
            "privacy_consent": (
                "Concordo que meus dados sejam usados somente para responder a esta mensagem."
            ),
        }
        error_messages = {
            "name": {"required": "Informe seu nome."},
            "email": {
                "required": "Informe seu e-mail.",
                "invalid": "Informe um e-mail válido.",
            },
            "project_type": {"required": "Selecione o tipo de projeto."},
            "message": {"required": "Conte um pouco sobre o projeto."},
            "privacy_consent": {
                "required": "É necessário aceitar o uso dos dados para enviar."
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project_type"].choices = [
            ("", "Selecione uma opção"),
            *ContactMessage.ProjectType.choices,
        ]

    def clean_website(self):
        value = self.cleaned_data.get("website", "")
        if value:
            raise forms.ValidationError("Não foi possível validar o envio.")
        return value

    def clean_privacy_consent(self):
        consent = self.cleaned_data.get("privacy_consent")
        if not consent:
            raise forms.ValidationError(
                "É necessário aceitar o uso dos dados para enviar."
            )
        return consent
