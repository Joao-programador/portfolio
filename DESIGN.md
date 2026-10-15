# Direção de Design & Identidade Visual (DESIGN.md)
**Projeto:** Portfólio Executivo de Dados e Business Intelligence — João Barbosa  
**Público-Alvo:** Liderança C-Level, Secretários, Diretores de Estatais/Concessões e Gestores de Negócio  
**Dial Declarado:** ENERGY 2 / RHYTHM 2 / MOTION 2

---

## 1. Identidade & Conceito
Um portfólio editorial de alto impacto para um Engenheiro e Analista de Dados com atuação estratégica em parcerias públicas, desestatizações e modelagem dimensional em São Paulo. O design transmite **rigor estatístico, auditoria confiável e clareza cognitiva**, fugindo deliberadamente de templates genéricos de SaaS.

---

## 2. Dials de Vivacidade (Liveliness Toolkit)
- **ENERGY: 2 (Balanced)** — Postura executiva segura e sóbria. O ponto focal de boas-vindas é o retrato editorial com recorte de estúdio e tipografia monumental em Oswald e Playfair, sem elementos infantis ou ruídos circenses.
- **RHYTHM: 2 (Consistente com Quebras Estratégicas)** — A página alterna dinamicamente o ritmo de leitura:
  1. *Hero* com status bar e retrato com profundidade.
  2. *Marquee* sutil com logos de stack tecnológica.
  3. *Biografia Institucional* (Trajetória na SPP, foco em controle e auditoria).
  4. *Carrossel 3D Interativo* com dashboards reais encapsulados.
  5. *Cena 3D Three.js* ("Do Caos Operacional à Clareza Executiva") com cubos que convergem de dispersão para matriz estruturada via ScrollTrigger.
  6. *Capacidades Técnicas* (Arquitetura relacional, governança e Star Schema).
  7. *Diagnóstico Interativo de Maturidade em Dados* (4 perguntas com pontuação e recomendação dinâmica).
  8. *Footer Monolítico Executivo*.
- **MOTION: 2 (Transições Suaves & Intencionais)** — Animações com ScrollTrigger discretas (`gs-reveal`, `gs-scroll`), expansão de modal com View Transitions, cena 3D interativa scrubada pelo scroll e respeito estrito a `prefers-reduced-motion`.

---

## 3. Paleta de Cores & Superfícies
- **Fundo Principal:** `#0A0A0C` (Dark Mode profundo de alto contraste, livre de lavagens acinzentadas fracas).
- **Superfícies de Seção:** `#0E0E12` e `#070709`.
- **Cartões e Painéis Elevados:** `#121217` e `#141419` com bordas sutis em `white/10` a `white/15`.
- **Tipografia:**
  - Títulos e Números: `text-white` (contraste superior a 15:1 sobre o fundo escuro).
  - Texto de Destaque: `text-zinc-200` e `text-zinc-300`.
  - Metadados e Rótulos Técnicos: `text-zinc-400` e `text-zinc-500`.
- **Acento Estratégico (1 único acento de KPI):** `emerald-400` (`#34d399`) para indicar dados vivos, status ativo e métricas de integridade.

---

## 4. Tipografia Editorial
- **Oswald (Google Fonts):** Letra condensada, firme e arquitetural para títulos monumentais (`H1`, `H2`, `H3`).
- **Playfair Display (Google Fonts):** Itálico sofisticado para sublinhar sofisticação editorial e humanidade nas aberturas.
- **JetBrains Mono (Google Fonts):** Fonte monoespaçada de precisão técnica para índices, badges de telemetria e metadados de pipeline.

---

## 5. Padrões de Artesanato (Craftsmanship Standards)
- **Zero Em Dashes:** Banimento estrito do caractere `—`. Uso de pontuação natural (vírgula, dois-pontos, parênteses ou `//`).
- **Zero Falsificação:** Nenhuma métrica inflada, nenhum cliente fictício, nenhum depoimento fabricado por IA. Demonstrações analíticas rotuladas honestamente como *"Dados fictícios para demonstração"*.
- **Navegação Real:** Todos os links (`#about`, `#work`, `#philosophy`, `#capabilities`, `#diagnostico`, `mailto:`) apontam para seções e ações existentes.
- **Acessibilidade Total (WCAG AA):** Foco por teclado (`Tab`, anéis visíveis em botões transparentes), alvos de toque maiores que 44px e contraste testado.
- **Ecossistema Python Nativo:** FastHTML + Tailwind CSS (CDN) + HTMX + Alpine.js (CDN) + Three.js (CDN). Zero dependência de Node.js/NPM.
