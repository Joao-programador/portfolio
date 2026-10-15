from fasthtml.common import *
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
import json
import urllib.parse
from pathlib import Path

# --- DADOS REAIS DE CONTATO ---
LINKEDIN_URL = "https://www.linkedin.com/in/joaobarbosamf"
GITHUB_URL = "https://github.com/Joao-programador"
EMAIL_CONTACT = "joaogoncalves07082022@gmail.com"

_app, rt = fast_app(
    htmx=False,
    surreal=False,
    pico=False,
    middleware=[Middleware(GZipMiddleware, minimum_size=500)],
    htmlkw={'lang': 'pt-BR'},
    hdrs=(
        Title("João Barbosa | Arquitetura de Dados & Inteligência Executiva (BI)"),
        Meta(name="description", content="Portfólio executivo de João Barbosa: Arquitetura de Dados, Analytics, Engenharia e Dashboards para decisões estratégicas."),
        Meta(property="og:title", content="João Barbosa | Portfólio de Dados & BI"),
        Meta(property="og:description", content="Arquitetura de Dados, Analytics e Visualização para Decisões C-Level."),
        Meta(property="og:type", content="website"),
        
        # Scripts essenciais
        Script(src="https://cdn.tailwindcss.com/3.4.17"),
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js", defer=True),
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js", defer=True),
        Script(src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.3/dist/cdn.min.js", defer=True),

        # Script do Carrossel e Modal com Acessibilidade
        Script(NotStr("""
window.featureCarousel = function() {
    return {
        step: 0,
        prevStep: 0,
        isPaused: false,
        isModalOpen: false,
        selectedFeature: null,
        iframeLoaded: false,
        len: 3,
        itemHeight: 74,
        intervalId: null,
        init() {
            const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
            if (!prefersReducedMotion) {
                this.intervalId = setInterval(() => {
                    if (!this.isPaused && !this.isModalOpen) this.go(1);
                }, 4000);
            }
        },
        get currentIndex() {
            return ((this.step % this.len) + this.len) % this.len;
        },
        wrap(min, max, v) {
            const rangeSize = max - min;
            return ((((v - min) % rangeSize) + rangeSize) % rangeSize) + min;
        },
        go(n) {
            this.prevStep = this.step;
            this.step += n;
        },
        dist(i, s) {
            return this.wrap(-this.len / 2, this.len / 2, i - (((s % this.len) + this.len) % this.len));
        },
        getChipStyle(i) {
            const d = this.dist(i, this.step);
            const prevD = this.dist(i, this.prevStep);
            const jumped = Math.abs(d - prevD) > 1;
            const tr = jumped
                ? 'none'
                : 'transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
            return `transform: translateY(${d * this.itemHeight}px); opacity: ${1 - Math.abs(d) * 0.35}; height: ${this.itemHeight - 8}px; transition: ${tr};`;
        },
        getCardStatus(index) {
            const diff = index - this.currentIndex;
            let normalizedDiff = diff;
            if (diff > this.len / 2) normalizedDiff -= this.len;
            if (diff < -this.len / 2) normalizedDiff += this.len;
            
            if (normalizedDiff === 0) return 'active';
            if (normalizedDiff === -1) return 'prev';
            if (normalizedDiff === 1) return 'next';
            return 'hidden';
        },
        getCardStyle(index) {
            if (this.isModalOpen && this.selectedFeature === index) {
                return "position: fixed; inset: 1.5rem; z-index: 100; transform: none; opacity: 1; pointer-events: auto; view-transition-name: feature-card;";
            }

            const status = this.getCardStatus(index);
            if (status === 'active') {
                let s = "position: absolute; inset: 0; transform: translateX(0px) scale(1) rotate(0deg); opacity: 1; z-index: 20; pointer-events: auto;";
                if (!this.isModalOpen) s += " view-transition-name: feature-card;";
                return s;
            }
            if (status === 'prev') return "position: absolute; inset: 0; transform: translateX(-110px) scale(0.88) rotate(-2deg); opacity: 0.35; z-index: 10; pointer-events: none;";
            if (status === 'next') return "position: absolute; inset: 0; transform: translateX(110px) scale(0.88) rotate(2deg); opacity: 0.35; z-index: 10; pointer-events: none;";
            
            return "position: absolute; inset: 0; transform: translateX(0px) scale(0.70) rotate(0deg); opacity: 0; z-index: 0; pointer-events: none;";
        },
        handleChipClick(index) {
            const diff = (index - this.currentIndex + this.len) % this.len;
            if (diff > 0) this.go(diff);
        },
        async openModal(index) {
            this.iframeLoaded = false;
            // Fallback de segurança para garantir a resolução do estado de loading
            setTimeout(() => { if (this.isModalOpen) this.iframeLoaded = true; }, 500);
            if (!document.startViewTransition) {
                this.selectedFeature = index;
                this.isModalOpen = true;
                document.body.style.overflow = 'hidden';
                return;
            }
            document.startViewTransition(async () => {
                this.selectedFeature = index;
                this.isModalOpen = true;
                document.body.style.overflow = 'hidden';
                await this.$nextTick();
            });
        },
        async closeModal() {
            if (!document.startViewTransition) {
                this.isModalOpen = false;
                setTimeout(() => this.selectedFeature = null, 300);
                document.body.style.overflow = 'unset';
                return;
            }
            document.startViewTransition(async () => {
                this.isModalOpen = false;
                this.selectedFeature = null;
                document.body.style.overflow = 'unset';
                await this.$nextTick();
            });
        }
    }
}
""")),

        Link(rel="preconnect", href="https://fonts.googleapis.com"),
        Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        Link(href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Oswald:wght@500;600;700&family=Playfair+Display:ital,wght@1,400;1,600&display=swap", rel="stylesheet"),
        Style("""
            html {
                scrollbar-gutter: stable;
                scroll-behavior: smooth;
            }
            body { 
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
                background-color: #0A0A0C; 
                color: #F4F4F6; 
                overflow-x: hidden; 
            }
            .font-playfair { font-family: 'Playfair Display', Georgia, serif; }
            .font-oswald { font-family: 'Oswald', sans-serif; }
            .font-mono { font-family: 'JetBrains Mono', monospace; }
            
            .glass-pill {
                background: rgba(22, 22, 28, 0.85);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.12);
            }

            .studio-spotlight {
                background: radial-gradient(circle at 50% 45%, rgba(255, 255, 255, 0.08) 0%, rgba(20, 20, 26, 0.35) 45%, rgba(10, 10, 12, 1) 75%);
            }
            
            [x-cloak] { display: none !important; }
            
            @keyframes marquee {
                0% { transform: translateX(0%); }
                100% { transform: translateX(-50%); }
            }
            .animate-marquee {
                display: flex;
                width: max-content;
                animation: marquee 35s linear infinite;
            }
            .animate-marquee:hover {
                animation-play-state: paused;
            }
            .mask-marquee {
                mask-image: linear-gradient(to right, transparent, black 12%, black 88%, transparent);
                -webkit-mask-image: linear-gradient(to right, transparent, black 12%, black 88%, transparent);
            }

            @media (prefers-reduced-motion: reduce) {
                *, ::before, ::after {
                    animation-duration: 0.01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: 0.01ms !important;
                    scroll-behavior: auto !important;
                }
            }
        """)
    ),
    live=False
)

# Exportação direta de nível superior exigida pelo construtor @vercel/python
app = _app
handler = app
application = app

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/Projetos", StaticFiles(directory=str(BASE_DIR / "Projetos"), html=True), name="projetos")

FEATURES = [
  {
      "id": "prazos",
      "label": "Análise de Prazos & SLAs",
      "tag": "Gestão Estratégica",
      "icon": '<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
      "image": "/static/dashboard-print.png",
      "iframe_src": "/Projetos/Análise de Prazos - Ficticio.html",
      "description": "Dashboard executivo interativo de monitoramento de prazos, curvas de atraso e conformidade de entregas contratuais."
  },
  {
      "id": "mapa",
      "label": "Mapeamento Geoespacial SP",
      "tag": "GIS & Mobilidade",
      "icon": '<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>',
      "image": "/static/mapa-estacionamentos-print.png",
      "iframe_src": "/Projetos/Mapa de Estacionamentos/index.html",
      "description": "Análise geoespacial e clustering de edifícios-garagem na região central de São Paulo com camadas vetoriais de densidade urbana."
  },
  {
      "id": "performance",
      "label": "Gestão Operacional (SGO)",
      "tag": "Eficiência Estratégica",
      "icon": '<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>',
      "image": "/static/performance-operacional-print.png",
      "iframe_src": "/Projetos/Painel de Performance Operacional/index.html",
      "description": "Cockpit executivo consolidado com KPIs de produtividade, gargalos de atendimento e controle operacional."
  }
]

def FeatureCarousel():
    left_chips = []
    for i, f in enumerate(FEATURES):
        left_chips.append(
            Div(
                Button(
                    Div(
                        NotStr(f['icon']),
                        **{":class": f"`flex items-center justify-center transition-colors duration-300 ${{{i} === currentIndex ? 'text-black' : 'text-zinc-400'}}`"}
                    ),
                    Div(
                        Span(f['label'], cls="font-semibold text-xs md:text-sm tracking-tight block uppercase"),
                        Span(f['tag'], cls="text-[10px] font-mono opacity-65 block"),
                        cls="text-left"
                    ),
                    **{
                        ":class": f"`w-full flex items-center gap-3.5 px-5 md:px-6 py-3 rounded-2xl transition-all duration-500 text-left group border ${{{i} === currentIndex ? 'bg-white text-black border-white shadow-xl z-10' : 'bg-[#121217] text-zinc-300 border-white/10 hover:border-white/25 hover:text-white'}}`",
                        "@click": f"handleChipClick({i})",
                        "@mouseenter": "isPaused = true",
                        "@mouseleave": "isPaused = false",
                        "@focus": "isPaused = true",
                        "@blur": "isPaused = false",
                        "aria-label": f"Selecionar demonstração: {f['label']}"
                    }
                ),
                **{":style": f"getChipStyle({i})"},
                cls="absolute inset-x-0 flex items-center justify-center"
            )
        )
        
    backdrop = Div(
        **{
            "x-show": "isModalOpen",
            "x-transition.opacity.duration.300ms": "",
            "@click": "closeModal()",
        },
        cls="fixed inset-0 bg-black/85 backdrop-blur-md z-[90]"
    )

    right_cards = []
    for i, f in enumerate(FEATURES):
        encoded_src = urllib.parse.quote(f['iframe_src'])
        media_element = Iframe(
            **{
                "x-bind:src": f"isModalOpen && selectedFeature === {i} ? '{encoded_src}' : 'about:blank'",
                "@load": "iframeLoaded = true"
            },
            title=f"Demonstração: {f['label']}",
            cls="w-full h-full border-0 pointer-events-auto bg-[#0A0A0C]"
        )
        image_cover = Img(
            src=f['image'], 
            alt=f['label'],
            width="580",
            height="362",
            loading="lazy",
            decoding="async",
            cls="absolute inset-0 w-full h-full object-cover object-center z-[30] bg-[#121217]",
            **{
                "x-show": f"!(isModalOpen && selectedFeature === {i})",
                "x-transition.opacity.duration.300ms": "",
                ":class": f"`${{{i} === currentIndex ? 'grayscale-0 blur-0 brightness-100' : 'grayscale blur-[2px] brightness-50'}}`"
            }
        )

        # Loading Skeleton do Iframe
        loading_skeleton = Div(
            Div(
                Span(cls="size-3 rounded-full bg-emerald-400 animate-ping"),
                Span("Carregando painel analítico...", cls="text-xs font-mono text-zinc-300"),
                cls="flex items-center gap-3 bg-[#121217] px-5 py-3 rounded-xl border border-white/10 shadow-xl"
            ),
            cls="absolute inset-0 flex items-center justify-center bg-[#0A0A0C] z-[25]",
            **{"x-show": f"isModalOpen && selectedFeature === {i} && !iframeLoaded", "x-transition.opacity.duration.200ms": ""}
        )

        # Barra Superior do Modal Exclusiva
        modal_header_bar = Div(
            Div(
                H3(f['label'], cls="text-base sm:text-lg font-bold text-white tracking-tight"),
                Span("Dados fictícios para demonstração", cls="ml-3 hidden sm:inline-block text-[10px] font-mono uppercase tracking-wider px-2.5 py-1 rounded bg-white/5 border border-white/10 text-zinc-400"),
                cls="flex items-center"
            ),
            Div(
                A(
                    Span("Abrir em Nova Aba"),
                    NotStr('<svg class="w-3.5 h-3.5 ml-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>'),
                    href=f['iframe_src'],
                    target="_blank",
                    rel="noopener noreferrer",
                    cls="inline-flex items-center text-xs font-semibold text-white bg-white/10 hover:bg-white/20 border border-white/15 px-3 py-1.5 rounded-lg transition-colors mr-2 cursor-pointer"
                ),
                Button(
                    NotStr('<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>'),
                    cls="p-1.5 bg-white/10 hover:bg-white hover:text-black text-white rounded-lg border border-white/15 transition-colors cursor-pointer",
                    aria_label="Fechar demonstração",
                    **{"@click.stop": "closeModal()"}
                ),
                cls="flex items-center"
            ),
            cls="h-14 px-6 bg-[#0E0E12] border-b border-white/10 flex items-center justify-between shrink-0 z-[110]",
            **{"x-show": f"isModalOpen && selectedFeature === {i}"}
        )

        media_content = Div(
            modal_header_bar,
            Div(media_element, image_cover, loading_skeleton, cls="relative flex-1 w-full overflow-hidden"),
            cls="w-full h-full relative bg-[#121217] flex flex-col"
        )

        right_cards.append(
            Div(
                media_content,
                
                # Bottom Project Details Bar (Visível apenas no card ATIVO e fora do modal)
                Div(
                    Div(
                        Span(f"0{i + 1} • {f['label']}", cls="bg-white/10 text-zinc-200 border border-white/10 px-3 py-1 rounded-full text-[10px] md:text-[11px] font-mono uppercase tracking-wider w-fit mb-2"),
                        Span("Dados fictícios", cls="text-[10px] font-mono text-zinc-400"),
                        cls="flex items-center justify-between"
                    ),
                    Div(
                        P(f['description'], cls="text-zinc-200 font-medium text-xs md:text-sm leading-snug tracking-tight flex-1"),
                        Span("Explorar Painel", cls="hidden sm:inline-flex items-center text-xs font-semibold text-black bg-white px-3.5 py-1.5 rounded-lg shadow-sm ml-3 shrink-0 hover:bg-zinc-200 transition-colors"),
                        cls="flex items-center justify-between gap-3"
                    ),
                    cls="absolute inset-x-4 md:inset-x-6 bottom-4 md:bottom-6 p-4 md:p-5 rounded-2xl bg-[#0E0E12] border border-white/15 shadow-2xl flex flex-col justify-end z-[40]",
                    **{
                        "x-show": f"!isModalOpen && currentIndex === {i}",
                        "x-transition.opacity.duration.300ms": ""
                    }
                ),
                
                # Live Interactive Badge (Apenas no card ativo fora do modal)
                Div(
                    Div(cls="w-2 h-2 rounded-full bg-emerald-400"),
                    Span("Demonstração Interativa", cls="text-zinc-200 text-[10px] font-medium tracking-wider font-mono"),
                    cls="absolute top-5 right-5 flex items-center gap-2 z-[40] bg-[#0E0E12] px-3 py-1.5 rounded-full border border-white/10 shadow-md",
                    **{
                        "x-show": f"!isModalOpen && currentIndex === {i}",
                        "x-transition.opacity.duration.300ms": ""
                    }
                ),

                # Click Catcher acessível via teclado com foco visível
                Button(
                    cls="absolute inset-0 z-[50] cursor-pointer opacity-0 w-full h-full border-0 focus-visible:opacity-100 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-[#0A0A0C] rounded-3xl outline-none transition-all",
                    aria_label=f"Expandir demonstração interativa: {f['label']}",
                    **{
                        "x-show": f"!(isModalOpen && selectedFeature === {i})",
                        "@click": f"if ({i} === currentIndex) openModal({i})"
                    }
                ),
                
                cls="rounded-3xl overflow-hidden border border-white/15 bg-[#121217] origin-center transition-all duration-700 ease-out shadow-2xl",
                **{
                    ":style": f"getCardStyle({i})",
                    ":class": f"`${{{i} === currentIndex && !isModalOpen ? 'hover:scale-[1.01] hover:border-white/30' : ''}}`"
                }
            )
        )

    return Div(
        backdrop,
        Div(
            # Left Navigation Column
            Div(
                Div(cls="absolute inset-x-0 top-0 h-16 bg-gradient-to-b from-[#0A0A0C] via-[#0A0A0C]/80 to-transparent z-40 pointer-events-none"),
                Div(cls="absolute inset-x-0 bottom-0 h-16 bg-gradient-to-t from-[#0A0A0C] via-[#0A0A0C]/80 to-transparent z-40 pointer-events-none"),
                Div(
                    *left_chips,
                    cls="relative w-full max-w-sm h-full flex items-center justify-center z-20"
                ),
                cls="w-full lg:w-[40%] min-h-[340px] md:min-h-[420px] lg:h-full relative z-30 flex flex-col items-center justify-center overflow-hidden px-6 md:px-8 bg-[#0A0A0C]"
            ),
            # Right Interactive Showcase Stage
            Div(
                Div(
                    *right_cards,
                    cls="relative w-full max-w-[580px] aspect-[16/10] md:aspect-video flex items-center justify-center"
                ),
                # Navigation Controls (Prev / Index / Next)
                Div(
                    Button(
                        NotStr('<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>'),
                        cls="w-10 h-10 rounded-full bg-[#18181E] border border-white/15 text-zinc-300 hover:text-white hover:border-white/40 hover:bg-[#22222A] flex items-center justify-center transition-all cursor-pointer",
                        **{"@click": "go(-1); isPaused = true", "aria-label": "Projeto anterior"}
                    ),
                    Span(
                        cls="text-xs font-mono font-medium tracking-wider text-zinc-300 px-4 py-2 bg-[#18181E] rounded-full border border-white/15",
                        **{"x-text": "`0${currentIndex + 1} / 0${len}`"}
                    ),
                    Button(
                        NotStr('<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>'),
                        cls="w-10 h-10 rounded-full bg-[#18181E] border border-white/15 text-zinc-300 hover:text-white hover:border-white/40 hover:bg-[#22222A] flex items-center justify-center transition-all cursor-pointer",
                        **{"@click": "go(1); isPaused = true", "aria-label": "Próximo projeto"}
                    ),
                    cls="flex items-center gap-3 mt-8 z-30"
                ),
                cls="flex-1 min-h-[500px] md:min-h-[580px] lg:h-full relative bg-[#0E0E12] flex flex-col items-center justify-center py-12 md:py-16 px-6 md:px-10 overflow-hidden border-t lg:border-t-0 lg:border-l border-white/10"
            ),
            cls="relative overflow-hidden rounded-[2.5rem] flex flex-col lg:flex-row min-h-[580px] border border-white/15 shadow-2xl bg-[#0A0A0C]"
        ),
        **{
            "x-data": "featureCarousel()",
            "@keydown.window.escape": "closeModal()",
            "@mouseenter": "isPaused = true",
            "@mouseleave": "isPaused = false"
        },
        cls="w-full max-w-7xl mx-auto gs-scroll"
    )

DIAGNOSTICO = {
    "max": 12,
    "perguntas": [
        {"q": "Onde os dados da sua organização residem hoje?", "opcoes": [
            ["Planilhas dispersas e pastas compartilhadas", 0],
            ["Sistemas múltiplos sem integração unificada", 1],
            ["Banco de dados centralizado, mas com retrabalho manual", 2],
            ["Pipelines automatizados, catalogados e auditados", 3],
        ]},
        {"q": "Com que frequência a diretoria toma decisões baseadas em métricas auditáveis?", "opcoes": [
            ["Quase nunca / Predominância de intuição", 0],
            ["Apenas em reuniões semestrais de fechamento", 1],
            ["Mensalmente, mas os números sofrem frequentes contestações", 2],
            ["Diariamente com KPIs consolidados e governança ativa", 3],
        ]},
        {"q": "Cada indicador estratégico possui documentação formal e um responsável claro?", "opcoes": [
            ["Não existe documentação formal", 0],
            ["Apenas em métricas financeiras pontuais", 1],
            ["Na maior parte dos indicadores, com pequenas divergências", 2],
            ["Sim, com dicionário de dados formal e governança ativa", 3],
        ]},
        {"q": "Se o painel principal cair hoje, quanto tempo leva para reconstruí-lo?", "opcoes": [
            ["Dias ou semanas, dependendo de uma pessoa específica", 0],
            ["Horas intensas de retrabalho manual", 1],
            ["Minutos, por meio de rotinas semiautomatizadas", 2],
            ["Processo automatizado via infraestrutura como código", 3],
        ]},
    ],
    "niveis": [
        {"max": 3, "titulo": "Fase 1: Fundação a Construir",
         "recomendacao": "Sua operação se beneficiará de um BI Sprint para organizar fontes dispersas, eliminar retrabalho manual e publicar os primeiros cockpits executivos auditáveis."},
        {"max": 7, "titulo": "Fase 2: Base em Expansão",
         "recomendacao": "Você já possui dados relevantes. O próximo passo recomendado é consolidar a modelagem dimensional (Star Schema) e esteiras de ingestão contínua para garantir escala sem gargalos."},
        {"max": 12, "titulo": "Fase 3: Maturidade Avançada",
         "recomendacao": "Sua estrutura é sólida e madura. A evolução natural envolve observabilidade analítica de ponta a ponta, governança preditiva e redução de latência para consultas executivas."},
    ],
}

DIAG_JS = f"""
window.maturidade = () => ({{
  dados: window.MATURIDADE,
  i: 0,
  respostas: [],
  concluido: false,
  get total() {{ return this.dados.perguntas.length; }},
  get progresso() {{ return this.concluido ? 100 : Math.round((this.i / this.total) * 100); }},
  get pontos() {{ return this.respostas.reduce((a, b) => a + b, 0); }},
  get nivel() {{ return this.dados.niveis.find(n => this.pontos <= n.max) || this.dados.niveis[2]; }},
  get mailto() {{
    const corpo = `Olá João,\\n\\nRealizei o diagnóstico de maturidade no seu portfólio:\\n- Pontuação: ${{this.pontos}} / ${{this.dados.max}}\\n- Nível Diagnosticado: ${{this.nivel.titulo}}\\n\\nGostaria de conversar sobre estratégias e próximos passos analíticos para nossa operação.`;
    return 'mailto:{EMAIL_CONTACT}?subject=' + encodeURIComponent('Diagnóstico de Maturidade em Dados: ' + this.nivel.titulo)
         + '&body=' + encodeURIComponent(corpo);
  }},
  responder(p) {{
    this.respostas[this.i] = p;
    if (this.i < this.total - 1) {{
      this.i++;
    }} else {{
      this.concluido = true;
    }}
  }},
  voltar() {{
    if (this.i > 0) {{
      this.i--;
      this.concluido = false;
    }}
  }},
  reiniciar() {{
    this.i = 0;
    this.respostas = [];
    this.concluido = false;
  }},
}});
"""

TECH_LOGOS = [
    {"name": "Python", "src": "https://cdn.simpleicons.org/python/FFFFFF"},
    {"name": "PostgreSQL", "src": "https://cdn.simpleicons.org/postgresql/FFFFFF"},
    {"name": "Power BI", "src": "https://cdn.simpleicons.org/powerbi/FFFFFF"},
    {"name": "Pandas", "src": "https://cdn.simpleicons.org/pandas/FFFFFF"},
    {"name": "Git & GitHub", "src": "https://cdn.simpleicons.org/git/FFFFFF"},
    {"name": "Leaflet GIS", "src": "https://cdn.simpleicons.org/leaflet/FFFFFF"},
    {"name": "Apache ECharts", "src": "https://cdn.simpleicons.org/apacheecharts/FFFFFF"},
    {"name": "JavaScript", "src": "https://cdn.simpleicons.org/javascript/FFFFFF"},
]

def TechMarquee():
    items = []
    for logo in TECH_LOGOS * 2:
        items.append(
            Div(
                Img(src=logo["src"], alt=logo["name"], width="24", height="24", loading="lazy", decoding="async", cls="h-6 w-6 object-contain opacity-75 hover:opacity-100 transition-opacity shrink-0"),
                Span(logo["name"], cls="text-sm font-semibold tracking-wide text-zinc-400 hover:text-white transition-colors whitespace-nowrap uppercase font-mono"),
                cls="flex items-center gap-3 shrink-0 py-2 cursor-default"
            )
        )
    return Section(
        Div(
            Div(
                Div(
                    *items,
                    cls="animate-marquee flex items-center gap-12 md:gap-16 py-3"
                ),
                cls="mask-marquee w-full overflow-hidden"
            ),
            cls="max-w-7xl mx-auto px-6"
        ),
        cls="py-8 bg-[#070709] border-y border-white/10 relative z-20"
    )

def AboutSection():
    return Section(
        Div(
            Div(
                # Coluna Esquerda
                Div(
                    Span("TRAJETÓRIA & PROPÓSITO", cls="text-[11px] font-mono font-semibold tracking-[0.25em] text-zinc-400 uppercase block mb-3"),
                    H2("DADOS A SERVIÇO DE DECISÕES ESTRATÉGICAS NA MAIOR METRÓPOLE DA AMÉRICA LATINA.", 
                       cls="text-3xl md:text-4xl lg:text-[40px] font-oswald uppercase tracking-tight text-white leading-[1.18] mb-6"),
                    P("A ponte essencial entre a engenharia analítica e a tomada de decisão executiva.", 
                       cls="font-playfair italic text-xl md:text-2xl text-zinc-300 leading-snug mb-8"),
                    
                    # Card Institucional SPP
                    Div(
                        Div(
                            Span(cls="size-2 rounded-full bg-emerald-400"),
                            Span("ATUAÇÃO INSTITUCIONAL", cls="text-[10px] font-mono font-semibold tracking-widest text-emerald-400 uppercase"),
                            cls="flex items-center gap-2 mb-2"
                        ),
                        H4("São Paulo Parcerias (SPP)", cls="text-lg font-bold text-white"),
                        P("Estruturação analítica, auditoria e modelagem de dados para desestatizações, concessões e projetos estratégicos do município de São Paulo.", 
                          cls="text-xs text-zinc-400 mt-1.5 leading-relaxed"),
                        cls="p-6 rounded-2xl bg-[#141419] border border-white/10 shadow-lg mt-auto"
                    ),
                    cls="lg:col-span-5 flex flex-col justify-between h-full gs-scroll"
                ),
                
                # Coluna Direita
                Div(
                    Div(
                        P("Com atuação direta na modelagem e auditoria de dados para desestatizações e parcerias públicas, meu foco é transformar bases volumosas e dispersas em ecossistemas de decisão auditáveis, claros e de alta adoção.",
                          cls="text-base md:text-lg text-zinc-200 leading-relaxed mb-6 font-medium"),
                        P("Inteligência de dados só tem valor real quando reduz a incerteza de diretores e gestores em segundos, unindo a robustez do código em Python e modelagem relacional a interfaces executivas de máxima clareza cognitiva.",
                          cls="text-base md:text-lg text-zinc-400 leading-relaxed mb-10"),
                        cls="mb-4"
                    ),
                    
                    # 3 Microcards de Pilares
                    Div(
                        Div(
                            Span("01", cls="text-xs font-mono font-bold text-zinc-400 block mb-1.5"),
                            H5("Rigor & Auditoria", cls="text-base font-bold text-white mb-1"),
                            P("Bases validadas e estruturadas para atender aos mais altos padrões de compliance e órgãos de controle.", 
                              cls="text-xs text-zinc-400 leading-relaxed"),
                            cls="p-5 rounded-2xl bg-[#141419] border border-white/10 hover:border-white/30 transition-colors"
                        ),
                        Div(
                            Span("02", cls="text-xs font-mono font-bold text-zinc-400 block mb-1.5"),
                            H5("Automação de Ponta", cls="text-base font-bold text-white mb-1"),
                            P("Pipelines em Python que eliminam retrabalho manual e aceleram o fechamento de análises complexas.", 
                              cls="text-xs text-zinc-400 leading-relaxed"),
                            cls="p-5 rounded-2xl bg-[#141419] border border-white/10 hover:border-white/30 transition-colors"
                        ),
                        Div(
                            Span("03", cls="text-xs font-mono font-bold text-zinc-400 block mb-1.5"),
                            H5("Design Cognitivo", cls="text-base font-bold text-white mb-1"),
                            P("Painéis executivos desenhados para que decisores encontrem respostas críticas com máxima agilidade.", 
                              cls="text-xs text-zinc-400 leading-relaxed"),
                            cls="p-5 rounded-2xl bg-[#141419] border border-white/10 hover:border-white/30 transition-colors"
                        ),
                        cls="grid grid-cols-1 sm:grid-cols-3 gap-4"
                    ),
                    cls="lg:col-span-7 flex flex-col justify-between h-full gs-scroll"
                ),
                cls="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16 items-stretch"
            ),
            cls="max-w-7xl mx-auto px-6"
        ),
        id="about",
        cls="py-24 md:py-28 bg-[#0A0A0C] border-b border-white/10 relative z-20 scroll-mt-20"
    )

def Diagnostico():
    btn = "w-full text-left p-5 rounded-2xl border border-white/10 bg-[#16161D] text-zinc-200 hover:border-white/40 hover:bg-white hover:text-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-white transition-all font-medium text-sm md:text-base cursor-pointer"

    # Painel Único Dinâmico
    painel_dinamico = Div(
        Div(
            Div(
                Span(cls="text-xs font-mono uppercase tracking-widest text-zinc-400", **{"x-text": "`Pergunta 0${i + 1} de 0${total}`"}),
                Button(
                    "← Voltar",
                    type="button",
                    cls="text-xs font-mono text-zinc-400 hover:text-white underline cursor-pointer",
                    **{"x-show": "i > 0", "@click": "voltar()"}
                ),
                cls="flex items-center justify-between mb-4"
            ),
            H3(cls="text-2xl md:text-3xl font-bold text-white mb-8 tracking-tight leading-snug", **{"x-text": "dados.perguntas[i].q"}),
            Div(
                Template(
                    Button(
                        Span(**{"x-text": "opt[0]"}),
                        type="button", 
                        cls=btn, 
                        **{"@click": "responder(opt[1])"}
                    ),
                    **{"x-for": "(opt, index) in dados.perguntas[i].opcoes", ":key": "index"}
                ),
                cls="grid grid-cols-1 gap-3.5"
            ),
            cls="space-y-4",
            aria_live="polite"
        ),
        **{"x-show": "!concluido"}
    )

    resultado = Div(
        Div(
            Span(cls="size-2 rounded-full bg-emerald-400"),
            Span("Diagnóstico Concluído", cls="text-xs font-mono uppercase tracking-wider text-emerald-400"),
            cls="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 mb-4"
        ),
        H3(cls="text-3xl md:text-4xl font-bold text-white mb-4 tracking-tight", **{"x-text": "nivel.titulo"}),
        Div(
            Span("Pontuação Consolidada: ", cls="text-zinc-400"),
            Span(cls="text-white font-bold", **{"x-text": "`${pontos} / ${dados.max}`"}),
            cls="font-mono text-sm mb-6"
        ),
        P(cls="text-zinc-300 text-base md:text-lg leading-relaxed mb-8 max-w-xl mx-auto", **{"x-text": "nivel.recomendacao"}),
        Div(
            A("Conversar Sobre o Próximo Passo", href="#",
              cls="bg-white text-black font-semibold px-8 py-4 rounded-xl hover:bg-zinc-200 transition-colors shadow-lg",
              **{":href": "mailto"}),
            Button("Refazer Diagnóstico", type="button",
                   cls="border border-white/20 bg-transparent text-white font-semibold px-8 py-4 rounded-xl hover:bg-white/10 transition-all cursor-pointer",
                   **{"@click": "reiniciar()"}),
            cls="flex flex-wrap items-center justify-center gap-4",
        ),
        **{"x-show": "concluido", "x-cloak": ""},
        cls="text-center py-4"
    )

    safe_json = json.dumps(DIAGNOSTICO, ensure_ascii=False).replace("</", "<\\/")

    return Section(
        Div(
            Span("FERRAMENTA INTERATIVA SEM CADASTRO", cls="text-xs font-mono uppercase tracking-[0.25em] text-zinc-400 text-center block mb-3"),
            H2("DIAGNÓSTICO DE MATURIDADE EM DADOS",
               cls="text-4xl md:text-5xl font-oswald uppercase tracking-tight text-white text-center mb-4 leading-[1.18]"),
            P("Quatro perguntas objetivas para mapear a maturidade analítica da sua operação e o próximo passo para alcançar decisões estratégicas.",
              cls="text-center text-zinc-400 text-base md:text-lg mb-12 max-w-xl mx-auto"),
            Div(
                # Progress Track com Acessibilidade
                Div(
                    Div(
                        cls="h-full bg-white rounded-full transition-all duration-500",
                        **{":style": "`width: ${progresso}%`"}
                    ),
                    role="progressbar",
                    aria_valuemin="0",
                    aria_valuemax="100",
                    **{":aria-valuenow": "progresso"},
                    cls="h-1.5 w-full bg-white/10 rounded-full mb-10 overflow-hidden",
                ),
                painel_dinamico,
                resultado,
                Script(NotStr(f"window.MATURIDADE = {safe_json};\n{DIAG_JS}")),
                cls="relative min-h-[340px] bg-[#121217] p-8 md:p-12 rounded-[2rem] border border-white/10 shadow-2xl",
            ),
            cls="max-w-3xl mx-auto",
            **{"x-data": "maturidade()"},
        ),
        id="diagnostico",
        cls="py-28 px-6 bg-[#0E0E12] relative z-10 border-t border-white/10 gs-scroll scroll-mt-20",
    )

@rt("/")
def get():
    return (
        # --- TOP NAVIGATION (Sincronizada + Mobile Drawer com Alpine) ---
        Header(
            Div(
                # Brand Logo
                A(
                    Span("João", cls="font-playfair italic font-bold text-3xl text-white"),
                    Span(".", cls="text-zinc-500 font-sans font-light not-italic text-3xl"),
                    href="/", 
                    cls="group flex items-center"
                ),
                
                # Links Desktop (Ordem Real da Página)
                Nav(
                    A("Sobre", href="#about", cls="text-sm font-semibold text-zinc-300 hover:text-white transition-colors"),
                    A("Projetos", href="#work", cls="text-sm font-semibold text-zinc-300 hover:text-white transition-colors"),
                    A("Filosofia", href="#philosophy", cls="text-sm font-semibold text-zinc-300 hover:text-white transition-colors"),
                    A("Engenharia", href="#capabilities", cls="text-sm font-semibold text-zinc-300 hover:text-white transition-colors"),
                    A("Diagnóstico", href="#diagnostico", cls="text-sm font-semibold text-zinc-300 hover:text-white transition-colors"),
                    cls="hidden md:flex items-center gap-8"
                ),
                
                # Right CTA & Mobile Toggle
                Div(
                    A(
                        "Iniciar Conversa", 
                        href=f"mailto:{EMAIL_CONTACT}", 
                        cls="hidden sm:inline-flex bg-white text-black text-sm font-semibold px-6 py-2.5 rounded-full hover:bg-zinc-200 transition-colors shadow-sm"
                    ),
                    Button(
                        NotStr('<svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>'),
                        cls="md:hidden p-2 text-white focus:outline-none cursor-pointer",
                        aria_label="Abrir menu de navegação",
                        **{"@click": "mobileOpen = !mobileOpen"}
                    ),
                    cls="flex items-center gap-3"
                ),
                
                cls="max-w-[1440px] mx-auto px-6 py-6 flex items-center justify-between"
            ),
            
            # Mobile Menu Dropdown
            Div(
                Nav(
                    A("Sobre", href="#about", cls="text-base font-semibold text-zinc-200 hover:text-white py-2 block border-b border-white/5", **{"@click": "mobileOpen = false"}),
                    A("Projetos", href="#work", cls="text-base font-semibold text-zinc-200 hover:text-white py-2 block border-b border-white/5", **{"@click": "mobileOpen = false"}),
                    A("Filosofia", href="#philosophy", cls="text-base font-semibold text-zinc-200 hover:text-white py-2 block border-b border-white/5", **{"@click": "mobileOpen = false"}),
                    A("Engenharia", href="#capabilities", cls="text-base font-semibold text-zinc-200 hover:text-white py-2 block border-b border-white/5", **{"@click": "mobileOpen = false"}),
                    A("Diagnóstico", href="#diagnostico", cls="text-base font-semibold text-zinc-200 hover:text-white py-2 block border-b border-white/5", **{"@click": "mobileOpen = false"}),
                    A("Iniciar Conversa", href=f"mailto:{EMAIL_CONTACT}", cls="text-base font-semibold text-emerald-400 py-3 block", **{"@click": "mobileOpen = false"}),
                    cls="flex flex-col p-6 space-y-1"
                ),
                cls="md:hidden bg-[#0E0E12] border-b border-white/10 shadow-2xl",
                **{"x-show": "mobileOpen", "x-cloak": "", "x-transition.opacity.duration.200ms": ""}
            ),
            cls="w-full absolute top-0 z-50",
            **{"x-data": "{ mobileOpen: false }"}
        ),
        
        # --- HERO SECTION (High-Contrast Editorial Dark Stage) ---
        Main(
            Div(
                # Studio Spotlight Background
                Div(cls="absolute inset-0 studio-spotlight z-0 pointer-events-none"),
                
                # TOP TYPOGRAPHY: "Hey, there"
                Div(
                    Span("Hey,", cls="font-playfair italic text-[11vw] sm:text-[9vw] lg:text-[120px] leading-none text-white/70 font-normal select-none"),
                    Span("there", cls="font-playfair italic text-[11vw] sm:text-[9vw] lg:text-[120px] leading-none text-white/30 font-normal select-none"),
                    cls="absolute top-[16%] w-full flex justify-between px-[10%] z-10 gs-reveal pointer-events-none"
                ),
                
                # CENTER PORTRAIT (Transparent Cutout Image)
                Img(
                    src="/static/images/joao.png", 
                    alt="João Barbosa - Analista de Dados & BI", 
                    width="432",
                    height="578",
                    fetchpriority="high",
                    cls="absolute -bottom-1 left-1/2 -translate-x-1/2 w-auto h-[68%] sm:h-[74%] max-h-[640px] max-w-[500px] object-contain object-bottom z-30 contrast-[1.08] brightness-[1.02] drop-shadow-[0_20px_50px_rgba(0,0,0,0.9)] pointer-events-none hero-image"
                ),
                
                # Gradient blend at feet to merge with next section seamlessly
                Div(cls="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-[#0A0A0C] via-[#0A0A0C]/80 to-transparent z-35 pointer-events-none"),

                # MIDDLE LEFT: Availability Pill
                A(
                    Div(cls="w-2.5 h-2.5 rounded-full bg-emerald-400"),
                    Span("Disponível para Projetos Estratégicos", cls="text-sm font-semibold text-zinc-200"),
                    href="#diagnostico",
                    cls="hidden lg:flex absolute left-[6%] xl:left-[10%] top-[45%] z-40 glass-pill px-4 py-2 rounded-full items-center gap-2.5 shadow-xl hover:border-white/30 transition-all gs-reveal"
                ),
                
                # MIDDLE RIGHT: Strategic Focus
                Div(
                    Div(
                        Span("FOCO ESTRATÉGICO", cls="text-[11px] font-mono font-bold text-zinc-400 tracking-wider block mb-1 uppercase"),
                        P("Arquitetura de Dados, Analytics e Visualização para Decisões Executivas.", cls="text-sm font-semibold text-zinc-200 leading-snug"),
                        cls="border-l-2 border-white/30 pl-3.5"
                    ),
                    cls="hidden lg:block absolute right-[6%] xl:right-[10%] top-[45%] z-40 max-w-[220px] text-left gs-reveal pointer-events-none"
                ),
                
                # BOTTOM LEFT: "EU SOU JOÃO" (Entrelinha e respiro corrigidos)
                Div(
                    H1(
                        Span("EU SOU", cls="block"), 
                        Span("JOÃO", cls="text-white block pt-[0.1em]"), 
                        cls="font-oswald text-[9vw] xl:text-[112px] leading-[0.98] font-bold text-white/90 uppercase tracking-tight"
                    ),
                    cls="absolute left-[5%] xl:left-[8%] bottom-6 sm:bottom-8 lg:bottom-10 z-20 gs-reveal pointer-events-none"
                ),
                
                # BOTTOM RIGHT: "DATA ANALYST" (Hierarquia visual valorizada em branco)
                Div(
                    H2(
                        Span("DATA", cls="text-white block"), 
                        Span("ANALYST", cls="text-white block pt-[0.1em]"), 
                        cls="font-oswald text-[8vw] xl:text-[92px] leading-[0.98] font-bold uppercase tracking-tight text-right"
                    ),
                    cls="absolute right-[5%] xl:right-[8%] bottom-6 sm:bottom-8 lg:bottom-10 z-20 gs-reveal pointer-events-none"
                ),
                
                # HERO BOTTOM STATUS BAR
                Div(
                    Div(
                        Span(cls="inline-block w-2 h-2 rounded-full bg-emerald-400"),
                        Span("STACK ANALÍTICA: PYTHON • POSTGRESQL • POWER BI"),
                        cls="flex items-center gap-2.5"
                    ),
                    Div(
                        Span("PREF. DE SÃO PAULO • GOV DATA LAB"),
                        A("EXPLORAR PORTFÓLIO ↓", href="#work", cls="text-white underline underline-offset-4 hover:text-zinc-300 ml-4 pointer-events-auto"),
                        cls="flex items-center gap-4"
                    ),
                    cls="absolute bottom-2 inset-x-0 max-w-7xl mx-auto px-6 hidden sm:flex items-center justify-between text-[11px] font-mono text-zinc-400 z-40"
                ),

                cls="relative w-full h-[100svh] min-h-[680px] max-h-[1020px] overflow-hidden border-b border-white/10"
            ),
            cls="w-full"
        ),
        
        # --- METRICS & PROVEN RECORD STRIP (Slim Single Row) ---
        Section(
            Div(
                # Metric 1
                Div(
                    H3("+3 ANOS", cls="text-2xl lg:text-[26px] font-oswald tracking-tight text-white"),
                    P("Gerando inteligência na ", Strong("Pref. de São Paulo", cls="text-zinc-200"), cls="text-[11px] lg:text-xs text-zinc-400 mt-0.5 leading-tight whitespace-nowrap"),
                    cls="flex-1 flex flex-col items-center text-center gs-scroll px-2"
                ),
                Div(cls="w-px h-8 bg-white/10 mx-2 hidden sm:block gs-scroll"),
                # Metric 2
                Div(
                    H3("10M+", cls="text-2xl lg:text-[26px] font-oswald tracking-tight text-white"),
                    P("Linhas auditadas em ", Strong("Pipelines Automatizados", cls="text-zinc-200"), cls="text-[11px] lg:text-xs text-zinc-400 mt-0.5 leading-tight whitespace-nowrap"),
                    cls="flex-1 flex flex-col items-center text-center gs-scroll px-2"
                ),
                Div(cls="w-px h-8 bg-white/10 mx-2 hidden sm:block gs-scroll"),
                # Metric 3
                Div(
                    H3("100%", cls="text-2xl lg:text-[26px] font-oswald tracking-tight text-white"),
                    P("Modelagem em ", Strong("Star Schema", cls="text-zinc-200"), " relacional", cls="text-[11px] lg:text-xs text-zinc-400 mt-0.5 leading-tight whitespace-nowrap"),
                    cls="flex-1 flex flex-col items-center text-center gs-scroll px-2"
                ),
                Div(cls="w-px h-8 bg-white/10 mx-2 hidden sm:block gs-scroll"),
                # Metric 4
                Div(
                    H3("< 5s", cls="text-2xl lg:text-[26px] font-oswald tracking-tight text-emerald-400"),
                    P("Tempo de insight para ", Strong("Diretoria e Gestores", cls="text-zinc-200"), cls="text-[11px] lg:text-xs text-zinc-400 mt-0.5 leading-tight whitespace-nowrap"),
                    cls="flex-1 flex flex-col items-center text-center gs-scroll px-2"
                ),
                cls="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between px-6 gap-4 sm:gap-0"
            ),
            cls="border-b border-white/10 bg-[#0E0E12] py-5 md:py-6 relative z-20"
        ),

        # --- TECH STACK MARQUEE ---
        TechMarquee(),

        # --- BIO / TRAJETÓRIA EXECUTIVA ---
        AboutSection(),

        # --- SELECTED WORK (REAL INTERACTIVE CAROUSEL) ---
        Section(
            Div(
                Div(
                    Span("PORTFÓLIO EXECUTIVO SELECIONADO", cls="text-xs font-mono uppercase tracking-[0.2em] text-zinc-400 block mb-3"),
                    H2("PROJETOS RECENTES", cls="text-4xl sm:text-5xl font-oswald uppercase tracking-tight text-white mb-4 leading-[1.18]"),
                    P("Demonstrações interativas reais construídas com rigor relacional, telemetria e interfaces executivas de alta adoção.", cls="text-zinc-400 text-base max-w-xl"),
                    cls="text-left mb-16 gs-scroll"
                ),
                FeatureCarousel(),
                cls="max-w-7xl mx-auto px-6 py-24"
            ),
            id="work", cls="bg-[#0A0A0C] relative z-10 border-b border-white/10"
        ),

        # --- PHILOSOPHY ---
        Section(
            Div(
                H2("Dashboards são fáceis.", Br(), Span("Decisões são difíceis.", cls="font-playfair italic text-zinc-400 font-normal"), cls="text-4xl sm:text-6xl font-bold tracking-tight text-white text-center mb-6 gs-scroll leading-[1.18]"),
                P("Qualquer um pode conectar um CSV a um visualizador comercial. Meu foco é estruturar dados para que reflitam rigorosamente a realidade operacional e respondam às perguntas estratégicas da liderança.", cls="text-center text-zinc-400 max-w-2xl mx-auto mb-16 text-base sm:text-lg gs-scroll"),
                Div(
                    # Card 1
                    Div(
                        Div(
                            Span("ETL & GOVERNANÇA", cls="text-[11px] font-mono font-bold tracking-widest text-zinc-400 uppercase"),
                            Span("01", cls="text-4xl font-oswald text-zinc-600 group-hover:text-white transition-colors duration-300"),
                            cls="flex items-center justify-between"
                        ),
                        Div(
                            H4("Higienização & Pipeline", cls="text-2xl font-oswald uppercase tracking-tight text-white mt-6 mb-3 leading-[1.18]"),
                            P("Garbage in, garbage out. Construo rotinas automatizadas e contratos de dados para tratar anomalias antes que elas contaminem reuniões de diretoria.", cls="text-sm text-zinc-400 leading-relaxed"),
                        ),
                        Div(
                            Span(cls="size-2 rounded-full bg-blue-400 mr-2.5"),
                            Span("Dados auditáveis e consistentes", cls="text-xs font-semibold text-zinc-300"),
                            cls="flex items-center pt-6 mt-6 border-t border-white/10"
                        ),
                        cls="bg-[#121217] rounded-[28px] p-8 md:p-10 border border-white/10 hover:border-white/30 transition-all duration-300 relative group flex flex-col justify-between gs-scroll"
                    ),
                    # Card 2
                    Div(
                        Div(
                            Span("ARQUITETURA RELACIONAL", cls="text-[11px] font-mono font-bold tracking-widest text-zinc-400 uppercase"),
                            Span("02", cls="text-4xl font-oswald text-zinc-600 group-hover:text-white transition-colors duration-300"),
                            cls="flex items-center justify-between"
                        ),
                        Div(
                            H4("Modelagem Dimensional", cls="text-2xl font-oswald uppercase tracking-tight text-white mt-6 mb-3 leading-[1.18]"),
                            P("Modelos relacionais otimizados em Star Schema. Crio a fundação que permite consultas instantâneas e cruzamentos complexos para milhões de linhas.", cls="text-sm text-zinc-400 leading-relaxed"),
                        ),
                        Div(
                            Span(cls="size-2 rounded-full bg-emerald-400 mr-2.5"),
                            Span("Consultas otimizadas em SQL", cls="text-xs font-semibold text-zinc-300"),
                            cls="flex items-center pt-6 mt-6 border-t border-white/10"
                        ),
                        cls="bg-[#121217] rounded-[28px] p-8 md:p-10 border border-white/10 hover:border-white/30 transition-all duration-300 relative group flex flex-col justify-between gs-scroll"
                    ),
                    # Card 3
                    Div(
                        Div(
                            Span("UI/UX & STORYTELLING", cls="text-[11px] font-mono font-bold tracking-widest text-zinc-400 uppercase"),
                            Span("03", cls="text-4xl font-oswald text-zinc-600 group-hover:text-white transition-colors duration-300"),
                            cls="flex items-center justify-between"
                        ),
                        Div(
                            H4("Visualização Executiva", cls="text-2xl font-oswald uppercase tracking-tight text-white mt-6 mb-3 leading-[1.18]"),
                            P("O cérebro humano é visual e seletivo. Projeto telas com hierarquia óptica limpa para que gestores absorvam conclusões críticas com rapidez e clareza.", cls="text-sm text-zinc-400 leading-relaxed"),
                        ),
                        Div(
                            Span(cls="size-2 rounded-full bg-amber-400 mr-2.5"),
                            Span("Foco em alta adoção prática", cls="text-xs font-semibold text-zinc-300"),
                            cls="flex items-center pt-6 mt-6 border-t border-white/10"
                        ),
                        cls="bg-[#121217] rounded-[28px] p-8 md:p-10 border border-white/10 hover:border-white/30 transition-all duration-300 relative group flex flex-col justify-between gs-scroll"
                    ),
                    cls="grid grid-cols-1 md:grid-cols-3 gap-8"
                ),
                cls="max-w-6xl mx-auto px-6 py-24"
            ),
            id="philosophy", cls="relative z-10 bg-[#0E0E12] border-b border-white/10"
        ),

        # --- BENTO GRID: CAPACIDADES TÉCNICAS (Impressão Digital em Dark Mode) ---
        Section(
            Div(
                Span("CAPACIDADES TÉCNICAS", cls="text-xs font-bold text-zinc-400 tracking-widest uppercase mb-3 block font-mono text-center gs-scroll"),
                H2("ENGENHARIA & INTELIGÊNCIA EM DADOS", cls="text-4xl md:text-5xl font-oswald uppercase tracking-tight text-white text-center mb-4 gs-scroll leading-[1.18]"),
                P("Modelagem relacional rigorosa, governança e rastreabilidade da origem ao painel final.", cls="text-center text-zinc-400 mb-16 gs-scroll text-base md:text-lg max-w-2xl mx-auto"),
                
                Div(
                    # Card 1: 100% Integridade (com Impressão Digital / Loop Orbital SVG)
                    Div(
                        Div(
                            Div(
                                NotStr('''<svg class="text-white/10 absolute inset-0 size-full pointer-events-none" viewBox="0 0 254 104" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M112.891 97.7022C140.366 97.0802 171.004 94.6715 201.087 87.5116C210.43 85.2881 219.615 82.6412 228.284 78.2473C232.198 76.3179 235.905 73.9942 239.348 71.3124C241.85 69.2557 243.954 66.7571 245.555 63.9408C249.34 57.3235 248.281 50.5341 242.498 45.6109C239.033 42.7237 235.228 40.2703 231.169 38.3054C219.443 32.7209 207.141 28.4382 194.482 25.534C184.013 23.1927 173.358 21.7755 162.64 21.2989C161.376 21.3512 160.113 21.181 158.908 20.796C158.034 20.399 156.857 19.1682 156.962 18.4535C157.115 17.8927 157.381 17.3689 157.743 16.9139C158.104 16.4588 158.555 16.0821 159.067 15.8066C160.14 15.4683 161.274 15.3733 162.389 15.5286C179.805 15.3566 196.626 18.8373 212.998 24.462C220.978 27.2494 228.798 30.4747 236.423 34.1232C240.476 36.1159 244.202 38.7131 247.474 41.8258C254.342 48.2578 255.745 56.9397 251.841 65.4892C249.793 69.8582 246.736 73.6777 242.921 76.6327C236.224 82.0192 228.522 85.4602 220.502 88.2924C205.017 93.7847 188.964 96.9081 172.738 99.2109C153.442 101.949 133.993 103.478 114.506 103.79C91.1468 104.161 67.9334 102.97 45.1169 97.5831C36.0094 95.5616 27.2626 92.1655 19.1771 87.5116C13.839 84.5746 9.1557 80.5802 5.41318 75.7725C-0.54238 67.7259 -1.13794 59.1763 3.25594 50.2827C5.82447 45.3918 9.29572 41.0315 13.4863 37.4319C24.2989 27.5721 37.0438 20.9681 50.5431 15.7272C68.1451 8.8849 86.4883 5.1395 105.175 2.83669C129.045 0.0992292 153.151 0.134761 177.013 2.94256C197.672 5.23215 218.04 9.01724 237.588 16.3889C240.089 17.3418 242.498 18.5197 244.933 19.6446C246.627 20.4387 247.725 21.6695 246.997 23.615C246.455 25.1105 244.814 25.5605 242.63 24.5811C230.322 18.9961 217.233 16.1904 204.117 13.4376C188.761 10.3438 173.2 8.36665 157.558 7.52174C129.914 5.70776 102.154 8.06792 75.2124 14.5228C60.6177 17.8788 46.5758 23.2977 33.5102 30.6161C26.6595 34.3329 20.4123 39.0673 14.9818 44.658C12.9433 46.8071 11.1336 49.1622 9.58207 51.6855C4.87056 59.5336 5.61172 67.2494 11.9246 73.7608C15.2064 77.0494 18.8775 79.925 22.8564 82.3236C31.6176 87.7101 41.3848 90.5291 51.3902 92.5804C70.6068 96.5773 90.0219 97.7419 112.891 97.7022Z" fill="currentColor"/>
                                </svg>'''),
                                Span("100%", cls="text-5xl font-oswald font-bold text-white z-10 block"),
                                cls="relative flex h-24 w-56 items-center justify-center"
                            ),
                            Div(
                                H3("Integridade & Auditoria", cls="text-xl font-oswald uppercase tracking-tight text-white font-bold leading-[1.18]"),
                                P("Modelagem com validações contínuas, sem duplicações ou inconsistências analíticas.", cls="text-sm text-zinc-400 mt-1"),
                                cls="mt-8 text-center"
                            ),
                            cls="relative m-auto size-fit pt-6"
                        ),
                        cls="relative col-span-full flex flex-col justify-between overflow-hidden lg:col-span-2 rounded-3xl border border-white/10 bg-[#121217] p-6 shadow-sm hover:border-white/25 transition-all gs-scroll"
                    ),
                    
                    # Card 2: Radar / Conexões Concêntricas
                    Div(
                        Div(
                            Div(
                                NotStr('''<svg class="m-auto h-fit w-24 text-zinc-400" viewBox="0 0 212 143" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path class="text-zinc-600" d="M44.0209 55.3542C43.1945 54.7639 42.6916 54.0272 42.5121 53.1442C42.3327 52.2611 42.5995 51.345 43.3125 50.3958C50.632 40.3611 59.812 32.5694 70.8525 27.0208C81.8931 21.4722 93.668 18.6979 106.177 18.6979C118.691 18.6979 130.497 21.3849 141.594 26.7587C152.691 32.1326 161.958 39.8936 169.396 50.0417C170.222 51.1042 170.489 52.0486 170.196 52.875C169.904 53.7014 169.401 54.4097 168.688 55C167.979 55.5903 167.153 55.8571 166.208 55.8004C165.264 55.7437 164.438 55.2408 163.729 54.2917C157.236 45.0833 148.885 38.0307 138.675 33.1337C128.466 28.2368 117.633 25.786 106.177 25.7812C94.7257 25.7812 83.9827 28.2321 73.948 33.1337C63.9132 38.0354 55.5903 45.0881 48.9792 54.2917C48.2709 55.3542 47.4445 55.9444 46.5 56.0625C45.5556 56.1806 44.7292 55.9444 44.0209 55.3542ZM126.188 142.656C113.91 139.587 103.875 133.476 96.0834 124.325C88.2917 115.173 84.3959 103.988 84.3959 90.7708C84.3959 84.8681 86.5209 79.9097 90.7709 75.8958C95.0209 71.8819 100.156 69.875 106.177 69.875C112.198 69.875 117.333 71.8819 121.583 75.8958C125.833 79.9097 127.958 84.8681 127.958 90.7708C127.958 94.6667 129.434 97.9439 132.385 100.602C135.337 103.261 138.819 104.588 142.833 104.583C146.847 104.583 150.271 103.256 153.104 100.602C155.938 97.9486 157.354 94.6714 157.354 90.7708C157.354 77.0764 152.337 65.566 142.302 56.2396C132.267 46.9132 120.285 42.25 106.354 42.25C92.4237 42.25 80.441 46.9132 70.4063 56.2396C60.3716 65.566 55.3542 77.0174 55.3542 90.5937C55.3542 93.4271 55.621 96.9687 56.1546 101.219C56.6882 105.469 57.9562 110.427 59.9584 116.094C60.3125 117.156 60.2842 118.101 59.8734 118.927C59.4625 119.753 58.7825 120.344 57.8334 120.698C56.8889 121.052 55.9752 121.024 55.0921 120.613C54.2091 120.202 53.5881 119.522 53.2292 118.573C51.4584 113.969 50.1905 109.395 49.4255 104.853C48.6605 100.31 48.2756 95.6158 48.2709 90.7708C48.2709 75.0694 53.9682 61.9062 65.363 51.2812C76.7577 40.6562 90.3624 35.3437 106.177 35.3437C122.115 35.3437 135.809 40.6562 147.26 51.2812C158.712 61.9062 164.438 75.0694 164.438 90.7708C164.438 96.6736 162.343 101.601 158.155 105.554C153.966 109.506 148.859 111.485 142.833 111.49C136.813 111.49 131.649 109.513 127.342 105.561C123.035 101.608 120.88 96.6783 120.875 90.7708C120.875 86.875 119.43 83.5978 116.54 80.9392C113.65 78.2805 110.196 76.9536 106.177 76.9583C102.163 76.9583 98.7089 78.2876 95.8142 80.9462C92.9195 83.6049 91.4745 86.8797 91.4792 90.7708C91.4792 102.222 94.8745 111.785 101.665 119.458C108.456 127.132 117.22 132.503 127.958 135.573C129.021 135.927 129.729 136.517 130.083 137.344C130.438 138.17 130.497 139.056 130.26 140C130.024 140.826 129.552 141.535 128.844 142.125C128.135 142.715 127.25 142.892 126.188 142.656ZM67.0417 18.3437C66.0973 18.934 65.1528 19.0828 64.2084 18.79C63.2639 18.4972 62.5556 17.8762 62.0834 16.9271C61.6112 15.9826 61.4931 15.1279 61.7292 14.3629C61.9653 13.5979 62.5556 12.9179 63.5 12.3229C70.1112 8.78125 77.0174 6.06597 84.2188 4.17708C91.4202 2.28819 98.7396 1.34375 106.177 1.34375C113.733 1.34375 121.111 2.25986 128.313 4.09208C135.514 5.92431 142.479 8.54986 149.208 11.9687C150.271 12.559 150.892 13.2674 151.071 14.0937C151.251 14.9201 151.161 15.7465 150.802 16.5729C150.448 17.3993 149.858 18.0486 149.031 18.5208C148.205 18.9931 147.201 18.934 146.021 18.3437C139.764 15.1563 133.299 12.7078 126.627 10.9983C119.954 9.28889 113.138 8.43181 106.177 8.42708C99.3299 8.42708 92.6007 9.22514 85.9896 10.8212C79.3785 12.4174 73.0625 14.9249 67.0417 18.3437ZM87.9375 140.177C80.9723 132.858 75.6314 125.392 71.915 117.78C68.1987 110.167 66.3381 101.164 66.3334 90.7708C66.3334 80.0278 70.2292 70.9658 78.0209 63.585C85.8125 56.2042 95.198 52.5161 106.177 52.5208C117.156 52.5208 126.601 56.2112 134.51 63.5921C142.42 70.9729 146.375 80.0325 146.375 90.7708C146.375 91.8333 146.052 92.6904 145.405 93.3421C144.758 93.9937 143.901 94.3172 142.833 94.3125C141.889 94.3125 141.063 93.989 140.354 93.3421C139.646 92.6951 139.292 91.8381 139.292 90.7708C139.292 81.9167 136.014 74.5099 129.46 68.5504C122.906 62.591 115.145 59.6089 106.177 59.6042C97.2049 59.6042 89.503 62.5862 83.0713 68.5504C76.6396 74.5146 73.4214 81.9214 73.4167 90.7708C73.4167 100.333 75.0695 108.451 78.375 115.123C81.6806 121.796 86.5209 128.494 92.8959 135.219C93.6042 135.927 93.9584 136.753 93.9584 137.698C93.9584 138.642 93.6042 139.469 92.8959 140.177C92.1875 140.885 91.3612 141.24 90.4167 141.24C89.4723 141.24 88.6459 140.885 87.9375 140.177ZM141.417 128.135C130.91 128.135 121.789 124.594 114.054 117.51C106.319 110.427 102.454 101.514 102.458 90.7708C102.458 89.8264 102.784 89 103.436 88.2917C104.088 87.5833 104.942 87.2292 106 87.2292C107.063 87.2292 107.92 87.5833 108.571 88.2917C109.223 89 109.546 89.8264 109.542 90.7708C109.542 99.625 112.729 106.885 119.104 112.552C125.479 118.219 132.917 121.052 141.417 121.052C142.125 121.052 143.129 120.993 144.427 120.875C145.726 120.757 147.083 120.58 148.5 120.344C149.563 120.108 150.479 120.256 151.248 120.79C152.018 121.324 152.519 122.119 152.75 123.177C152.986 124.122 152.809 124.948 152.219 125.656C151.629 126.365 150.861 126.837 149.917 127.073C147.792 127.663 145.934 127.989 144.342 128.05C142.751 128.112 141.776 128.14 141.417 128.135Z" fill="currentColor"/>
                                    <path d="M3 72H209" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
                                </svg>'''),
                                cls="relative mx-auto flex aspect-square size-32 rounded-full border border-white/10 before:absolute before:-inset-2 before:rounded-full before:border before:border-white/5 items-center justify-center bg-white/[0.02]"
                            ),
                            Div(
                                H3("Segurança & Governança", cls="text-xl font-oswald uppercase tracking-tight text-white font-bold leading-[1.18]"),
                                P("Controle rigoroso de acessos, conformidade e rastreabilidade total de linhagem de dados.", cls="text-sm text-zinc-400 mt-1"),
                                cls="relative z-10 mt-6 space-y-2 text-center"
                            ),
                            cls="pt-6"
                        ),
                        cls="relative col-span-full overflow-hidden sm:col-span-3 lg:col-span-2 rounded-3xl border border-white/10 bg-[#121217] p-6 shadow-sm hover:border-white/25 transition-all gs-scroll"
                    ),
                    
                    # Card 3: Performance em Milissegundos
                    Div(
                        Div(
                            Div(
                                NotStr('''<svg class="w-full text-zinc-200" viewBox="0 0 386 123" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <rect width="386" height="123" rx="10" fill="#18181E"/>
                                    <path d="M3 121.077C3 121.077 15.3041 93.6691 36.0195 87.756C56.7349 81.8429 66.6632 80.9723 66.6632 80.9723C66.6632 80.9723 80.0327 80.9723 91.4656 80.9723C102.898 80.9723 100.415 64.2824 108.556 64.2824C116.696 64.2824 117.693 92.1332 125.226 92.1332C132.759 92.1332 142.07 78.5115 153.591 80.9723C165.113 83.433 186.092 92.1332 193 92.1332C199.908 92.1332 205.274 64.2824 213.017 64.2824C220.76 64.2824 237.832 93.8946 243.39 92.1332C248.948 90.3718 257.923 60.5 265.284 60.5C271.145 60.5 283.204 87.7182 285.772 87.756C293.823 87.8746 299.2 73.0802 304.411 73.0802C311.283 73.0802 321.425 65.9506 333.552 64.2824C345.68 62.6141 346.91 82.4553 362.27 80.9723C377.629 79.4892 383 106.605 383 106.605" stroke="#FFFFFF" stroke-width="2.5"/>
                                </svg>'''),
                                cls="pt-2 px-1"
                            ),
                            Div(
                                H3("Performance & Otimização", cls="text-xl font-oswald uppercase tracking-tight text-white font-bold leading-[1.18]"),
                                P("Consultas SQL otimizadas com Star Schema e tempos de resposta instantâneos.", cls="text-sm text-zinc-400 mt-1"),
                                cls="relative z-10 mt-6 space-y-2 text-center"
                            ),
                            cls="pt-6"
                        ),
                        cls="relative col-span-full overflow-hidden sm:col-span-3 lg:col-span-2 rounded-3xl border border-white/10 bg-[#121217] p-6 shadow-sm hover:border-white/25 transition-all gs-scroll"
                    ),
                    
                    # Card 4: Pipelines & Telemetria
                    Div(
                        Div(
                            Div(
                                Div(
                                    NotStr('''<svg class="size-5 text-white" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
                                    </svg>'''),
                                    cls="relative flex aspect-square size-12 rounded-full border border-white/10 before:absolute before:-inset-1.5 before:rounded-full before:border before:border-white/5 items-center justify-center bg-white/[0.02]"
                                ),
                                Div(
                                    H3("Pipelines Automatizados", cls="text-xl font-oswald uppercase tracking-tight text-white font-bold leading-[1.18]"),
                                    P("Ingestão contínua com rotinas automatizadas, reexecução assistida e logs de auditoria.", cls="text-sm text-zinc-400 mt-1"),
                                    cls="space-y-2"
                                ),
                                cls="relative z-10 flex flex-col justify-between space-y-6"
                            ),
                            Div(
                                Div(
                                    Span(cls="block size-2 rounded-full bg-zinc-600"),
                                    Span(cls="block size-2 rounded-full bg-zinc-600"),
                                    Span(cls="block size-2 rounded-full bg-zinc-600"),
                                    cls="absolute left-3 top-2 flex gap-1 z-10"
                                ),
                                NotStr('''<svg class="w-full text-zinc-200" viewBox="0 0 366 231" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M1 179.796L4.05663 172.195V183.933L7.20122 174.398L8.45592 183.933L10.0546 186.948V155.455L12.6353 152.613V145.122L15.3021 134.71V149.804V155.455L16.6916 160.829L18.1222 172.195V158.182L19.8001 152.613L21.4105 148.111V137.548L23.6863 142.407V126.049L25.7658 127.87V120.525L27.2755 118.066L29.1801 112.407V123.822L31.0426 120.525V130.26L32.3559 134.71L34.406 145.122V137.548L35.8982 130.26L37.1871 126.049L38.6578 134.71L40.659 138.977V130.26V126.049L43.7557 130.26V123.822L45.972 112.407L47.3391 103.407V92.4726L49.2133 98.4651V106.053L52.5797 89.7556L54.4559 82.7747L56.1181 87.9656L58.9383 89.7556V98.4651L60.7617 103.407L62.0545 123.822L63.8789 118.066L65.631 122.082L68.5479 114.229L70.299 109.729L71.8899 118.066L73.5785 123.822V130.26L74.9446 134.861L76.9243 127.87L78.352 134.71V138.977L80.0787 142.407V152.613L83.0415 142.407V130.26L86.791 123.822L89.0121 116.645V122.082L90.6059 127.87L92.3541 131.77L93.7104 123.822L95.4635 118.066L96.7553 122.082V137.548L99.7094 140.988V131.77L101.711 120.525L103.036 116.645V133.348L104.893 136.218L106.951 140.988L108.933 134.71L110.797 130.26L112.856 140.988V148.111L115.711 152.613L117.941 145.122L119.999 140.988L121.501 148.111L123.4 152.613L125.401 158.182L127.992 152.613L131.578 146.76V155.455L134.143 158.182L135.818 164.629L138.329 158.182L140.612 160.829L144.117 166.757L146.118 155.455L147.823 149.804L151.02 152.613L154.886 145.122L158.496 140.988V133.348L161.295 127.87V122.082L162.855 116.645V109.729L164.83 103.407L166.894 109.729L176.249 98.4651L178.254 106.169L180.77 98.4651V81.045L182.906 69.1641L184.8 56.8669L186.477 62.8428L187.848 79.7483L188.849 106.169L191.351 79.7483L193.485 75.645V98.4651L196.622 94.4523L198.623 87.4228V79.7483L200.717 75.645L202.276 81.045V89.3966L203.638 113.023L205.334 99.8037L207.164 94.4523L208.982 98.4651V102.176L211.267 107.64L212.788 81.045L214.437 66.0083L216.19 62.8428L217.941 56.8669V73.676V79.7483L220.28 75.645L222.516 66.0083V73.676H226.174V84.8662L228.566 98.4651L230.316 75.645L233.61 94.4523V104.25L236.882 102.176L239.543 113.023L241.057 98.4651L243.604 94.4523L244.975 106.169L245.975 87.4228L247.272 89.3966L250.732 84.8662L251.733 96.7549L254.644 94.4523L257.452 99.8037L259.853 91.3111L261.193 84.8662L264.162 75.645L265.808 87.4228L267.247 58.4895L269.757 66.0083L276.625 13.5146L273.33 58.4895L276.25 67.6563L282.377 20.1968L281.37 58.4895V66.0083L283.579 75.645L286.033 56.8669L287.436 73.676L290.628 77.6636L292.414 84.8662L294.214 61.3904L296.215 18.9623L300.826 0.947876L297.531 56.8669L299.973 62.8428L305.548 22.0598L299.755 114.956L301.907 105.378L304.192 112.688V94.9932L308.009 80.0829L310.003 94.9932L311.004 102.127L312.386 105.378L315.007 112.688L316.853 98.004L318.895 105.378L321.257 94.9932L324.349 100.81L325.032 80.0829L327.604 61.5733L329.357 74.9864L332.611 52.6565L334.352 48.5552L335.785 55.2637L338.377 59.5888V73.426L341.699 87.5181L343.843 93.4347L347.714 82.1171L350.229 78.6821L351.974 89.7556L353.323 94.9932L355.821 93.4347L357.799 102.127L360.684 108.794L363.219 98.004L365 89.7556" stroke="#F4F4F6" stroke-width="1.8"/>
                                </svg>'''),
                                cls="relative mt-2 h-fit border border-white/10 p-4 pt-6 bg-[#16161D] rounded-2xl overflow-hidden shadow-inner"
                            ),
                            cls="grid pt-2 sm:grid-cols-2 gap-6 items-center"
                        ),
                        cls="relative col-span-full overflow-hidden lg:col-span-3 rounded-3xl border border-white/10 bg-[#121217] p-6 shadow-sm hover:border-white/25 transition-all gs-scroll"
                    ),
                    
                    # Card 5: Stakeholders C-Level
                    Div(
                        Div(
                            Div(
                                Div(
                                    NotStr('''<svg class="size-6 text-white" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
                                    </svg>'''),
                                    cls="relative flex aspect-square size-12 rounded-full border border-white/10 before:absolute before:-inset-1.5 before:rounded-full before:border before:border-white/5 items-center justify-center bg-white/[0.02]"
                                ),
                                Div(
                                    H3("Adoção Executiva C-Level", cls="text-xl font-oswald uppercase tracking-tight text-white font-bold leading-[1.18]"),
                                    P("Storytelling e métricas desenhadas sob medida para diretoria, gerência e analistas de ponta.", cls="text-sm text-zinc-400 mt-1"),
                                    cls="space-y-2"
                                ),
                                cls="relative z-10 flex flex-col justify-between space-y-6"
                            ),
                            Div(
                                Div(
                                    Div(
                                        Span("Diretoria C-Level", cls="block rounded border border-white/10 bg-white/5 px-2.5 py-1 text-xs font-semibold text-zinc-200 shadow-sm"),
                                        Div("CDO", cls="size-9 rounded-full bg-white text-black flex items-center justify-center text-[10px] font-bold tracking-tight ring-2 ring-white/20 shrink-0"),
                                        cls="relative flex items-center justify-end gap-2 pr-6"
                                    ),
                                    Div(
                                        Div("BI", cls="size-9 rounded-full bg-zinc-700 text-white flex items-center justify-center text-[11px] font-bold tracking-tight ring-2 ring-white/20 shrink-0"),
                                        Span("Liderança de Analytics", cls="block rounded border border-white/10 bg-white/5 px-2.5 py-1 text-xs font-semibold text-zinc-200 shadow-sm"),
                                        cls="relative flex items-center justify-start gap-2 pl-4"
                                    ),
                                    Div(
                                        Span("Times de Negócio & Produto", cls="block rounded border border-white/10 bg-white/5 px-2.5 py-1 text-xs font-semibold text-zinc-200 shadow-sm"),
                                        Div("OPS", cls="size-9 rounded-full bg-zinc-800 text-white flex items-center justify-center text-[10px] font-bold tracking-tight ring-2 ring-white/20 shrink-0"),
                                        cls="relative flex items-center justify-end gap-2 pr-6"
                                    ),
                                    cls="relative flex h-full flex-col justify-center space-y-4 py-4"
                                ),
                                cls="relative mt-2 border-l border-white/10 sm:-my-6 sm:-mr-6 pl-4"
                            ),
                            cls="grid h-full pt-2 sm:grid-cols-2 gap-6 items-center"
                        ),
                        cls="relative col-span-full overflow-hidden lg:col-span-3 rounded-3xl border border-white/10 bg-[#121217] p-6 shadow-sm hover:border-white/25 transition-all gs-scroll"
                    ),
                    
                    cls="relative z-10 grid grid-cols-6 gap-4"
                ),
                cls="max-w-5xl mx-auto px-6 py-24"
            ),
            id="capabilities", cls="relative z-10 bg-[#0A0A0C] border-b border-white/10"
        ),

        # --- DIAGNÓSTICO DE MATURIDADE EM DADOS ---
        Diagnostico(),
        
        # --- FOOTER (Executive Monolith) ---
        Footer(
            Div(
                Div(
                    A(
                        Span("João Barbosa", cls="font-playfair italic font-bold text-3xl text-white"),
                        Span(".", cls="text-zinc-500 font-sans font-light not-italic text-3xl"),
                        href="/", 
                        cls="group inline-block"
                    ),
                    P("Arquitetura de Dados • Business Intelligence Executivo • FastHTML & SQL", cls="text-xs text-zinc-400 font-mono mt-2"),
                    cls="mb-6 md:mb-0"
                ),
                Div(
                    A("LinkedIn", href=LINKEDIN_URL, target="_blank", rel="noopener noreferrer", cls="text-xs font-mono uppercase tracking-wider text-zinc-400 hover:text-white mr-6 transition-colors"),
                    A("GitHub", href=GITHUB_URL, target="_blank", rel="noopener noreferrer", cls="text-xs font-mono uppercase tracking-wider text-zinc-400 hover:text-white mr-6 transition-colors"),
                    A("Email", href=f"mailto:{EMAIL_CONTACT}", cls="text-xs font-mono uppercase tracking-wider text-zinc-400 hover:text-white transition-colors"),
                    cls="flex items-center"
                ),
                cls="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between"
            ),
            Div(
                Div(
                    Span("© 2026 JOÃO BARBOSA. TODOS OS DIREITOS RESERVADOS.", cls="text-[11px] font-mono text-zinc-400"),
                    Span("DESENHADO PARA DECISÕES ESTRATÉGICAS C-LEVEL.", cls="text-[11px] font-mono text-zinc-400"),
                    cls="flex flex-col sm:flex-row items-center justify-between gap-4 mt-12 pt-8 border-t border-white/5"
                ),
                cls="max-w-7xl mx-auto px-6"
            ),
            cls="py-16 relative z-10 bg-[#070709] border-t border-white/10"
        ),

        # GSAP Animations com verificação de prefers-reduced-motion
        Script("""
            if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && window.gsap) {
                gsap.registerPlugin(ScrollTrigger);
                
                // Hero Entrance
                gsap.from(".gs-reveal", { y: 25, opacity: 0, duration: 1.0, stagger: 0.1, ease: "power3.out", delay: 0.1 });
                
                // Scroll animations para elementos marcados
                gsap.utils.toArray('.gs-scroll').forEach(el => {
                    gsap.from(el, {
                        scrollTrigger: {
                            trigger: el,
                            start: "top 88%",
                            toggleActions: "play none none reverse"
                        },
                        y: 30,
                        opacity: 0,
                        duration: 0.8,
                        ease: "power2.out",
                        clearProps: "transform,opacity"
                    });
                });
            }
        """)
    )

if __name__ == "__main__":
    serve()
