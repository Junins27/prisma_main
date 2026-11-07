# PRISMA — Identidade de marca e briefing de desenvolvimento

> **Documento de contexto para Codex / ChatGPT local**  
> Versão inicial: 1.0 — 06/11/2026  
> Status: **direção criativa proposta**, não identidade legalmente registrada nem especificação final aprovada.

## 1. Visão da empresa

**Nome de trabalho:** Prisma  
**Segmento:** soluções de tecnologia e marketing digital para empresas.  
**Serviços previstos:**
- Desenvolvimento de sites institucionais, landing pages e e-commerce.
- Desenvolvimento de aplicativos e sistemas sob medida.
- Business Intelligence (BI), dashboards e análise de dados.
- Automações e integrações entre sistemas.
- Marketing digital, design e estratégia de presença online.

**Posicionamento desejado:** empresa moderna, sofisticada e confiável, que une clareza estratégica, tecnologia, criatividade e proximidade humana. Não reduzir a marca a apenas uma agência de marketing nem a apenas uma software house.

### Conceito central

**Prisma + golden hour tecnológica**.

Um prisma revela diferentes componentes da luz: a Prisma torna ideias, informações e desafios empresariais mais claros e transforma essas perspectivas em soluções concretas. O dourado remete a iluminação, descoberta, valor e ao momento quente da *golden hour*, em contraste com interfaces de tecnologia frias ou excessivamente neon.

**Metáfora de marca:** “Um prisma não cria luz; ele revela aquilo que já existe nela.”

### Personalidade

- Premium, sem ser ostentatória.
- Tecnológica, sem parecer impessoal.
- Criativa, sem perder precisão e clareza.
- Minimalista, contemporânea, com espaço para crescer.
- Comunicação clara, objetiva e confiante; evitar jargões vazios.

## 2. Slogans e textos — opções, não definitivos

**Slogan de destaque sugerido:** “A luz que transforma.”

Outras possibilidades:
- “Luz sobre ideias. Inteligência sobre resultados.”
- “Conectando tecnologia, criatividade e resultados.”
- “Transformamos dados, tecnologia e comunicação em clareza, valor e crescimento.”

**Exemplo de headline para a home:**
> Tecnologia, inteligência e criatividade sob uma nova luz.

**Subheadline:**
> Criamos experiências digitais, sistemas e soluções orientadas por dados para transformar a forma como empresas crescem.

Não tratar essas frases como textos finais sem revisão.

## 3. Paleta oficial proposta — HEX

| Token | Nome | Hex | Uso recomendado |
| --- | --- | --- | --- |
| `--color-night` | Grafite Noturno | `#13171B` | Fundo principal, grandes áreas escuras |
| `--color-slate` | Chumbo Tecnológico | `#242A30` | Cards, menus, superfícies secundárias |
| `--color-gold` | Ouro Âmbar | `#D1A45B` | Cor principal da marca, detalhes e CTAs com texto escuro |
| `--color-sun` | Golden Hour | `#E8B967` | Destaques, halo de luz, gradientes |
| `--color-champagne` | Champagne | `#F5DEB3` | Tipografia especial, reflexos leves |
| `--color-copper` | Cobre Solar | `#B77A32` | Profundidade, transições e bordas decorativas |
| `--color-ivory` | Branco Quente | `#F7F4EE` | Texto principal em fundo escuro e seções claras |

**Proporção visual indicativa:** 60% grafite, 20% chumbo e 20% distribuídos entre dourado, champagne e branco quente. Não é regra matemática rígida.

### Gradiente de assinatura

```css
background: linear-gradient(
  110deg,
  #B77A32 0%,
  #D1A45B 35%,
  #F5DEB3 65%,
  #E8B967 100%
);
```

Use com moderação, em detalhes como linhas de destaque, brilho do símbolo, elementos decorativos e componentes selecionados. Evitar páginas inteiras cobertas de gradiente dourado.

### Tokens CSS iniciais

```css
:root {
  --color-night: #13171B;
  --color-slate: #242A30;
  --color-gold: #D1A45B;
  --color-sun: #E8B967;
  --color-champagne: #F5DEB3;
  --color-copper: #B77A32;
  --color-ivory: #F7F4EE;

  --color-text: var(--color-ivory);
  --color-text-muted: #B6B2AA; /* auxiliar, a validar */
  --color-surface: var(--color-night);
  --color-surface-raised: var(--color-slate);
  --color-accent: var(--color-gold);

  --gradient-golden-hour: linear-gradient(
    110deg,
    #B77A32 0%,
    #D1A45B 35%,
    #F5DEB3 65%,
    #E8B967 100%
  );
}
```

## 4. Direção de arte

### Sensação visual

**Golden hour tecnológico**: atmosfera noturna elegante com uma iluminação dourada suave atravessando as superfícies. Misturar brilho âmbar, vidro translúcido e linhas geométricas refinadas, sem exagerar no efeito futurista.

**Referências abstratas:** luz refratada, prismas geométricos, raios solares baixos no horizonte, vidro fosco, reflexos quentes, linhas de dados e grids discretos.

### Logo — exploração inicial, NÃO logo final

- Palavra **PRISMA** em caixa alta ou marca tipográfica minimalista.
- Símbolo baseado em prisma triangular ou facetas geométricas que refratam um feixe de luz.
- Dourado champagne/âmbar aplicado sutilmente sobre grafite escuro.
- Testar também versão monocromática e versão reduzida para favicon.
- Evitar efeito 3D pesado, ouro excessivamente metálico ou estética de joalheria.
- O símbolo e a marca nominal vistos na conversa foram **esboços conceituais**, não arquivos vetoriais aprovados.

### Tipografia — sugestões para testar

- **Títulos:** Manrope, Sora ou Plus Jakarta Sans.
- **Texto corrido:** Inter ou Manrope.
- **Detalhes técnicos:** JetBrains Mono, apenas em microtextos/etiquetas quando fizer sentido.

Escolher fontes com licença adequada e carregar com boa performance. Não há uma fonte oficialmente escolhida ainda.

### Componentes visuais

- Header limpo, fundo escuro e navegação simples.
- Hero com título grande, contraste alto e iluminação dourada abstrata.
- Cards em chumbo com bordas finas e brilho suave no hover.
- CTA primário em Ouro Âmbar, com **texto escuro**.
- CTA secundário em contorno discreto ou botão textual.
- Ícones de traço fino, consistentes.
- Microinterações delicadas; respeitar `prefers-reduced-motion`.
- Utilizar bastante espaço em branco/negativo.

### Acessibilidade

- Garantir contraste WCAG AA para os textos reais usados na interface.
- Não pressupor que texto dourado pequeno sobre fundo claro seja legível.
- Verificar também o contraste de texto em dourado sobre grafite antes do uso; não confiar apenas na percepção visual.
- Estados de foco por teclado visíveis, sem depender exclusivamente da cor.
- Layout responsivo, labels acessíveis, imagens com `alt` significativo.

## 5. Direção para a primeira versão do site

**Objetivo do MVP:** apresentar marca, serviços e proposta de valor, captar contatos e sustentar percepção premium. Não assumir necessidade de e-commerce ou dashboard do cliente dentro do site institucional inicial.

### Estrutura sugerida

1. **Home / Hero:** headline, subtítulo, botão “Conversar sobre um projeto”, visual com prisma e luz dourada.
2. **O que fazemos:** cards para Desenvolvimento Web, Sistemas & Apps, BI & Dados, Marketing & Design, Automação & Integrações.
3. **Por que Prisma:** clareza, estratégia, integração entre design e engenharia, soluções sob medida.
4. **Processo:** entender → planejar → construir → evoluir.
5. **Projetos / cases:** placeholders explicitamente marcados até existirem cases autorizados; **não inventar clientes, números ou depoimentos**.
6. **Contato:** formulário simples com consentimento de privacidade, validação, antispam e canais reais a preencher.
7. **Rodapé:** contatos, dados legais e links de privacidade quando disponíveis.

### Diretrizes de conteúdo

- Idioma inicial: português do Brasil.
- Textos objetivos, sem promessas de resultado não comprovadas.
- Evitar frases genéricas como “revolucionamos o mercado” sem evidência.
- Destacar entregáveis de negócio: clareza dos indicadores, melhor presença digital, sistemas eficientes e experiências de uso.

## 6. Diretrizes técnicas para Codex

A stack ainda **não foi decidida para este projeto**. Antes de programar, verificar o repositório e seguir o ecossistema existente. Se o repositório estiver vazio, propor uma arquitetura simples, explicando os trade-offs. Uma opção razoável para um site institucional é HTML/CSS/JavaScript ou React/Vite; usar Django caso haja necessidade real de backend, formulário persistido, painel administrativo ou integrações do servidor.

### Critérios de implementação

- Código legível, componentes reutilizáveis e organização clara.
- Centralizar cores e gradientes nos tokens CSS.
- Layout responsivo (mobile-first) e navegação acessível.
- Otimizar fontes, imagens, animações e métricas web vitals.
- SEO básico (title, description, heading hierarchy, OG tags e sitemap quando pertinente).
- Formulário funcional apenas quando houver integração definida; caso contrário, marcar explicitamente como protótipo, sem simular envio bem-sucedido.
- Nunca colocar credenciais, tokens ou chaves privadas no frontend.
- Não presumir domínio, arrobas sociais, CNPJ ou registro de marca.
- Não comprar domínio, implantar em produção nem criar serviços pagos sem autorização.

### Sequência recomendada de trabalho

1. Ler este briefing e examinar o projeto local.
2. Propor estrutura de arquivos e stack escolhida, com justificativa curta.
3. Implementar tokens, tipografia e componentes básicos da identidade.
4. Implementar a landing page com conteúdo editável e responsividade.
5. Testar build, acessibilidade, desempenho e estados de hover/foco.
6. Registrar em README as instruções de instalação, execução e personalização.
7. Solicitar aprovação antes de produção, compra de domínio ou integração externa.

## 7. Prompt pronto para colar no Codex

> Leia `PRISMA_BRAND_AND_CODEX.md` como referência de marca e produto. Quero iniciar o desenvolvimento do site institucional da Prisma, empresa de marketing e soluções tecnológicas, com a estética “golden hour tecnológico”. Inspecione este repositório; se estiver vazio, sugira uma stack simples e implemente uma primeira versão funcional da landing page responsiva. Use rigorosamente a paleta do briefing, com grafite profundo e dourado usado como iluminação, preserve acessibilidade, mantenha código organizado e não invente clientes ou informações comerciais. Ao final, indique como executar localmente, o que foi implementado e quais informações ainda preciso definir.

## 8. Pendências antes de lançar a marca

- **Disponibilidade do nome “Prisma”**: pesquisar conflitos de marca no INPI, especialmente nas classes pertinentes, idealmente com orientação profissional.
- **Domínio:** verificar a disponibilidade do endereço desejado no Registro.br e em outros TLDs aplicáveis.
- **Redes sociais:** verificar handles relevantes.
- **Identidade final:** decidir logo vetorial, tipografia definitiva, slogan e versões claro/escuro.
- **Comercial:** definir serviços, planos, cases, contatos e informações legais reais.
- **Privacidade:** adequar formulário de contato e política de tratamento de dados à realidade operacional.

---

**Resumo de uma linha:** Prisma é uma marca tecnológica e criativa de posicionamento premium, com base grafite e iluminação dourada inspirada na golden hour — luz como metáfora para revelar perspectivas, dar clareza aos dados e transformar ideias em soluções.
