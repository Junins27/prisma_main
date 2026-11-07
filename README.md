# Prisma — site institucional e portfólio em Django

Sistema institucional e de portfólio criado a partir de `PRISMA_BRAND_AND_CODEX.md`. A mesma estrutura de conteúdo oferece duas versões visuais completas:

- **Golden Hour** — grafite e iluminação âmbar, baseada na paleta principal do briefing.
- **Solar Editorial** — creme, amarelo, cinzas e carvão, baseada na paleta anexada.

As versões podem ser trocadas no cabeçalho. A preferência fica salva no navegador e também possui URLs diretas:

- `/tema/golden-hour/`
- `/tema/solar-editorial/`

## O que está implementado

- landing page responsiva em português do Brasil;
- navegação acessível, foco visível e suporte a `prefers-reduced-motion`;
- tokens CSS centralizados para os dois temas;
- duas frentes de negócio em destaque: **Marketing** e **Tecnologia**;
- páginas próprias para cada frente, com serviços e cases filtrados;
- hero, serviços, diferenciais, processo, portfólio e contato editáveis pelo painel;
- projetos cadastráveis no Django Admin, vinculados a uma frente, com capa, status, destaque e ordenação;
- página individual para cada projeto publicado;
- placeholders honestos enquanto não existem cases autorizados;
- formulário de contato persistido no SQLite, com validação, consentimento e honeypot;
- SEO básico com metadados, `sitemap.xml` e `robots.txt`, incluindo as páginas das frentes;
- testes automatizados para temas, frentes, conteúdo, projetos, formulário, painel e sitemap.

## Executar localmente

Requer Python 3.11 ou mais recente.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abra [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### macOS ou Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Painel editorial

Crie o primeiro usuário responsável pelo conteúdo:

```powershell
python manage.py createsuperuser
```

Depois acesse [http://127.0.0.1:8000/painel/](http://127.0.0.1:8000/painel/). Usuários não autenticados são encaminhados para `/painel/entrar/`.

Esse é o fluxo visual principal para a equipe editorial. O dashboard reúne busca e filtros por frente e status, apresenta os cases existentes e oferece atalhos para criar ou editar conteúdo conforme as permissões do usuário.

No painel é possível:

- localizar cases por texto, frente ou status;
- criar um case já vinculado a **Marketing** ou **Tecnologia**;
- editar conteúdo, mídia, ordem, destaque e estado de publicação de um case.

O acesso exige uma conta ativa marcada como integrante da equipe (`is_staff`). Além disso, cada ação respeita as permissões do Django:

- `view_project` permite abrir o dashboard e consultar os cases;
- `add_project` permite criar cases;
- `change_project` permite editar cases.

O botão de sair envia uma requisição `POST`; abrir `/painel/sair/` diretamente não encerra a sessão.

### Retaguarda do Django

O endereço [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) continua disponível como retaguarda para superusuários administrarem contas, grupos, permissões e configurações avançadas. Para o trabalho editorial cotidiano, use `/painel/`.

Na retaguarda também permanecem disponíveis:

- **Conteúdo do site**: textos globais da página inicial;
- **Frentes de negócio**: apresentação de Marketing e Tecnologia;
- **Serviços**: serviços, visibilidade e ordenação de cada frente;
- **Mensagens de contato**: contatos recebidos e status do atendimento.

As páginas públicas das frentes ficam disponíveis em:

- `/frentes/marketing/`
- `/frentes/tecnologia/`

Cadastre somente cases e imagens autorizados. Enquanto um case estiver em **Rascunho**, ele não aparece na página inicial, na página da frente, na página individual nem no sitemap. Revise todo o conteúdo antes de mudar o status para **Publicado**.

### Fluxo recomendado para publicar um case

1. Confirme na retaguarda que a frente e os serviços relacionados estão corretos.
2. Crie o projeto como **Rascunho** e preencha desafio, solução, entregáveis e texto alternativo da imagem.
3. Use a página pública da frente para revisar o contexto em que o case aparecerá.
4. Altere o status para **Publicado** apenas depois da aprovação.

## Verificações

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py collectstatic --noinput
```

Depois de alterar modelos ou receber uma atualização do projeto, aplique as migrações antes de abrir o painel:

```powershell
python manage.py migrate
```

## Configuração de ambiente

Em desenvolvimento, as configurações padrão funcionam sem arquivo adicional. Para um ambiente publicado, defina variáveis de ambiente antes de iniciar o servidor:

| Variável | Finalidade |
| --- | --- |
| `DJANGO_SECRET_KEY` | chave longa e secreta da aplicação |
| `DJANGO_DEBUG=0` | desativa o modo de desenvolvimento |
| `DJANGO_ALLOWED_HOSTS` | hosts separados por vírgula |
| `DJANGO_SECURE=1` | ativa redirecionamento HTTPS e cookies seguros |
| `DJANGO_HSTS_SECONDS` | ativa HSTS gradualmente; comece com um valor curto |
| `DJANGO_HSTS_INCLUDE_SUBDOMAINS=1` | inclui subdomínios no HSTS somente após validação |
| `DJANGO_HSTS_PRELOAD=1` | opt-in de preload somente após atender seus requisitos |
| `DJANGO_BEHIND_HTTPS_PROXY=1` | confia em `X-Forwarded-Proto` de um proxy controlado |
| `CONTACT_RATE_LIMIT` | tentativas de contato por janela; padrão `8` |
| `CONTACT_RATE_WINDOW` | duração da janela em segundos; padrão `600` |

Este projeto usa o servidor de desenvolvimento do Django. Antes de publicar, escolha um servidor WSGI/ASGI, armazenamento persistente de mídia, rotina de backup e banco adequados ao ambiente. Configure um cache compartilhado e limite de requisições/corpo HTTP no proxy ou na plataforma; o limite interno do formulário é apenas uma camada complementar.

## Pontos ainda pendentes

- contatos e horários comerciais reais;
- domínio, dados legais e política de privacidade definitiva;
- cases, imagens e resultados com autorização de publicação;
- logo vetorial e tipografia finais;
- canal de notificação para novas mensagens (hoje elas ficam registradas no Admin);
- revisão jurídica de marca e privacidade antes do lançamento.

Nenhum cliente, depoimento, número de resultado, domínio ou informação legal foi inventado nesta versão.
