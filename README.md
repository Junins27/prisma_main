# Prisma — Cloudflare Pages

Versão estática do site institucional da Prisma, preparada para deploy direto no **Cloudflare Pages**. Mantém a identidade visual Golden Hour e Solar Editorial, as frentes de Marketing e Tecnologia, o portfólio, páginas de case e o painel editorial personalizado.

## Estrutura de deploy

- `dist/`: diretório estático publicado pelo Cloudflare. Contém `index.html`, CSS, JavaScript, ícone e páginas públicas.
- `functions/api/`: Cloudflare Pages Functions que persistem cases e mensagens de contato em D1.
- `dist/painel/`: painel editorial visual para criar e editar cases sem Django Admin.

## Publicar no Cloudflare

Na tela de criação do projeto, conecte este repositório GitHub e use:

| Campo | Valor |
| --- | --- |
| Framework preset | `None` |
| Branch de produção | `master` |
| Build command | `exit 0` |
| Build output directory | `dist` |

O arquivo `dist/index.html` é entregue diretamente, eliminando o erro de diretório estático ausente.

Este repositório também declara `wrangler.jsonc`, com `assets.directory` apontando para `./dist`. Portanto, se o projeto tiver sido criado no modo **Workers** (em vez de Pages), o deploy automático também reconhece os arquivos estáticos e mantém a API no mesmo Worker.

### Ativar painel, cases, galeria e formulário de contato

As páginas públicas funcionam sem configuração adicional. Para que o painel e o formulário gravem dados de forma persistente:

1. No Cloudflare, crie um banco D1, por exemplo `prisma-production`.
2. Em **Workers & Pages > seu projeto > Settings > Bindings**, adicione esse banco com o nome da variável `PRISMA_DB`.
3. Crie um bucket **R2** (por exemplo, `prisma-media`) e, em **Settings > Bindings**, vincule-o como **R2 bucket** com o nome da variável `PRISMA_MEDIA`.
4. Em **Settings > Variables and Secrets**, crie os segredos de produção e preview:
   - `ADMIN_PASSWORD`: senha da equipe editorial;
   - `ADMIN_SESSION_SECRET`: texto aleatório, longo e exclusivo para assinar as sessões.
5. Faça um novo deploy. As tabelas de cases e contatos são criadas automaticamente no primeiro acesso.

O painel fica em `/painel/`. Cada case aceita até cinco imagens (JPG, PNG, WebP ou AVIF), de até 8 MB por arquivo. Elas são armazenadas no R2 e exibidas como uma galeria com rolagem. Para cada imagem, o editor permite mostrar a imagem inteira ou preencher o quadro, além de ajustar zoom e ponto focal horizontal/vertical sem alterar o arquivo original. O menu **Dados de contato** permite publicar e atualizar e-mail, telefone, WhatsApp, disponibilidade, localização, Instagram e LinkedIn na página inicial. As credenciais nunca são colocadas no repositório: elas ficam exclusivamente nos Secrets do Cloudflare.

## Rotas públicas

- `/` — site institucional;
- `/tema/golden-hour/` — Golden Hour;
- `/tema/solar-editorial/` — Solar Editorial;
- `/frentes/marketing/` e `/frentes/tecnologia/` — frentes principais;
- `/case.html?slug=<slug>` — case publicado;
- `/painel/` — painel editorial.

## Desenvolvimento local

Para verificar apenas a interface estática:

```powershell
python -m http.server 8000 --directory dist
```

Para executar também Pages Functions e D1 localmente, instale Wrangler e use:

```powershell
npx wrangler pages dev dist --d1 PRISMA_DB
```

Nenhum cliente, resultado ou case fictício foi incluído. O portfólio permanece pronto para receber apenas trabalhos autorizados.
