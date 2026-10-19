from fasthtml.common import *
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
import json
import urllib.parse
from pathlib import Path
import os
from i18n import get_content, get_diagnostico_data, CONTENT

# --- DADOS REAIS DE CONTATO ---
LINKEDIN_URL = "https://www.linkedin.com/in/joaobarbosamf"
GITHUB_URL = "https://github.com/Joao-programador"
EMAIL_CONTACT = "joaogoncalves07082022@gmail.com"

_app, rt = fast_app(
    secret_key=os.environ.get("SECRET_KEY", "joao-portfolio-secret-key-2026-spp-parcerias"),
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
        Link(rel="icon", type="image/svg+xml", href="/static/favicon.svg"),
        
        # Scripts essenciais
        Script(src="https://cdn.tailwindcss.com/3.4.17"),
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js", defer=True),
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js", defer=True),
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js", defer=True),
        Script(src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.3/dist/cdn.min.js", defer=True),

        # Dados Bilíngues dos Projetos para o Carrossel
        Script(NotStr(f"""
window.FEATURES_PT = {json.dumps(CONTENT['pt']['work']['features'], ensure_ascii=False)};
window.FEATURES_EN = {json.dumps(CONTENT['en']['work']['features'], ensure_ascii=False)};
""")),

        # Script do Carrossel Executivo 2.0 Bilíngue (Accordion + Progress + 3D Tilt + Modal Flutuante)
        Script(NotStr("""
window.featureCarousel = function() {
    const isEn = window.location.pathname.startsWith('/en');
    const feats = isEn ? window.FEATURES_EN : window.FEATURES_PT;
    return {
        currentIndex: 0,
        isPaused: false,
        isModalOpen: false,
        selectedFeature: null,
        iframeLoaded: false,
        len: feats.length,
        progress: 0,
        duration: 5000,
        rafId: null,
        lastTick: null,
        tiltX: 0,
        tiltY: 0,
        features: feats,
        get currentModalFeature() {
            return this.selectedFeature !== null ? this.features[this.selectedFeature] : null;
        },
        get modalSrc() {
            return (this.isModalOpen && this.currentModalFeature) ? encodeURI(this.currentModalFeature.iframe_src) : 'about:blank';
        },
        init() {
            const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
            if (!prefersReducedMotion) {
                this.lastTick = performance.now();
                const loop = (now) => {
                    const dt = now - this.lastTick;
                    this.lastTick = now;
                    if (!this.isPaused && !this.isModalOpen) {
                        this.progress += (dt / this.duration) * 100;
                        if (this.progress >= 100) {
                            this.progress = 0;
                            this.next();
                        }
                    }
                    this.rafId = requestAnimationFrame(loop);
                };
                this.rafId = requestAnimationFrame(loop);
            }
        },
        select(index) {
            if (this.currentIndex !== index) {
                this.currentIndex = index;
                this.progress = 0;
                this.resetTilt();
                if (window.ScrollTrigger) window.ScrollTrigger.refresh();
            }
        },
        next() {
            this.currentIndex = (this.currentIndex + 1) % this.len;
            this.progress = 0;
            this.resetTilt();
            if (window.ScrollTrigger) window.ScrollTrigger.refresh();
        },
        prev() {
            this.currentIndex = (this.currentIndex - 1 + this.len) % this.len;
            this.progress = 0;
            this.resetTilt();
            if (window.ScrollTrigger) window.ScrollTrigger.refresh();
        },
        handleMouseMove(e) {
            if (this.isModalOpen) return;
            const rect = e.currentTarget.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            this.tiltX = (y * -7).toFixed(2);
            this.tiltY = (x * 7).toFixed(2);
        },
        resetTilt() {
            this.tiltX = 0;
            this.tiltY = 0;
        },
        getCardStatus(index) {
            const diff = (index - this.currentIndex + this.len) % this.len;
            if (diff === 0) return 'active';
            if (diff === 1) return 'next';
            if (diff === this.len - 1) return 'prev';
            return 'hidden';
        },
        getCardStyle(index) {
            const status = this.getCardStatus(index);
            if (status === 'active') {
                return `position: absolute; inset: 0; transform: perspective(1200px) rotateX(${this.tiltX}deg) rotateY(${this.tiltY}deg) scale(1); opacity: 1; z-index: 30; pointer-events: auto;`;
            }
            if (status === 'next') {
                return "position: absolute; inset: 0; transform: perspective(1200px) translateY(22px) translateX(28px) scale(0.92); opacity: 0.35; z-index: 20; pointer-events: none; filter: blur(1px) brightness(0.6);";
            }
            if (status === 'prev') {
                return "position: absolute; inset: 0; transform: perspective(1200px) translateY(-22px) translateX(-28px) scale(0.88); opacity: 0.18; z-index: 10; pointer-events: none; filter: blur(2px) brightness(0.4);";
            }
            return "position: absolute; inset: 0; transform: perspective(1200px) scale(0.82); opacity: 0; z-index: 5; pointer-events: none;";
        },
        openModal(index) {
            this.iframeLoaded = false;
            this.resetTilt();
            this.selectedFeature = index;
            this.isModalOpen = true;
            document.body.style.overflow = 'hidden';
        },
        closeModal() {
            this.isModalOpen = false;
            document.body.style.overflow = 'unset';
            setTimeout(() => {
                if (!this.isModalOpen) this.selectedFeature = null;
            }, 300);
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
            }
            body { 
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
                background-color: #0A0A0C; 
                color: #F4F4F6; 
                overflow-x: clip; 
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

            @keyframes bioScan {
                0%, 100% { transform: translateY(-38px); opacity: 0.35; }
                50% { transform: translateY(38px); opacity: 1; }
            }
            .group:hover .bio-scanner-line {
                animation: bioScan 2.4s ease-in-out infinite;
            }
            @keyframes slowOrbit {
                0% { transform: rotate(0deg) scale(1); }
                50% { transform: rotate(4deg) scale(1.04); }
                100% { transform: rotate(0deg) scale(1); }
            }
            .group:hover .integrity-orbit {
                animation: slowOrbit 4s ease-in-out infinite;
                color: rgba(52, 211, 153, 0.28);
            }
            @keyframes pulseDash {
                0% { stroke-dasharray: 400; stroke-dashoffset: 400; }
                100% { stroke-dasharray: 400; stroke-dashoffset: 0; }
            }
            .group:hover .perf-line-svg {
                animation: pulseDash 1.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
                stroke: #34d399;
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
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

projetos_dir = BASE_DIR / "Projetos"
if projetos_dir.exists():
    app.mount("/Projetos", StaticFiles(directory=str(projetos_dir), html=True), name="projetos")

FEATURES = [
  {
      "id": "disponibilidade",
      "label": "Fiscalização de Concessões (DF%)",
      "tag": "GovTech & PPPs • SP Parcerias",
      "icon": '<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>',
      "image": "/static/disponibilidade-fisica-print.png",
      "iframe_src": "/Projetos/Painel de Disponibilidade Fisica/index.html",
      "description": "Centro de Controle de Concessões e PPPs (PMSP / SP Parcerias): monitoramento da Disponibilidade Física (DF%) em 21 complexos concedidos, fiscalização contratual e série temporal de 30 dias."
  },
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

def FeatureCarousel(lang="pt"):
    t = get_content(lang)
    work = t["work"]
    features = work["features"]

    # Configuração complementar visual por projeto (Backlight + URL de Cockpit)
    meta_styles = [
        {"glow": "rgba(16, 185, 129, 0.18)", "accent": "text-emerald-400", "bar": "bg-emerald-400", "path": "cco.spparcerias.gov.br/df-concessoes"},
        {"glow": "rgba(59, 130, 246, 0.16)", "accent": "text-blue-400", "bar": "bg-blue-400", "path": "analytics.spp.gov/sla-monitor"},
        {"glow": "rgba(52, 211, 153, 0.16)", "accent": "text-emerald-400", "bar": "bg-emerald-400", "path": "gis.spp.gov/sp-mobilidade"},
        {"glow": "rgba(245, 158, 11, 0.16)", "accent": "text-amber-400", "bar": "bg-amber-400", "path": "cockpit.spp.gov/sgo-executivo"},
    ]

    left_accordion_items = []
    for i, f_trans in enumerate(features):
        f = {**FEATURES[i % len(FEATURES)], **f_trans}
        m = meta_styles[i % len(meta_styles)]
        left_accordion_items.append(
            Div(
                # Cabeçalho clicável do Item
                Button(
                    Div(
                        # Índice + Ícone + Textos
                        Div(
                            Span(f"0{i + 1}",
                                 **{":class": f"`font-mono text-xs font-bold transition-colors duration-300 ${{currentIndex === {i} ? 'text-white' : 'text-zinc-600 group-hover:text-zinc-400'}}`"}),
                            Div(
                                NotStr(f['icon']),
                                **{":class": f"`p-2 rounded-xl border transition-all duration-300 ${{currentIndex === {i} ? 'bg-white text-black border-white shadow-md' : 'bg-[#16161D] text-zinc-400 border-white/10 group-hover:text-white'}}`"}
                            ),
                            Div(
                                Span(f['tag'], cls="text-[10px] font-mono uppercase tracking-widest text-zinc-400 block mb-0.5"),
                                H3(f['label'],
                                   **{":class": f"`font-bold text-sm md:text-base tracking-tight transition-colors ${{currentIndex === {i} ? 'text-white' : 'text-zinc-300 group-hover:text-white'}}`"}),
                                cls="text-left"
                            ),
                            cls="flex items-center gap-3.5"
                        ),
                        # Indicador lateral de status
                        Span(
                            "ACTIVE" if lang == "en" else "ATIVO",
                            **{"x-show": f"currentIndex === {i}"},
                            cls="hidden sm:inline-block text-[9px] font-mono font-semibold uppercase tracking-widest px-2 py-0.5 rounded bg-white/10 text-zinc-200 border border-white/10"
                        ),
                        cls="w-full flex items-center justify-between gap-2"
                    ),
                    type="button",
                    cls="w-full text-left p-4 md:p-5 cursor-pointer focus:outline-none group",
                    **{
                        "@click": f"select({i})",
                        "aria-label": f"{work['btn_explore']}: {f['label']}"
                    }
                ),

                # Corpo Expansível (Visível apenas quando este projeto está ativo)
                Div(
                    P(f['description'], cls="text-xs md:text-sm text-zinc-300 leading-relaxed mb-4"),
                    Div(
                        Button(
                            Span(work["btn_explore"]),
                            NotStr('<svg class="w-3.5 h-3.5 ml-1.5 transition-transform group-hover/btn:translate-x-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>'),
                            type="button",
                            cls="inline-flex items-center text-xs font-semibold text-black bg-white hover:bg-zinc-200 px-4 py-2 rounded-xl transition-all shadow-md cursor-pointer group/btn",
                            **{"@click.stop": f"openModal({i})"}
                        ),
                        Span(work["auditable_hint"], cls="text-[10px] font-mono text-zinc-500"),
                        cls="flex items-center justify-between gap-3 pt-1"
                    ),
                    cls="px-4 md:px-5 pb-5 pt-0 border-t border-white/5 mt-1",
                    **{
                        "x-show": f"currentIndex === {i}",
                        "x-transition:enter": "transition ease-out duration-300",
                        "x-transition:enter-start": "opacity-0 -translate-y-1",
                        "x-transition:enter-end": "opacity-100 translate-y-0"
                    }
                ),

                # Barra de Progresso do Autoplay (na base do Card Ativo)
                Div(
                    Div(
                        cls=f"h-full {m['bar']} transition-none",
                        **{":style": f"`width: ${{currentIndex === {i} ? progress : 0}}%`"}
                    ),
                    cls="h-[2px] w-full bg-white/5 overflow-hidden",
                    **{"x-show": f"currentIndex === {i}"}
                ),

                **{
                    ":class": f"`relative rounded-2xl overflow-hidden transition-all duration-300 border ${{currentIndex === {i} ? 'bg-[#14141B] border-white/25 shadow-2xl' : 'bg-[#0E0E13]/60 border-white/5 hover:border-white/15 hover:bg-[#121218]'}}`"
                }
            )
        )

    # MODAL FLUTUANTE EXECUTIVO 100% DESACOPLADO (Escala Livre de Transformações)
    modal = Div(
        # 1. Backdrop com blur
        Div(
            cls="fixed inset-0 bg-black/85 backdrop-blur-md z-[90]",
            **{
                "x-show": "isModalOpen",
                "x-transition.opacity.duration.300ms": "",
                "@click": "closeModal()",
            }
        ),
        # 2. Janela Modal Flutuante
        Div(
            Div(
                # Barra Superior do Modal
                Div(
                    Div(
                        H3(
                            cls="text-base sm:text-lg font-bold text-white tracking-tight",
                            **{"x-text": "currentModalFeature ? currentModalFeature.label : ''"}
                        ),
                        Span(
                            work["modal_hint"],
                            cls="ml-3 hidden sm:inline-block text-[10px] font-mono uppercase tracking-wider px-2.5 py-1 rounded bg-white/5 border border-white/10 text-zinc-400"
                        ),
                        cls="flex items-center"
                    ),
                    Div(
                        A(
                            Span(work["modal_new_tab"]),
                            NotStr('<svg class="w-3.5 h-3.5 ml-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>'),
                            target="_blank",
                            rel="noopener noreferrer",
                            cls="inline-flex items-center text-xs font-semibold text-white bg-white/10 hover:bg-white/20 border border-white/15 px-3 py-1.5 rounded-lg transition-colors mr-2 cursor-pointer",
                            **{":href": "currentModalFeature ? currentModalFeature.iframe_src : '#'"}
                        ),
                        Button(
                            NotStr('<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>'),
                            cls="p-1.5 bg-white/10 hover:bg-white hover:text-black text-white rounded-lg border border-white/15 transition-colors cursor-pointer",
                            aria_label=work["modal_close"],
                            **{"@click.stop": "closeModal()"}
                        ),
                        cls="flex items-center"
                    ),
                    cls="h-14 px-6 bg-[#0E0E12] border-b border-white/10 flex items-center justify-between shrink-0"
                ),
                # Conteúdo do Modal: Iframe e Loading Skeleton
                Div(
                    # Loading Skeleton
                    Div(
                        Div(
                            Span(cls="size-3 rounded-full bg-emerald-400 animate-ping"),
                            Span(work["modal_loading"], cls="text-xs font-mono text-zinc-300"),
                            cls="flex items-center gap-3 bg-[#121217] px-5 py-3 rounded-xl border border-white/10 shadow-xl"
                        ),
                        cls="absolute inset-0 flex items-center justify-center bg-[#0A0A0C] z-20 pointer-events-none",
                        **{"x-show": "!iframeLoaded", "x-transition.opacity.duration.200ms": ""}
                    ),
                    # Iframe Real
                    Iframe(
                        title="Demonstração Interativa",
                        cls="w-full h-full border-0 pointer-events-auto bg-[#0A0A0C]",
                        **{
                            ":src": "modalSrc",
                            "@load": "iframeLoaded = true"
                        }
                    ),
                    cls="relative flex-1 w-full overflow-hidden bg-[#0A0A0C]"
                ),
                cls="relative w-full h-full max-w-7xl max-h-[92vh] bg-[#121217] rounded-2xl border border-white/20 shadow-2xl flex flex-col overflow-hidden",
                **{"@click.stop": ""}
            ),
            cls="fixed inset-0 z-[100] flex items-center justify-center p-3 sm:p-6 md:p-8 pointer-events-auto",
            **{
                "x-show": "isModalOpen",
                "x-transition:enter": "transition ease-out duration-300",
                "x-transition:enter-start": "opacity-0 scale-95",
                "x-transition:enter-end": "opacity-100 scale-100",
                "x-transition:leave": "transition ease-in duration-200",
                "x-transition:leave-start": "opacity-100 scale-100",
                "x-transition:leave-end": "opacity-0 scale-95",
            }
        ),
        **{"x-show": "isModalOpen", "x-cloak": ""}
    )

    right_cards = []
    for i, f_trans in enumerate(features):
        f = {**FEATURES[i % len(FEATURES)], **f_trans}
        m = meta_styles[i % len(meta_styles)]

        # 1. Barra Superior de Janela (Window Chrome para o Preview)
        preview_window_bar = Div(
            # Bolinhas estilo macOS
            Div(
                Span(cls="size-2.5 rounded-full bg-zinc-700/80"),
                Span(cls="size-2.5 rounded-full bg-zinc-700/80"),
                Span(cls="size-2.5 rounded-full bg-zinc-700/80"),
                cls="flex items-center gap-1.5"
            ),
            # Barra de endereço simulada do Cockpit
            Div(
                NotStr('<svg class="w-3 h-3 text-zinc-500 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>'),
                Span(m["path"], cls="text-[10px] font-mono text-zinc-400 truncate"),
                cls="hidden sm:flex items-center bg-[#0A0A0E] px-3 py-1 rounded-md border border-white/5 max-w-[240px]"
            ),
            # Badge de Demonstração Interativa alojada na barra superior
            Div(
                Span(cls="size-1.5 rounded-full bg-emerald-400 animate-pulse"),
                Span(work["badge_interactive"], cls="text-[10px] font-mono font-medium text-zinc-200 tracking-wide"),
                cls="flex items-center gap-1.5 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-0.5 rounded-full"
            ),
            cls="h-9 px-4 bg-[#14141B] border-b border-white/10 flex items-center justify-between shrink-0 z-[35]"
        )

        # 2. Imagem 100% limpa e visível
        image_cover = Img(
            src=f['image'],
            alt=f['label'],
            width="640",
            height="400",
            loading="lazy",
            decoding="async",
            cls="absolute inset-0 w-full h-full object-cover object-top z-[30] bg-[#121217] transition-transform duration-700 group-hover/card:scale-[1.02]"
        )

        # 3. Pílula Flutuante Sutil no Hover ("Clique para Interagir")
        hover_cta_overlay = Div(
            Div(
                NotStr('<svg class="w-4 h-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"/></svg>'),
                Span(work["interactive_hint"], cls="text-xs font-semibold text-white tracking-tight"),
                cls="flex items-center gap-2 bg-[#0A0A0E]/90 backdrop-blur-md border border-white/20 px-4 py-2.5 rounded-full shadow-2xl transform translate-y-2 opacity-0 group-hover/card:translate-y-0 group-hover/card:opacity-100 transition-all duration-300"
            ),
            cls="absolute inset-0 z-[40] flex items-center justify-center bg-black/0 group-hover/card:bg-black/25 transition-colors duration-300 pointer-events-none",
            **{"x-show": f"!isModalOpen && currentIndex === {i}"}
        )

        right_cards.append(
            Div(
                preview_window_bar,
                Div(
                    image_cover,
                    hover_cta_overlay,
                    cls="relative flex-1 w-full overflow-hidden"
                ),
                # Botão invisível de captura de clique acessível via teclado
                Button(
                    cls="absolute inset-0 z-[50] cursor-pointer opacity-0 w-full h-full border-0 focus-visible:opacity-100 focus-visible:ring-2 focus-visible:ring-white rounded-2xl outline-none",
                    aria_label=f"{work['btn_explore']}: {f['label']}",
                    **{
                        "@click": f"if ({i} === currentIndex) openModal({i})"
                    }
                ),
                cls="rounded-2xl overflow-hidden border border-white/15 bg-[#121217] flex flex-col transition-all duration-500 ease-out shadow-[0_25px_70px_rgba(0,0,0,0.75)] group/card",
                **{
                    ":style": f"getCardStyle({i})",
                    "@mousemove": f"if (currentIndex === {i}) handleMouseMove($event)",
                    "@mouseleave": "resetTilt()"
                }
            )
        )

    return Div(
        modal,
        Div(
            # COLUNA ESQUERDA: Accordion Inteligente + Controles
            Div(
                Div(
                    Span(work["select_case"], cls="text-[10px] font-mono uppercase tracking-[0.2em] text-zinc-500 block mb-4"),
                    Div(*left_accordion_items, cls="space-y-3"),
                    cls="w-full"
                ),
                # Rodapé da Coluna Esquerda: Navegação Manual + Status de Autoplay
                Div(
                    Div(
                        Button(
                            NotStr('<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>'),
                            type="button",
                            cls="w-9 h-9 rounded-xl bg-[#14141B] border border-white/10 text-zinc-300 hover:text-white hover:border-white/30 flex items-center justify-center transition-all cursor-pointer",
                            **{"@click": "prev()", "aria-label": "Previous project" if lang == "en" else "Projeto anterior"}
                        ),
                        Span(
                            cls="text-xs font-mono text-zinc-400 px-3",
                            **{"x-text": "`0${currentIndex + 1} / 0${len}`"}
                        ),
                        Button(
                            NotStr('<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>'),
                            type="button",
                            cls="w-9 h-9 rounded-xl bg-[#14141B] border border-white/10 text-zinc-300 hover:text-white hover:border-white/30 flex items-center justify-center transition-all cursor-pointer",
                            **{"@click": "next()", "aria-label": "Next project" if lang == "en" else "Próximo projeto"}
                        ),
                        cls="flex items-center gap-1"
                    ),
                    Span(
                        **{"x-text": f"isPaused ? ('{('⏸ PAUSED' if lang == 'en' else '⏸ PAUSADO')}') : ('{('▶ AUTO-CYCLE' if lang == 'en' else '▶ AUTO-CICLO')}')"},
                        cls="text-[10px] font-mono tracking-widest text-zinc-500 uppercase"
                    ),
                    cls="w-full flex items-center justify-between pt-6 mt-6 border-t border-white/10"
                ),
                cls="w-full lg:w-[42%] p-6 sm:p-8 lg:p-10 flex flex-col justify-between bg-[#0A0A0C] z-30"
            ),

            # COLUNA DIREITA: Palco de Exibição com Backlight Dinâmico e 3D Tilt
            Div(
                # Luz Ambiental Dinâmica no fundo (Muda de cor conforme o projeto ativo)
                Div(
                    cls="absolute inset-0 pointer-events-none transition-all duration-700 opacity-90",
                    **{
                        ":style": "`background: radial-gradient(circle at 55% 50%, ${currentIndex === 0 ? 'rgba(59,130,246,0.16)' : currentIndex === 1 ? 'rgba(52,211,153,0.16)' : 'rgba(245,158,11,0.16)'}, transparent 68%);`"
                    }
                ),
                # Grade de Fundo Sutil de Engenharia
                Div(cls="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.025)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.025)_1px,transparent_1px)] bg-[size:32px_32px] pointer-events-none"),

                # Container dos Cards Empilhados em Perspectiva
                Div(
                    *right_cards,
                    cls="relative w-full max-w-[640px] aspect-[16/10] flex items-center justify-center z-20"
                ),

                cls="flex-1 min-h-[380px] sm:min-h-[480px] lg:min-h-[560px] relative bg-[#0D0D12] flex items-center justify-center p-6 sm:p-10 lg:p-14 overflow-hidden border-t lg:border-t-0 lg:border-l border-white/10"
            ),

            cls="relative overflow-hidden rounded-[2rem] flex flex-col lg:flex-row border border-white/15 shadow-2xl bg-[#0A0A0C]"
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
    const isEn = window.location.pathname.startsWith('/en');
    const assunto = isEn 
      ? 'Data Maturity Assessment: ' + this.nivel.titulo
      : 'Diagnóstico de Maturidade em Dados: ' + this.nivel.titulo;
    const corpo = isEn
      ? `Hello João,\\n\\nI completed the data maturity assessment on your portfolio:\\n- Score: ${{this.pontos}} / ${{this.dados.max}}\\n- Diagnosed Stage: ${{this.nivel.titulo}}\\n\\nI would like to discuss analytics strategy and next steps for our operation.`
      : `Olá João,\\n\\nRealizei o diagnóstico de maturidade no seu portfólio:\\n- Pontuação: ${{this.pontos}} / ${{this.dados.max}}\\n- Nível Diagnosticado: ${{this.nivel.titulo}}\\n\\nGostaria de conversar sobre estratégias e próximos passos analíticos para nossa operação.`;
    return 'mailto:{EMAIL_CONTACT}?subject=' + encodeURIComponent(assunto)
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

def AboutSection(lang="pt"):
    t = get_content(lang)
    about = t["about"]
    pillars = about["pillars"]

    pillar_cards = []
    for p in pillars:
        pillar_cards.append(
            Div(
                Span(p["num"], cls="text-xs font-mono font-bold text-zinc-400 block mb-1.5"),
                H5(p["title"], cls="text-base font-bold text-white mb-1"),
                P(p["desc"], cls="text-xs text-zinc-400 leading-relaxed"),
                cls="p-5 rounded-2xl bg-[#141419] border border-white/10 hover:border-white/30 transition-colors"
            )
        )

    return Section(
        Div(
            Div(
                # Coluna Esquerda
                Div(
                    Span(about["tag"], cls="text-[11px] font-mono font-semibold tracking-[0.25em] text-zinc-400 uppercase block mb-3"),
                    H2(about["h2"], 
                       cls="text-3xl md:text-4xl lg:text-[40px] font-oswald uppercase tracking-tight text-white leading-[1.18] mb-6"),
                    P(about["lead"], 
                       cls="font-playfair italic text-xl md:text-2xl text-zinc-300 leading-snug mb-8"),
                    
                    # Card Institucional SPP
                    Div(
                        Div(
                            Span(cls="size-2 rounded-full bg-emerald-400"),
                            Span(about["spp_badge"], cls="text-[10px] font-mono font-semibold tracking-widest text-emerald-400 uppercase"),
                            cls="flex items-center gap-2 mb-2"
                        ),
                        H4(about["spp_title"], cls="text-lg font-bold text-white"),
                        P(about["spp_desc"], 
                          cls="text-xs text-zinc-400 mt-1.5 leading-relaxed"),
                        cls="p-6 rounded-2xl bg-[#141419] border border-white/10 shadow-lg mt-auto"
                    ),
                    cls="lg:col-span-5 flex flex-col justify-between h-full gs-scroll"
                ),
                
                # Coluna Direita
                Div(
                    Div(
                        P(about["p1"],
                          cls="text-base md:text-lg text-zinc-200 leading-relaxed mb-6 font-medium"),
                        P(about["p2"],
                          cls="text-base md:text-lg text-zinc-400 leading-relaxed mb-10"),
                        cls="mb-4"
                    ),
                    
                    # 3 Microcards de Pilares
                    Div(
                        *pillar_cards,
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

def DataJourney3DSection(lang="pt"):
    t = get_content(lang)
    phil = t["philosophy"]

    three_js_script = """
    window.addEventListener('DOMContentLoaded', () => {
        if (typeof THREE === 'undefined' || typeof gsap === 'undefined') return;
        gsap.registerPlugin(ScrollTrigger);

        const container = document.getElementById('data-3d-canvas');
        const tooltip = document.getElementById('node-3d-tooltip');
        const ttId = document.getElementById('tt-node-id');
        const ttKpi = document.getElementById('tt-node-kpi');
        const ttMeta = document.getElementById('tt-node-meta');
        if (!container) return;

        const isEn = window.location.pathname.startsWith('/en');
        const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        // 1. CENA, CÂMERA E RENDERER (Dark Mode #0A0A0C)
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0A0A0C);
        scene.fog = new THREE.FogExp2(0x0A0A0C, 0.018);

        const camera = new THREE.PerspectiveCamera(40, container.clientWidth / container.clientHeight, 0.1, 150);
        camera.position.set(0, 26, 5);
        camera.lookAt(0, 0, 0);

        const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.appendChild(renderer.domElement);

        // 2. ILUMINAÇÃO EXECUTIVA DE ESTÚDIO
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.55);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xf4f4f6, 1.15);
        dirLight.position.set(16, 30, 20);
        dirLight.castShadow = true;
        dirLight.shadow.mapSize.width = 1024;
        dirLight.shadow.mapSize.height = 1024;
        const d = 16;
        dirLight.shadow.camera.left = -d;
        dirLight.shadow.camera.right = d;
        dirLight.shadow.camera.top = d;
        dirLight.shadow.camera.bottom = -d;
        scene.add(dirLight);

        const emeraldLight = new THREE.PointLight(0x34d399, 0.9, 32);
        emeraldLight.position.set(-8, 8, 8);
        scene.add(emeraldLight);

        // 3. PLATAFORMA BASE (#121217 com Grid Sutil)
        const boardGroup = new THREE.Group();
        scene.add(boardGroup);

        const baseGeo = new THREE.BoxGeometry(17.5, 0.5, 11.5);
        const baseMat = new THREE.MeshStandardMaterial({ color: 0x121217, roughness: 0.7, metalness: 0.2 });
        const baseMesh = new THREE.Mesh(baseGeo, baseMat);
        baseMesh.position.y = -0.3;
        baseMesh.receiveShadow = true;
        boardGroup.add(baseMesh);

        const gridHelper = new THREE.GridHelper(17, 16, 0x27272a, 0x18181b);
        gridHelper.position.y = -0.03;
        gridHelper.scale.z = 11.5 / 17;
        boardGroup.add(gridHelper);

        // 4. INSTANCED MESH (480 Nós de Dados)
        const COLS = 10, ROWS = 6, MAX_STACK = 11, TOTAL = 480;
        const cubeGeo = new THREE.BoxGeometry(0.8, 0.4, 0.8);
        const cubeMat = new THREE.MeshStandardMaterial({ roughness: 0.22, metalness: 0.25 });
        const instancedData = new THREE.InstancedMesh(cubeGeo, cubeMat, TOTAL);
        instancedData.castShadow = true;
        instancedData.receiveShadow = true;
        boardGroup.add(instancedData);

        const palette = [
            new THREE.Color(0x27272a), // Zinc-800
            new THREE.Color(0x52525b), // Zinc-600
            new THREE.Color(0xa1a1aa), // Zinc-400
            new THREE.Color(0xf4f4f6), // Branco Puro
            new THREE.Color(0x34d399)  // Emerald-400 (KPI Destaque)
        ];

        const chaosState = [];
        const currentInsight = [];
        const targetInsight = [];
        const nodeMetadata = [];
        const dummy = new THREE.Object3D();
        let currentMode = 'olap'; // 'olap' | 'star' | 'gauss'

        const kpiLabels = isEn ? [
            "PUBLIC CONCESSION SLA", "FLOW AUDIT", "CAPEX/OPEX MODEL",
            "SP MOBILITY INDEX", "CONCESSION FEE REVENUE", "SGO EFFICIENCY"
        ] : [
            "SLA CONCESSÃO PÚBLICA", "AUDITORIA DE FLUXO", "MODELO CAPEX/OPEX",
            "ÍNDICE DE MOBILIDADE SP", "RECEITA DE OUTORGA", "EFICIÊNCIA SGO"
        ];

        // Inicializar estado de Caos uma única vez + Metadados para o Tooltip
        for (let i = 0; i < TOTAL; i++) {
            const angle = Math.random() * Math.PI * 2;
            const radius = 2 + Math.random() * 13;
            chaosState.push({
                x: Math.cos(angle) * radius,
                y: 3.5 + Math.random() * 13,
                z: Math.sin(angle) * (radius * 0.75),
                rx: (Math.random() - 0.5) * Math.PI * 2,
                ry: (Math.random() - 0.5) * Math.PI * 2,
                rz: (Math.random() - 0.5) * Math.PI * 2,
                phase: Math.random() * Math.PI * 2,
                speed: 0.5 + Math.random() * 1.0
            });
            currentInsight.push({ x: 0, y: 0, z: 0 });
            targetInsight.push({ x: 0, y: 0, z: 0 });
            nodeMetadata.push({
                id: `NODE_${String(i + 1).padStart(3, '0')}`,
                kpi: kpiLabels[i % kpiLabels.length],
                val: `${(92 + Math.random() * 7.9).toFixed(1)}%`,
                lat: `${Math.floor(2 + Math.random() * 9)}ms`
            });
        }

        function computeTopology(mode) {
            currentMode = mode;
            let idx = 0;

            if (mode === 'olap') {
                // MODO 1: Matriz Dimensional OLAP (Barras Executivas)
                const spX = 1.42, spZ = 1.42;
                const stX = -((COLS - 1) * spX) / 2;
                const stZ = -((ROWS - 1) * spZ) / 2;
                const heights = [];

                for (let c = 0; c < COLS; c++) {
                    heights[c] = [];
                    for (let r = 0; r < ROWS; r++) {
                        const trend = (c / COLS) * 5.5;
                        heights[c][r] = Math.max(1, Math.min(MAX_STACK, Math.floor(Math.random() * 6 + trend + 1)));
                    }
                }

                for (let c = 0; c < COLS; c++) {
                    for (let r = 0; r < ROWS; r++) {
                        const h = heights[c][r];
                        for (let s = 0; s < h; s++) {
                            if (idx >= TOTAL) break;
                            targetInsight[idx] = { x: stX + c * spX, y: 0.22 + s * 0.44, z: stZ + r * spZ };
                            let cIdx = 0;
                            if (h >= 9 && s === h - 1) cIdx = 4;
                            else if (h >= 7) cIdx = 3;
                            else if (h >= 5) cIdx = 2;
                            else if (h >= 3) cIdx = 1;
                            instancedData.setColorAt(idx, palette[cIdx]);
                            idx++;
                        }
                    }
                }
                while (idx < TOTAL) {
                    const c = idx % COLS;
                    const r = Math.floor(idx / COLS) % ROWS;
                    const s = heights[c][r]++;
                    targetInsight[idx] = { x: stX + c * spX, y: 0.22 + s * 0.44, z: stZ + r * spZ };
                    instancedData.setColorAt(idx, palette[2]);
                    idx++;
                }
            } else if (mode === 'star') {
                // MODO 2: Star Schema Relacional (1 Tabela Fato Central + 6 Tabelas Dimensão Satélites)
                const factCols = 5, factRows = 5;
                for (let i = 0; i < 180; i++) {
                    const c = i % factCols;
                    const r = Math.floor(i / factCols) % factRows;
                    const s = Math.floor(i / (factCols * factRows));
                    targetInsight[idx] = {
                        x: (c - 2) * 0.88,
                        y: 0.22 + s * 0.44,
                        z: (r - 2) * 0.88
                    };
                    instancedData.setColorAt(idx, s >= 6 ? palette[4] : palette[3]);
                    idx++;
                }
                const satellites = 6;
                const radius = 5.4;
                for (let sat = 0; sat < satellites; sat++) {
                    const angle = (sat / satellites) * Math.PI * 2;
                    const cx = Math.cos(angle) * radius;
                    const cz = Math.sin(angle) * (radius * 0.72);
                    for (let j = 0; j < 50; j++) {
                        if (idx >= TOTAL) break;
                        const sc = j % 3;
                        const sr = Math.floor(j / 3) % 3;
                        const ss = Math.floor(j / 9);
                        targetInsight[idx] = {
                            x: cx + (sc - 1) * 0.85,
                            y: 0.22 + ss * 0.44,
                            z: cz + (sr - 1) * 0.85
                        };
                        instancedData.setColorAt(idx, ss >= 4 ? palette[4] : palette[2]);
                        idx++;
                    }
                }
            } else if (mode === 'gauss') {
                // MODO 3: Distribuição Normal / Superfície Gaussiana 3D
                const gCols = 12, gRows = 8;
                const spX = 1.25, spZ = 1.22;
                const stX = -((gCols - 1) * spX) / 2;
                const stZ = -((gRows - 1) * spZ) / 2;

                for (let c = 0; c < gCols; c++) {
                    for (let r = 0; r < gRows; r++) {
                        const dx = (c - (gCols - 1) / 2) / 3.2;
                        const dz = (r - (gRows - 1) / 2) / 2.2;
                        const bell = Math.exp(-(dx * dx + dz * dz));
                        const h = Math.max(1, Math.round(bell * 11));
                        for (let s = 0; s < h; s++) {
                            if (idx >= TOTAL) break;
                            targetInsight[idx] = {
                                x: stX + c * spX,
                                y: 0.22 + s * 0.44,
                                z: stZ + r * spZ
                            };
                            let cIdx = 1;
                            if (h >= 9 && s === h - 1) cIdx = 4;
                            else if (h >= 7) cIdx = 3;
                            else if (h >= 4) cIdx = 2;
                            instancedData.setColorAt(idx, palette[cIdx]);
                            idx++;
                        }
                    }
                }
                while (idx < TOTAL) {
                    const ring = idx % gCols;
                    targetInsight[idx] = {
                        x: stX + ring * spX,
                        y: 0.22,
                        z: stZ + (idx % gRows) * spZ
                    };
                    instancedData.setColorAt(idx, palette[0]);
                    idx++;
                }
            }

            instancedData.instanceColor.needsUpdate = true;
        }

        // Inicializar na topologia OLAP
        computeTopology('olap');
        for (let i = 0; i < TOTAL; i++) {
            currentInsight[i].x = targetInsight[i].x;
            currentInsight[i].y = targetInsight[i].y;
            currentInsight[i].z = targetInsight[i].z;
        }

        // Função para alternar Topologia com transição suave
        function switchTopology(mode) {
            computeTopology(mode);
            for (let i = 0; i < TOTAL; i++) {
                gsap.to(currentInsight[i], {
                    x: targetInsight[i].x,
                    y: targetInsight[i].y,
                    z: targetInsight[i].z,
                    duration: 0.85,
                    ease: "power3.inOut"
                });
            }
            gsap.fromTo(boardGroup.rotation, { y: boardGroup.rotation.y - 0.22 }, { y: boardGroup.rotation.y, duration: 0.8, ease: "back.out(1.7)" });

            document.querySelectorAll('.topo-btn').forEach(btn => {
                if (btn.dataset.topo === mode) {
                    btn.className = "topo-btn font-mono text-[10px] sm:text-xs tracking-wider bg-white text-black font-semibold px-3.5 py-2 rounded-xl transition-all cursor-pointer shadow-md";
                } else {
                    btn.className = "topo-btn font-mono text-[10px] sm:text-xs tracking-wider text-zinc-300 hover:text-white bg-[#121217]/90 border border-white/10 px-3.5 py-2 rounded-xl transition-all cursor-pointer";
                }
            });
        }

        document.querySelectorAll('.topo-btn').forEach(btn => {
            btn.addEventListener('click', () => switchTopology(btn.dataset.topo));
        });

        // 5. SCROLLTRIGGER ATRELADO AO TRACK #philosophy-scroll-track
        const state = {
            progress: reducedMotion ? 1 : 0,
            camX: 0,
            camY: reducedMotion ? 9.2 : 26,
            camZ: reducedMotion ? 20.5 : 5,
            lookY: reducedMotion ? 1.8 : 3.5
        };

        const stageBadge = document.getElementById('stage-3d-badge');
        const stageMetric = document.getElementById('stage-3d-metric');

        if (!reducedMotion) {
            const tl = gsap.timeline({
                scrollTrigger: {
                    trigger: "#philosophy-scroll-track",
                    start: "top top",
                    end: "bottom bottom",
                    scrub: 0.6,
                    onUpdate: (self) => {
                        const p = self.progress;
                        if (!stageBadge || !stageMetric) return;
                        if (p < 0.3) {
                            stageBadge.textContent = isEn 
                                ? "01 // DISPERSED DATA & OPERATIONAL CHAOS" 
                                : "01 // BASES DISPERSAS & CAOS OPERACIONAL";
                            stageMetric.textContent = isEn 
                                ? `Entropy: ${(98.4 - p * 110).toFixed(1)}% • Spreadsheets & Isolated Silos`
                                : `Entropia: ${(98.4 - p * 110).toFixed(1)}% • Planilhas & Sistemas Isolados`;
                        } else if (p < 0.72) {
                            stageBadge.textContent = isEn 
                                ? "02 // PYTHON PIPELINES & SQL STAR SCHEMA" 
                                : "02 // PIPELINE PYTHON & STAR SCHEMA SQL";
                            stageMetric.textContent = isEn 
                                ? `Modeling & Validation: ${Math.min(99, Math.floor(p * 130))}% • Anomaly Resolution`
                                : `Modelagem & Validação: ${Math.min(99, Math.floor(p * 130))}% • Tratamento de Anomalias`;
                        } else {
                            stageBadge.textContent = isEn 
                                ? "03 // C-LEVEL EXECUTIVE COCKPIT" 
                                : "03 // COCKPIT EXECUTIVO C-LEVEL";
                            stageMetric.textContent = isEn 
                                ? "Auditable Consistency • Hover blocks to inspect"
                                : "Consistência Auditável • Passe o mouse nos blocos para inspecionar";
                        }
                    }
                }
            });

            tl.to(state, {
                progress: 1,
                camX: 0,
                camY: 9.2,
                camZ: 20.5,
                lookY: 1.8,
                ease: "none"
            });
        }

        // 6. RAYCASTER PARA INSPEÇÃO TÁTIL DE NÓS 3D + TOOLTIP HUD
        const raycaster = new THREE.Raycaster();
        const mouseNDC = new THREE.Vector2(-999, -999);
        let mouseX = 0, mouseY = 0;
        let hoveredInstance = -1;

        window.addEventListener('mousemove', (e) => {
            mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
            mouseY = (e.clientY / window.innerHeight - 0.5) * 2;

            const rect = container.getBoundingClientRect();
            if (e.clientY >= rect.top && e.clientY <= rect.bottom) {
                mouseNDC.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
                mouseNDC.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
                if (tooltip) {
                    tooltip.style.left = `${e.clientX + 18}px`;
                    tooltip.style.top = `${e.clientY - 18}px`;
                }
            } else {
                mouseNDC.set(-999, -999);
            }
        });

        let isVisible = true;
        const observer = new IntersectionObserver((entries) => {
            isVisible = entries[0].isIntersecting;
        }, { threshold: 0.01 });
        observer.observe(container);

        const clock = new THREE.Clock();
        function animate() {
            requestAnimationFrame(animate);
            if (!isVisible) return;

            const elapsed = clock.getElapsedTime();
            const t = state.progress;
            const chaosFactor = 1 - t;

            if (mouseNDC.x !== -999 && t > 0.45) {
                raycaster.setFromCamera(mouseNDC, camera);
                const hits = raycaster.intersectObject(instancedData);
                if (hits.length > 0 && hits[0].instanceId !== undefined) {
                    hoveredInstance = hits[0].instanceId;
                    const meta = nodeMetadata[hoveredInstance];
                    if (tooltip && ttId && ttKpi && ttMeta) {
                        ttId.textContent = meta.id;
                        ttKpi.textContent = meta.kpi;
                        ttMeta.textContent = isEn 
                            ? `COMPLIANCE: ${meta.val} • QUERY: ${meta.lat}`
                            : `CONFORMIDADE: ${meta.val} • QUERY: ${meta.lat}`;
                        tooltip.style.opacity = '1';
                    }
                } else {
                    hoveredInstance = -1;
                    if (tooltip) tooltip.style.opacity = '0';
                }
            } else {
                hoveredInstance = -1;
                if (tooltip) tooltip.style.opacity = '0';
            }

            for (let i = 0; i < TOTAL; i++) {
                const c = chaosState[i];
                const ins = currentInsight[i];

                const fx = Math.sin(elapsed * c.speed + c.phase) * 0.45 * chaosFactor;
                const fy = Math.cos(elapsed * c.speed + c.phase) * 0.45 * chaosFactor;
                const fz = Math.sin(elapsed * 0.7 * c.speed + c.phase) * 0.45 * chaosFactor;

                const hoverLift = (i === hoveredInstance) ? 0.32 : 0;
                const hoverScale = (i === hoveredInstance) ? 1.16 : 1.0;

                dummy.position.set(
                    THREE.MathUtils.lerp(c.x, ins.x, t) + fx,
                    THREE.MathUtils.lerp(c.y, ins.y, t) + fy + hoverLift,
                    THREE.MathUtils.lerp(c.z, ins.z, t) + fz
                );
                dummy.rotation.set(
                    THREE.MathUtils.lerp(c.rx + elapsed * 0.25, 0, t),
                    THREE.MathUtils.lerp(c.ry + elapsed * 0.35, 0, t),
                    THREE.MathUtils.lerp(c.rz, 0, t)
                );
                dummy.scale.set(hoverScale, hoverScale, hoverScale);
                dummy.updateMatrix();
                instancedData.setMatrixAt(i, dummy.matrix);
            }
            instancedData.instanceMatrix.needsUpdate = true;

            camera.position.x = state.camX + mouseX * 1.5;
            camera.position.y = state.camY - mouseY * 0.9;
            camera.position.z = state.camZ;
            camera.lookAt(0, state.lookY, 0);

            boardGroup.rotation.y = THREE.MathUtils.lerp(boardGroup.rotation.y, mouseX * 0.15, 0.05);
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
            if (window.ScrollTrigger) window.ScrollTrigger.refresh();
        });

        window.addEventListener('load', () => {
            if (window.ScrollTrigger) window.ScrollTrigger.refresh();
        });
    });
    """

    cards = phil["cards"]
    c1, c2, c3 = cards[0], cards[1], cards[2]

    return Section(
        # Tooltip Flutuante de Inspeção Tátil 3D (Raycaster HUD)
        Div(
            Div(
                Span(cls="size-1.5 rounded-full bg-emerald-400"),
                Span("NODE_001", id="tt-node-id", cls="text-[10px] font-mono font-bold text-emerald-400 tracking-wider"),
                cls="flex items-center gap-1.5 mb-0.5"
            ),
            Div(phil["tt_kpi_label"], id="tt-node-kpi", cls="text-xs font-bold text-white tracking-tight"),
            Div(f"{phil['tt_conf_label']}: 99.4% • QUERY: 4ms", id="tt-node-meta", cls="text-[10px] font-mono text-zinc-400 mt-0.5"),
            id="node-3d-tooltip",
            cls="fixed z-50 pointer-events-none opacity-0 transition-opacity duration-150 bg-[#0A0A0E]/95 backdrop-blur-md border border-emerald-500/30 px-3.5 py-2.5 rounded-xl shadow-2xl"
        ),

        # Track de Scroll (250vh) onde a câmera 3D viaja do Caos ao Insight
        Div(
            Div(
                Div(id="data-3d-canvas", cls="absolute inset-0 w-full h-full z-0"),

                # Header Editorial do Palco 3D
                Div(
                    Span(phil["tag"], cls="text-[11px] font-mono uppercase tracking-[0.25em] text-emerald-400 block mb-2"),
                    H2(phil["h2_line1"], Br(), Span(phil["h2_line2"], cls="font-playfair italic text-zinc-300 font-normal"),
                       cls="text-3xl sm:text-5xl font-oswald uppercase tracking-tight text-white leading-[1.1]"),
                    cls="relative z-10 pt-24 px-6 max-w-7xl mx-auto w-full pointer-events-none"
                ),

                # HUD Inferior: Telemetria do Pipeline + Seletor de 3 Topologias Matemáticas
                Div(
                    Div(
                        Div(
                            Span(cls="size-2 rounded-full bg-emerald-400 animate-pulse"),
                            Span(phil["stage_intro"], id="stage-3d-badge", cls="text-xs font-mono font-semibold text-white tracking-wider"),
                            cls="flex items-center gap-2.5 mb-1"
                        ),
                        P(phil["stage_metric_1"], id="stage-3d-metric", cls="text-xs font-mono text-zinc-400"),
                        cls="glass-pill px-5 py-3.5 rounded-2xl border border-white/10"
                    ),
                    # Seletor Multi-Topologia (OLAP | Star Schema | Gaussiana)
                    Div(
                        Span("TOPOLOGY:" if lang == "en" else "TOPOLOGIA:", cls="hidden md:inline-block text-[10px] font-mono text-zinc-400 uppercase tracking-widest mr-1"),
                        Button(
                            phil["mode_olap"],
                            type="button",
                            data_topo="olap",
                            cls="topo-btn font-mono text-[10px] sm:text-xs tracking-wider bg-white text-black font-semibold px-3.5 py-2 rounded-xl transition-all cursor-pointer shadow-md"
                        ),
                        Button(
                            phil["mode_star"],
                            type="button",
                            data_topo="star",
                            cls="topo-btn font-mono text-[10px] sm:text-xs tracking-wider text-zinc-300 hover:text-white bg-[#121217]/90 border border-white/10 px-3.5 py-2 rounded-xl transition-all cursor-pointer"
                        ),
                        Button(
                            phil["mode_gauss"],
                            type="button",
                            data_topo="gauss",
                            cls="topo-btn font-mono text-[10px] sm:text-xs tracking-wider text-zinc-300 hover:text-white bg-[#121217]/90 border border-white/10 px-3.5 py-2 rounded-xl transition-all cursor-pointer"
                        ),
                        cls="flex flex-wrap items-center gap-2 pointer-events-auto glass-pill p-2 rounded-2xl border border-white/10"
                    ),
                    cls="relative z-10 pb-10 px-6 max-w-7xl mx-auto w-full flex flex-col lg:flex-row items-start lg:items-end justify-between gap-4 pointer-events-none"
                ),

                id="data-3d-stage",
                cls="sticky top-0 w-full h-screen overflow-hidden flex flex-col justify-between"
            ),
            id="philosophy-scroll-track",
            cls="relative w-full h-[250vh]"
        ),

        # Bloco de Filosofia que desliza por cima do palco 3D ao final do scroll
        Div(
            Div(
                H2(phil["h2_sub1"], Br(), Span(phil["h2_sub2"], cls="font-playfair italic text-zinc-400 font-normal"), cls="text-4xl sm:text-6xl font-bold tracking-tight text-white text-center mb-6 gs-scroll leading-[1.18]"),
                P(phil["p_sub"], cls="text-center text-zinc-400 max-w-2xl mx-auto mb-16 text-base sm:text-lg gs-scroll"),
                Div(
                    # Card 1
                    Div(
                        Div(
                            Span(c1["tag"], cls="text-[11px] font-mono font-bold tracking-widest text-zinc-400 uppercase"),
                            Span("01", cls="text-4xl font-oswald text-zinc-600 group-hover:text-white transition-colors duration-300"),
                            cls="flex items-center justify-between"
                        ),
                        Div(
                            H4(c1["title"], cls="text-2xl font-oswald uppercase tracking-tight text-white mt-6 mb-3 leading-[1.18]"),
                            P(c1["desc"], cls="text-sm text-zinc-400 leading-relaxed"),
                        ),
                        Div(
                            Span(cls="size-2 rounded-full bg-blue-400 mr-2.5"),
                            Span(c1["footer"], cls="text-xs font-semibold text-zinc-300"),
                            cls="flex items-center pt-6 mt-6 border-t border-white/10"
                        ),
                        cls="bg-[#121217] rounded-[28px] p-8 md:p-10 border border-white/10 hover:border-white/30 transition-all duration-300 relative group flex flex-col justify-between gs-scroll"
                    ),
                    # Card 2
                    Div(
                        Div(
                            Span(c2["tag"], cls="text-[11px] font-mono font-bold tracking-widest text-zinc-400 uppercase"),
                            Span("02", cls="text-4xl font-oswald text-zinc-600 group-hover:text-white transition-colors duration-300"),
                            cls="flex items-center justify-between"
                        ),
                        Div(
                            H4(c2["title"], cls="text-2xl font-oswald uppercase tracking-tight text-white mt-6 mb-3 leading-[1.18]"),
                            P(c2["desc"], cls="text-sm text-zinc-400 leading-relaxed"),
                        ),
                        Div(
                            Span(cls="size-2 rounded-full bg-emerald-400 mr-2.5"),
                            Span(c2["footer"], cls="text-xs font-semibold text-zinc-300"),
                            cls="flex items-center pt-6 mt-6 border-t border-white/10"
                        ),
                        cls="bg-[#121217] rounded-[28px] p-8 md:p-10 border border-white/10 hover:border-white/30 transition-all duration-300 relative group flex flex-col justify-between gs-scroll"
                    ),
                    # Card 3
                    Div(
                        Div(
                            Span(c3["tag"], cls="text-[11px] font-mono font-bold tracking-widest text-zinc-400 uppercase"),
                            Span("03", cls="text-4xl font-oswald text-zinc-600 group-hover:text-white transition-colors duration-300"),
                            cls="flex items-center justify-between"
                        ),
                        Div(
                            H4(c3["title"], cls="text-2xl font-oswald uppercase tracking-tight text-white mt-6 mb-3 leading-[1.18]"),
                            P(c3["desc"], cls="text-sm text-zinc-400 leading-relaxed"),
                        ),
                        Div(
                            Span(cls="size-2 rounded-full bg-amber-400 mr-2.5"),
                            Span(c3["footer"], cls="text-xs font-semibold text-zinc-300"),
                            cls="flex items-center pt-6 mt-6 border-t border-white/10"
                        ),
                        cls="bg-[#121217] rounded-[28px] p-8 md:p-10 border border-white/10 hover:border-white/30 transition-all duration-300 relative group flex flex-col justify-between gs-scroll"
                    ),
                    cls="grid grid-cols-1 md:grid-cols-3 gap-8"
                ),
                cls="max-w-6xl mx-auto px-6 py-24"
            ),
            cls="relative z-20 bg-[#0E0E12] border-t border-white/15 shadow-[0_-30px_60px_rgba(0,0,0,0.85)] rounded-t-[2.5rem]"
        ),

        Script(NotStr(three_js_script)),
        id="philosophy",
        cls="relative bg-[#0A0A0C] border-b border-white/10"
    )

def Diagnostico(lang="pt"):
    t = get_content(lang)
    diag_content = t["diagnostic"]
    diag_data = get_diagnostico_data(lang)

    btn = "w-full text-left p-5 rounded-2xl border border-white/10 bg-[#16161D] text-zinc-200 hover:border-white/40 hover:bg-white hover:text-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-white transition-all font-medium text-sm md:text-base cursor-pointer"

    # Painel Único Dinâmico
    painel_dinamico = Div(
        Div(
            Div(
                Span(cls="text-xs font-mono uppercase tracking-widest text-zinc-400", **{"x-text": f"`{diag_content['question_prefix']} 0${{i + 1}} {diag_content['of']} 0${{total}}`"}),
                Button(
                    diag_content["back"],
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
            Span(diag_content["result_badge"], cls="text-xs font-mono uppercase tracking-wider text-emerald-400"),
            cls="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 mb-4"
        ),
        H3(cls="text-3xl md:text-4xl font-bold text-white mb-4 tracking-tight", **{"x-text": "nivel.titulo"}),
        Div(
            Span(diag_content["analysis_label"] + " ", cls="text-zinc-400"),
            Span(cls="text-white font-bold", **{"x-text": "`${pontos} / ${dados.max}`"}),
            cls="font-mono text-sm mb-6"
        ),
        P(cls="text-zinc-300 text-base md:text-lg leading-relaxed mb-8 max-w-xl mx-auto", **{"x-text": "nivel.recomendacao"}),
        Div(
            A(diag_content["cta_btn"], href=f"mailto:{EMAIL_CONTACT}",
              cls="bg-white text-black font-semibold px-8 py-4 rounded-xl hover:bg-zinc-200 transition-colors shadow-lg",
              **{":href": "mailto"}),
            Button(diag_content["restart"], type="button",
                   cls="border border-white/20 bg-transparent text-white font-semibold px-8 py-4 rounded-xl hover:bg-white/10 transition-all cursor-pointer",
                   **{"@click": "reiniciar()"}),
            cls="flex flex-wrap items-center justify-center gap-4",
        ),
        **{"x-show": "concluido", "x-cloak": ""},
        cls="text-center py-4"
    )

    safe_json = json.dumps(diag_data, ensure_ascii=False).replace("</", "<\\/")

    return Section(
        Div(
            Span(diag_content["tag"], cls="text-xs font-mono uppercase tracking-[0.25em] text-zinc-400 text-center block mb-3"),
            H2(diag_content["h2"],
               cls="text-4xl md:text-5xl font-oswald uppercase tracking-tight text-white text-center mb-4 leading-[1.18]"),
            P(diag_content["desc"],
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

def ExecutiveCTASection(lang="pt"):
    t = get_content(lang)
    cta = t["cta"]
    mail_subject = urllib.parse.quote(cta["subject"])

    return Section(
        Div(
            # Card Monumental com Spotlight Interativo no Mouse
            Div(
                # Efeito Spotlight que segue o mouse (Alpine.js)
                Div(
                    cls="pointer-events-none absolute -inset-px rounded-[2.5rem] opacity-0 group-hover/cta:opacity-100 transition-opacity duration-500 z-0",
                    **{
                        ":style": "`background: radial-gradient(650px circle at ${mx}px ${my}px, rgba(52, 211, 153, 0.12), rgba(255, 255, 255, 0.04) 40%, transparent 80%);`"
                    }
                ),

                # Malha Arquitetônica de Fundo + Glow Fixo Central
                Div(cls="pointer-events-none absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_70%_70%_at_50%_50%,#000_40%,transparent_100%)] z-0"),
                Div(cls="pointer-events-none absolute -top-24 left-1/2 -translate-x-1/2 w-[520px] h-[240px] bg-emerald-500/10 blur-[110px] rounded-full z-0"),

                # Conteúdo Principal Centralizado
                Div(
                    # Badge de Status Operacional
                    Div(
                        Span(cls="size-2 rounded-full bg-emerald-400 animate-ping"),
                        Span(cls="size-2 rounded-full bg-emerald-400 -ml-2"),
                        Span(cta["badge"], cls="text-[10px] sm:text-[11px] font-mono font-semibold uppercase tracking-[0.2em] text-emerald-400"),
                        cls="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 mb-8"
                    ),

                    # Headline Monumental
                    H2(
                        cta["h2_line1"],
                        Br(),
                        Span(cta["h2_line2"], cls="font-playfair italic font-normal text-zinc-300"),
                        cls="text-4xl sm:text-6xl lg:text-7xl font-oswald uppercase tracking-tight text-white leading-[1.05] mb-6 max-w-4xl mx-auto"
                    ),

                    P(
                        cta["desc"],
                        cls="text-zinc-400 text-base sm:text-lg max-w-2xl mx-auto mb-10 leading-relaxed"
                    ),

                    # Linha de Botões de Ação (Iniciar Conversa + Copiar E-mail 1-Click)
                    Div(
                        # Botão Primário (Mailto Direto)
                        A(
                            Span(cta["btn_start"]),
                            NotStr('<svg class="w-4 h-4 ml-2.5 transition-transform duration-300 group-hover/btn:translate-x-1 group-hover/btn:-translate-y-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>'),
                            href=f"mailto:{EMAIL_CONTACT}?subject={mail_subject}",
                            cls="w-full sm:w-auto inline-flex items-center justify-center bg-white text-black font-semibold text-sm sm:text-base px-8 py-4 rounded-2xl hover:bg-zinc-200 transition-all shadow-[0_0_40px_rgba(255,255,255,0.2)] group/btn"
                        ),

                        # Botão Secundário Inteligente (Copiar E-mail sem abrir cliente de email)
                        Button(
                            NotStr('<svg x-show="!copied" class="w-4 h-4 mr-2.5 text-zinc-400 group-hover/copy:text-white transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>'),
                            NotStr('<svg x-show="copied" x-cloak class="w-4 h-4 mr-2.5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>'),
                            Span(**{"x-text": f"copied ? '{cta['btn_copied'].format(email=EMAIL_CONTACT)}' : '{cta['btn_copy']}'"}),
                            type="button",
                            cls="w-full sm:w-auto inline-flex items-center justify-center bg-[#181820] hover:bg-[#22222C] text-zinc-200 hover:text-white font-mono text-xs sm:text-sm px-7 py-4 rounded-2xl border border-white/15 hover:border-white/30 transition-all cursor-pointer group/copy",
                            **{
                                "@click": f"navigator.clipboard.writeText('{EMAIL_CONTACT}'); copied = true; setTimeout(() => copied = false, 3000)"
                            }
                        ),
                        cls="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12"
                    ),

                    # Barra Inferior de Conexão Rápida e Credenciais
                    Div(
                        A(
                            Span(cta["lk_label"], cls="text-xs font-mono text-zinc-300 group-hover/lk:text-white transition-colors"),
                            NotStr('<svg class="w-3.5 h-3.5 text-zinc-500 group-hover/lk:text-emerald-400 group-hover/lk:translate-x-0.5 group-hover/lk:-translate-y-0.5 transition-all" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>'),
                            href=LINKEDIN_URL,
                            target="_blank",
                            rel="noopener noreferrer",
                            cls="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white/[0.03] hover:bg-white/[0.08] border border-white/10 transition-all group/lk"
                        ),
                        A(
                            Span(cta["gh_label"], cls="text-xs font-mono text-zinc-300 group-hover/gh:text-white transition-colors"),
                            NotStr('<svg class="w-3.5 h-3.5 text-zinc-500 group-hover/gh:text-emerald-400 group-hover/gh:translate-x-0.5 group-hover/gh:-translate-y-0.5 transition-all" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>'),
                            href=GITHUB_URL,
                            target="_blank",
                            rel="noopener noreferrer",
                            cls="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white/[0.03] hover:bg-white/[0.08] border border-white/10 transition-all group/gh"
                        ),
                        Div(
                            Span(cta["base_label"], cls="text-[11px] font-mono text-zinc-500"),
                            Span(cta["base_val"], cls="text-xs font-mono text-zinc-300"),
                            cls="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white/[0.02] border border-white/5"
                        ),
                        cls="flex flex-wrap items-center justify-center gap-3 pt-8 border-t border-white/10 max-w-2xl mx-auto"
                    ),

                    cls="relative z-10 text-center py-16 sm:py-20 px-6 sm:px-12"
                ),

                cls="relative overflow-hidden rounded-[2.5rem] bg-[#101015] border border-white/15 shadow-[0_30px_90px_rgba(0,0,0,0.85)] group/cta",
                **{
                    "x-data": "{ mx: 500, my: 250, copied: false }",
                    "@mousemove": "const r = $el.getBoundingClientRect(); mx = $event.clientX - r.left; my = $event.clientY - r.top"
                }
            ),
            cls="max-w-7xl mx-auto px-6"
        ),
        id="contact",
        cls="py-20 sm:py-28 bg-[#0A0A0C] border-t border-white/10 relative z-20 gs-scroll"
    )

def render_portfolio(lang="pt"):
    t = get_content(lang)
    meta = t["meta"]
    nav = t["nav"]
    hero = t["hero"]
    metrics = t["metrics"]
    work = t["work"]
    cap = t["capabilities"]
    footer = t["footer"]

    # Faixa de Métricas formatada
    metric_elements = []
    for idx, m in enumerate(metrics):
        metric_elements.append(
            Div(
                H3(m["val"], cls=f"text-2xl lg:text-[26px] font-oswald tracking-tight {'text-emerald-400' if idx == 3 else 'text-white'}"),
                P(m["prefix"], Strong(m["strong"], cls="text-zinc-200"), cls="text-[11px] lg:text-xs text-zinc-400 mt-0.5 leading-tight whitespace-nowrap"),
                cls="flex-1 flex flex-col items-center text-center gs-scroll px-2"
            )
        )
        if idx < len(metrics) - 1:
            metric_elements.append(Div(cls="w-px h-8 bg-white/10 mx-2 hidden sm:block gs-scroll"))

    return (
        # Atualização dinâmica de lang e title no cliente
        Script(NotStr(f"""
            document.documentElement.lang = '{meta['lang']}';
            document.title = {json.dumps(meta['title'])};
        """)),

        # --- TOP NAVIGATION (Sincronizada + Mobile Drawer com Seletor Bilíngue) ---
        Header(
            Div(
                # Brand Logo
                A(
                    Span("João", cls="font-playfair italic font-bold text-3xl text-white"),
                    Span(".", cls="text-zinc-500 font-sans font-light not-italic text-3xl"),
                    href=f"/{'en' if lang == 'en' else ''}", 
                    cls="group flex items-center"
                ),
                
                # Links Desktop (Ordem Real da Página)
                Nav(
                    A(nav["about"], href="#about", cls="text-sm font-semibold text-zinc-300 hover:text-white transition-colors"),
                    A(nav["work"], href="#work", cls="text-sm font-semibold text-zinc-300 hover:text-white transition-colors"),
                    A(nav["philosophy"], href="#philosophy", cls="text-sm font-semibold text-zinc-300 hover:text-white transition-colors"),
                    A(nav["capabilities"], href="#capabilities", cls="text-sm font-semibold text-zinc-300 hover:text-white transition-colors"),
                    A(nav["diagnostic"], href="#diagnostico", cls="text-sm font-semibold text-zinc-300 hover:text-white transition-colors"),
                    cls="hidden md:flex items-center gap-8"
                ),
                
                # Right CTA & Language Toggle & Mobile Hamburger
                Div(
                    # Language Selector Pill [ PT | EN ]
                    Div(
                        A("PT", href="/", cls=f"px-2.5 py-1 text-xs font-mono rounded-full font-bold transition-all {'bg-white text-black shadow-sm' if lang == 'pt' else 'text-zinc-400 hover:text-white'}"),
                        Span("|", cls="text-zinc-600 text-xs font-mono select-none"),
                        A("EN", href="/en", cls=f"px-2.5 py-1 text-xs font-mono rounded-full font-bold transition-all {'bg-white text-black shadow-sm' if lang == 'en' else 'text-zinc-400 hover:text-white'}"),
                        cls="flex items-center gap-1 p-1 rounded-full bg-white/[0.05] border border-white/10"
                    ),

                    A(
                        nav["cta"], 
                        href=f"mailto:{EMAIL_CONTACT}", 
                        cls="hidden sm:inline-flex bg-white text-black text-sm font-semibold px-6 py-2.5 rounded-full hover:bg-zinc-200 transition-colors shadow-sm ml-2"
                    ),
                    Button(
                        NotStr('<svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>'),
                        cls="md:hidden p-2 text-white focus:outline-none cursor-pointer",
                        aria_label="Menu",
                        **{"@click": "mobileOpen = !mobileOpen"}
                    ),
                    cls="flex items-center gap-2 sm:gap-3"
                ),
                
                cls="max-w-[1440px] mx-auto px-6 py-6 flex items-center justify-between"
            ),
            
            # Mobile Menu Dropdown
            Div(
                Nav(
                    # Language Pill no Mobile
                    Div(
                        Span("Idioma / Language:", cls="text-xs font-mono text-zinc-400 uppercase tracking-wider"),
                        Div(
                            A("PT", href="/", cls=f"px-3 py-1 text-xs font-mono rounded-full font-bold {'bg-white text-black' if lang == 'pt' else 'text-zinc-400 hover:text-white'}"),
                            Span("|", cls="text-zinc-600 text-xs font-mono"),
                            A("EN", href="/en", cls=f"px-3 py-1 text-xs font-mono rounded-full font-bold {'bg-white text-black' if lang == 'en' else 'text-zinc-400 hover:text-white'}"),
                            cls="flex items-center gap-1 p-1 rounded-full bg-white/5 border border-white/10"
                        ),
                        cls="flex items-center justify-between py-3 border-b border-white/5"
                    ),
                    A(nav["about"], href="#about", cls="text-base font-semibold text-zinc-200 hover:text-white py-2 block border-b border-white/5", **{"@click": "mobileOpen = false"}),
                    A(nav["work"], href="#work", cls="text-base font-semibold text-zinc-200 hover:text-white py-2 block border-b border-white/5", **{"@click": "mobileOpen = false"}),
                    A(nav["philosophy"], href="#philosophy", cls="text-base font-semibold text-zinc-200 hover:text-white py-2 block border-b border-white/5", **{"@click": "mobileOpen = false"}),
                    A(nav["capabilities"], href="#capabilities", cls="text-base font-semibold text-zinc-200 hover:text-white py-2 block border-b border-white/5", **{"@click": "mobileOpen = false"}),
                    A(nav["diagnostic"], href="#diagnostico", cls="text-base font-semibold text-zinc-200 hover:text-white py-2 block border-b border-white/5", **{"@click": "mobileOpen = false"}),
                    A(nav["cta"], href=f"mailto:{EMAIL_CONTACT}", cls="text-base font-semibold text-emerald-400 py-3 block", **{"@click": "mobileOpen = false"}),
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
                    alt="João Barbosa | Data Architect & BI", 
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
                    Span(hero["badge"], cls="text-sm font-semibold text-zinc-200"),
                    href="#diagnostico",
                    cls="hidden lg:flex absolute left-[6%] xl:left-[10%] top-[45%] z-40 glass-pill px-4 py-2 rounded-full items-center gap-2.5 shadow-xl hover:border-white/30 transition-all gs-reveal"
                ),
                
                # MIDDLE RIGHT: Strategic Focus
                Div(
                    Div(
                        Span(hero["focus_tag"], cls="text-[11px] font-mono font-bold text-zinc-400 tracking-wider block mb-1 uppercase"),
                        P(hero["focus_desc"], cls="text-sm font-semibold text-zinc-200 leading-snug"),
                        cls="border-l-2 border-white/30 pl-3.5"
                    ),
                    cls="hidden lg:block absolute right-[6%] xl:right-[10%] top-[45%] z-40 max-w-[220px] text-left gs-reveal pointer-events-none"
                ),
                
                # BOTTOM LEFT: "EU SOU JOÃO" / "I AM JOÃO"
                Div(
                    H1(
                        Span(hero["title_1"], cls="block"), 
                        Span(hero["title_2"], cls="text-white block pt-[0.1em]"), 
                        cls="font-oswald text-[9vw] xl:text-[112px] leading-[0.98] font-bold text-white/90 uppercase tracking-tight"
                    ),
                    cls="absolute left-[5%] xl:left-[8%] bottom-6 sm:bottom-8 lg:bottom-10 z-20 gs-reveal pointer-events-none"
                ),
                
                # BOTTOM RIGHT: "DATA ANALYST" / "DATA ARCHITECT & BI"
                Div(
                    H2(
                        Span(hero["role_1"], cls="text-white block"), 
                        Span(hero["role_2"], cls="text-white block pt-[0.1em]"), 
                        cls="font-oswald text-[8vw] xl:text-[86px] leading-[0.98] font-bold uppercase tracking-tight text-right"
                    ),
                    cls="absolute right-[5%] xl:right-[8%] bottom-6 sm:bottom-8 lg:bottom-10 z-20 gs-reveal pointer-events-none"
                ),
                
                # HERO BOTTOM STATUS BAR
                Div(
                    Div(
                        Span(cls="inline-block w-2 h-2 rounded-full bg-emerald-400"),
                        Span("ANALYTICS STACK: PYTHON • POSTGRESQL • POWER BI" if lang == 'en' else "STACK ANALÍTICA: PYTHON • POSTGRESQL • POWER BI"),
                        cls="flex items-center gap-2.5"
                    ),
                    Div(
                        Span("CITY OF SÃO PAULO • GOV DATA LAB" if lang == 'en' else "PREF. DE SÃO PAULO • GOV DATA LAB"),
                        A("EXPLORE PORTFOLIO ↓" if lang == 'en' else "EXPLORAR PORTFÓLIO ↓", href="#work", cls="text-white underline underline-offset-4 hover:text-zinc-300 ml-4 pointer-events-auto"),
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
                *metric_elements,
                cls="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between px-6 gap-4 sm:gap-0"
            ),
            cls="border-b border-white/10 bg-[#0E0E12] py-5 md:py-6 relative z-20"
        ),

        # --- TECH STACK MARQUEE ---
        TechMarquee(),

        # --- BIO / TRAJETÓRIA EXECUTIVA ---
        AboutSection(lang=lang),

        # --- SELECTED WORK (REAL INTERACTIVE CAROUSEL) ---
        Section(
            Div(
                Div(
                    Span(work["tag"], cls="text-xs font-mono uppercase tracking-[0.2em] text-zinc-400 block mb-3"),
                    H2(work["h2"], cls="text-4xl sm:text-5xl font-oswald uppercase tracking-tight text-white mb-4 leading-[1.18]"),
                    P(work["p"], cls="text-zinc-400 text-base max-w-xl"),
                    cls="text-left mb-16 gs-scroll"
                ),
                FeatureCarousel(lang=lang),
                cls="max-w-7xl mx-auto px-6 py-24"
            ),
            id="work", cls="bg-[#0A0A0C] relative z-10 border-b border-white/10"
        ),

        # --- PHILOSOPHY (COM CENA 3D INTERATIVA) ---
        DataJourney3DSection(lang=lang),

        # --- BENTO GRID: CAPACIDADES TÉCNICAS ---
        Section(
            Div(
                Span(cap["tag"], cls="text-xs font-bold text-zinc-400 tracking-widest uppercase mb-3 block font-mono text-center gs-scroll"),
                H2(cap["h2"], cls="text-4xl md:text-5xl font-oswald uppercase tracking-tight text-white text-center mb-4 gs-scroll leading-[1.18]"),
                P(cap["desc"], cls="text-center text-zinc-400 mb-16 gs-scroll text-base md:text-lg max-w-2xl mx-auto"),
                
                Div(
                    # Card 1: Integridade & Auditoria
                    Div(
                        Div(
                            Div(
                                NotStr('''<svg class="integrity-orbit transition-colors duration-500 text-white/10 absolute inset-0 size-full pointer-events-none" viewBox="0 0 254 104" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M112.891 97.7022C140.366 97.0802 171.004 94.6715 201.087 87.5116C210.43 85.2881 219.615 82.6412 228.284 78.2473C232.198 76.3179 235.905 73.9942 239.348 71.3124C241.85 69.2557 243.954 66.7571 245.555 63.9408C249.34 57.3235 248.281 50.5341 242.498 45.6109C239.033 42.7237 235.228 40.2703 231.169 38.3054C219.443 32.7209 207.141 28.4382 194.482 25.534C184.013 23.1927 173.358 21.7755 162.64 21.2989C161.376 21.3512 160.113 21.181 158.908 20.796C158.034 20.399 156.857 19.1682 156.962 18.4535C157.115 17.8927 157.381 17.3689 157.743 16.9139C158.104 16.4588 158.555 16.0821 159.067 15.8066C160.14 15.4683 161.274 15.3733 162.389 15.5286C179.805 15.3566 196.626 18.8373 212.998 24.462C220.978 27.2494 228.798 30.4747 236.423 34.1232C240.476 36.1159 244.202 38.7131 247.474 41.8258C254.342 48.2578 255.745 56.9397 251.841 65.4892C249.793 69.8582 246.736 73.6777 242.921 76.6327C236.224 82.0192 228.522 85.4602 220.502 88.2924C205.017 93.7847 188.964 96.9081 172.738 99.2109C153.442 101.949 133.993 103.478 114.506 103.79C91.1468 104.161 67.9334 102.97 45.1169 97.5831C36.0094 95.5616 27.2626 92.1655 19.1771 87.5116C13.839 84.5746 9.1557 80.5802 5.41318 75.7725C-0.54238 67.7259 -1.13794 59.1763 3.25594 50.2827C5.82447 45.3918 9.29572 41.0315 13.4863 37.4319C24.2989 27.5721 37.0438 20.9681 50.5431 15.7272C68.1451 8.8849 86.4883 5.1395 105.175 2.83669C129.045 0.0992292 153.151 0.134761 177.013 2.94256C197.672 5.23215 218.04 9.01724 237.588 16.3889C240.089 17.3418 242.498 18.5197 244.933 19.6446C246.627 20.4387 247.725 21.6695 246.997 23.615C246.455 25.1105 244.814 25.5605 242.63 24.5811C230.322 18.9961 217.233 16.1904 204.117 13.4376C188.761 10.3438 173.2 8.36665 157.558 7.52174C129.914 5.70776 102.154 8.06792 75.2124 14.5228C60.6177 17.8788 46.5758 23.2977 33.5102 30.6161C26.6595 34.3329 20.4123 39.0673 14.9818 44.658C12.9433 46.8071 11.1336 49.1622 9.58207 51.6855C4.87056 59.5336 5.61172 67.2494 11.9246 73.7608C15.2064 77.0494 18.8775 79.925 22.8564 82.3236C31.6176 87.7101 41.3848 90.5291 51.3902 92.5804C70.6068 96.5773 90.0219 97.7419 112.891 97.7022Z" fill="currentColor"/>
                                </svg>'''),
                                Span(cap["card1_tag"], cls="text-4xl font-oswald font-bold tracking-widest text-white z-10 block"),
                                cls="relative flex h-24 w-56 items-center justify-center"
                            ),
                            Div(
                                H3(cap["card1_title"], cls="text-xl font-oswald uppercase tracking-tight text-white font-bold leading-[1.18]"),
                                P(cap["card1_desc"], cls="text-sm text-zinc-400 mt-1"),
                                cls="mt-8 text-center"
                            ),
                            cls="relative m-auto size-fit pt-6"
                        ),
                        cls="group relative col-span-full flex flex-col justify-between overflow-hidden lg:col-span-2 rounded-3xl border border-white/10 bg-[#121217] p-6 shadow-sm hover:border-white/25 transition-all gs-scroll"
                    ),
                    
                    # Card 2: Segurança & Governança
                    Div(
                        Div(
                            Div(
                                NotStr('''<svg class="m-auto h-fit w-24 text-zinc-400" viewBox="0 0 212 143" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path class="text-zinc-600" d="M44.0209 55.3542C43.1945 54.7639 42.6916 54.0272 42.5121 53.1442C42.3327 52.2611 42.5995 51.345 43.3125 50.3958C50.632 40.3611 59.812 32.5694 70.8525 27.0208C81.8931 21.4722 93.668 18.6979 106.177 18.6979C118.691 18.6979 130.497 21.3849 141.594 26.7587C152.691 32.1326 161.958 39.8936 169.396 50.0417C170.222 51.1042 170.489 52.0486 170.196 52.875C169.904 53.7014 169.401 54.4097 168.688 55C167.979 55.5903 167.153 55.8571 166.208 55.8004C165.264 55.7437 164.438 55.2408 163.729 54.2917C157.236 45.0833 148.885 38.0307 138.675 33.1337C128.466 28.2368 117.633 25.786 106.177 25.7812C94.7257 25.7812 83.9827 28.2321 73.948 33.1337C63.9132 38.0354 55.5903 45.0881 48.9792 54.2917C48.2709 55.3542 47.4445 55.9444 46.5 56.0625C45.5556 56.1806 44.7292 55.9444 44.0209 55.3542ZM126.188 142.656C113.91 139.587 103.875 133.476 96.0834 124.325C88.2917 115.173 84.3959 103.988 84.3959 90.7708C84.3959 84.8681 86.5209 79.9097 90.7709 75.8958C95.0209 71.8819 100.156 69.875 106.177 69.875C112.198 69.875 117.333 71.8819 121.583 75.8958C125.833 79.9097 127.958 84.8681 127.958 90.7708C127.958 94.6667 129.434 97.9439 132.385 100.602C135.337 103.261 138.819 104.588 142.833 104.583C146.847 104.583 150.271 103.256 153.104 100.602C155.938 97.9486 157.354 94.6714 157.354 90.7708C157.354 77.0764 152.337 65.566 142.302 56.2396C132.267 46.9132 120.285 42.25 106.354 42.25C92.4237 42.25 80.441 46.9132 70.4063 56.2396C60.3716 65.566 55.3542 77.0174 55.3542 90.5937C55.3542 93.4271 55.621 96.9687 56.1546 101.219C56.6882 105.469 57.9562 110.427 59.9584 116.094C60.3125 117.156 60.2842 118.101 59.8734 118.927C59.4625 119.753 58.7825 120.344 57.8334 120.698C56.8889 121.052 55.9752 121.024 55.0921 120.613C54.2091 120.202 53.5881 119.522 53.2292 118.573C51.4584 113.969 50.1905 109.395 49.4255 104.853C48.6605 100.31 48.2756 95.6158 48.2709 90.7708C48.2709 75.0694 53.9682 61.9062 65.363 51.2812C76.7577 40.6562 90.3624 35.3437 106.177 35.3437C122.115 35.3437 135.809 40.6562 147.26 51.2812C158.712 61.9062 164.438 75.0694 164.438 90.7708C164.438 96.6736 162.343 101.601 158.155 105.554C153.966 109.506 148.859 111.485 142.833 111.49C136.813 111.49 131.649 109.513 127.342 105.561C123.035 101.608 120.88 96.6783 120.875 90.7708C120.875 86.875 119.43 83.5978 116.54 80.9392C113.65 78.2805 110.196 76.9536 106.177 76.9583C102.163 76.9583 98.7089 78.2876 95.8142 80.9462C92.9195 83.6049 91.4745 86.8797 91.4792 90.7708C91.4792 102.222 94.8745 111.785 101.665 119.458C108.456 127.132 117.22 132.503 127.958 135.573C129.021 135.927 129.729 136.517 130.083 137.344C130.438 138.17 130.497 139.056 130.26 140C130.024 140.826 129.552 141.535 128.844 142.125C128.135 142.715 127.25 142.892 126.188 142.656ZM67.0417 18.3437C66.0973 18.934 65.1528 19.0828 64.2084 18.79C63.2639 18.4972 62.5556 17.8762 62.0834 16.9271C61.6112 15.9826 61.4931 15.1279 61.7292 14.3629C61.9653 13.5979 62.5556 12.9179 63.5 12.3229C70.1112 8.78125 77.0174 6.06597 84.2188 4.17708C91.4202 2.28819 98.7396 1.34375 106.177 1.34375C113.733 1.34375 121.111 2.25986 128.313 4.09208C135.514 5.92431 142.479 8.54986 149.208 11.9687C150.271 12.559 150.892 13.2674 151.071 14.0937C151.251 14.9201 151.161 15.7465 150.802 16.5729C150.448 17.3993 149.858 18.0486 149.031 18.5208C148.205 18.9931 147.201 18.934 146.021 18.3437C139.764 15.1563 133.299 12.7078 126.627 10.9983C119.954 9.28889 113.138 8.43181 106.177 8.42708C99.3299 8.42708 92.6007 9.22514 85.9896 10.8212C79.3785 12.4174 73.0625 14.9249 67.0417 18.3437ZM87.9375 140.177C80.9723 132.858 75.6314 125.392 71.915 117.78C68.1987 110.167 66.3381 101.164 66.3334 90.7708C66.3334 80.0278 70.2292 70.9658 78.0209 63.585C85.8125 56.2042 95.198 52.5161 106.177 52.5208C117.156 52.5208 126.601 56.2112 134.51 63.5921C142.42 70.9729 146.375 80.0325 146.375 90.7708C146.375 91.8333 146.052 92.6904 145.405 93.3421C144.758 93.9937 143.901 94.3172 142.833 94.3125C141.889 94.3125 141.063 93.989 140.354 93.3421C139.646 92.6951 139.292 91.8381 139.292 90.7708C139.292 81.9167 136.014 74.5099 129.46 68.5504C122.906 62.591 115.145 59.6089 106.177 59.6042C97.2049 59.6042 89.503 62.5862 83.0713 68.5504C76.6396 74.5146 73.4214 81.9214 73.4167 90.7708C73.4167 100.333 75.0695 108.451 78.375 115.123C81.6806 121.796 86.5209 128.494 92.8959 135.219C93.6042 135.927 93.9584 136.753 93.9584 137.698C93.9584 138.642 93.6042 139.469 92.8959 140.177C92.1875 140.885 91.3612 141.24 90.4167 141.24C89.4723 141.24 88.6459 140.885 87.9375 140.177ZM141.417 128.135C130.91 128.135 121.789 124.594 114.054 117.51C106.319 110.427 102.454 101.514 102.458 90.7708C102.458 89.8264 102.784 89 103.436 88.2917C104.088 87.5833 104.942 87.2292 106 87.2292C107.063 87.2292 107.92 87.5833 108.571 88.2917C109.223 89 109.546 89.8264 109.542 90.7708C109.542 99.625 112.729 106.885 119.104 112.552C125.479 118.219 132.917 121.052 141.417 121.052C142.125 121.052 143.129 120.993 144.427 120.875C145.726 120.757 147.083 120.58 148.5 120.344C149.563 120.108 150.479 120.256 151.248 120.79C152.018 121.324 152.519 122.119 152.75 123.177C152.986 124.122 152.809 124.948 152.219 125.656C151.629 126.365 150.861 126.837 149.917 127.073C147.792 127.663 145.934 127.989 144.342 128.05C142.751 128.112 141.776 128.14 141.417 128.135Z" fill="currentColor"/>
                                    <path class="bio-scanner-line" d="M3 72H209" stroke="#34d399" stroke-width="5" stroke-linecap="round"/>
                                </svg>'''),
                                cls="relative mx-auto flex aspect-square size-32 rounded-full border border-white/10 before:absolute before:-inset-2 before:rounded-full before:border before:border-white/5 items-center justify-center bg-white/[0.02]"
                            ),
                            Div(
                                H3(cap["card2_title"], cls="text-xl font-oswald uppercase tracking-tight text-white font-bold leading-[1.18]"),
                                P(cap["card2_desc"], cls="text-sm text-zinc-400 mt-1"),
                                cls="relative z-10 mt-6 space-y-2 text-center"
                            ),
                            cls="pt-6"
                        ),
                        cls="group relative col-span-full overflow-hidden sm:col-span-3 lg:col-span-2 rounded-3xl border border-white/10 bg-[#121217] p-6 shadow-sm hover:border-white/25 transition-all gs-scroll"
                    ),
                    
                    # Card 3: Performance & Otimização
                    Div(
                        Div(
                            Div(
                                NotStr('''<svg class="w-full text-zinc-200" viewBox="0 0 386 123" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <rect width="386" height="123" rx="10" fill="#18181E"/>
                                    <path class="perf-line-svg" d="M3 121.077C3 121.077 15.3041 93.6691 36.0195 87.756C56.7349 81.8429 66.6632 80.9723 66.6632 80.9723C66.6632 80.9723 80.0327 80.9723 91.4656 80.9723C102.898 80.9723 100.415 64.2824 108.556 64.2824C116.696 64.2824 117.693 92.1332 125.226 92.1332C132.759 92.1332 142.07 78.5115 153.591 80.9723C165.113 83.433 186.092 92.1332 193 92.1332C199.908 92.1332 205.274 64.2824 213.017 64.2824C220.76 64.2824 237.832 93.8946 243.39 92.1332C248.948 90.3718 257.923 60.5 265.284 60.5C271.145 60.5 283.204 87.7182 285.772 87.756C293.823 87.8746 299.2 73.0802 304.411 73.0802C311.283 73.0802 321.425 65.9506 333.552 64.2824C345.68 62.6141 346.91 82.4553 362.27 80.9723C377.629 79.4892 383 106.605 383 106.605" stroke="#FFFFFF" stroke-width="2.5"/>
                                </svg>'''),
                                cls="pt-2 px-1"
                            ),
                            Div(
                                H3(cap["card3_title"], cls="text-xl font-oswald uppercase tracking-tight text-white font-bold leading-[1.18]"),
                                P(cap["card3_desc"], cls="text-sm text-zinc-400 mt-1"),
                                cls="relative z-10 mt-6 space-y-2 text-center"
                            ),
                            cls="pt-6"
                        ),
                        cls="group relative col-span-full overflow-hidden sm:col-span-3 lg:col-span-2 rounded-3xl border border-white/10 bg-[#121217] p-6 shadow-sm hover:border-white/25 transition-all gs-scroll"
                    ),
                    
                    # Card 4: Pipelines Automatizados
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
                                    H3(cap["card4_title"], cls="text-xl font-oswald uppercase tracking-tight text-white font-bold leading-[1.18]"),
                                    P(cap["card4_desc"], cls="text-sm text-zinc-400 mt-1"),
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
                                    H3(cap["card5_title"], cls="text-xl font-oswald uppercase tracking-tight text-white font-bold leading-[1.18]"),
                                    P(cap["card5_desc"], cls="text-sm text-zinc-400 mt-1"),
                                    cls="space-y-2"
                                ),
                                cls="relative z-10 flex flex-col justify-between space-y-6"
                            ),
                            Div(
                                Div(
                                    Div(
                                        Span(cap["roles"]["cdo"], cls="block rounded border border-white/10 bg-white/5 px-2.5 py-1 text-xs font-semibold text-zinc-200 shadow-sm"),
                                        Div("CDO", cls="size-9 rounded-full bg-white text-black flex items-center justify-center text-[10px] font-bold tracking-tight ring-2 ring-white/20 shrink-0"),
                                        cls="relative flex items-center justify-end gap-2 pr-6"
                                    ),
                                    Div(
                                        Div("BI", cls="size-9 rounded-full bg-zinc-700 text-white flex items-center justify-center text-[11px] font-bold tracking-tight ring-2 ring-white/20 shrink-0"),
                                        Span(cap["roles"]["bi"], cls="block rounded border border-white/10 bg-white/5 px-2.5 py-1 text-xs font-semibold text-zinc-200 shadow-sm"),
                                        cls="relative flex items-center justify-start gap-2 pl-4"
                                    ),
                                    Div(
                                        Span(cap["roles"]["ops"], cls="block rounded border border-white/10 bg-white/5 px-2.5 py-1 text-xs font-semibold text-zinc-200 shadow-sm"),
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
        Diagnostico(lang=lang),

        # --- EXECUTIVE CLOSING CTA ---
        ExecutiveCTASection(lang=lang),
        
        # --- FOOTER (Executive Monolith) ---
        Footer(
            Div(
                Div(
                    A(
                        Span("João Barbosa", cls="font-playfair italic font-bold text-3xl text-white"),
                        Span(".", cls="text-zinc-500 font-sans font-light not-italic text-3xl"),
                        href=f"/{'en' if lang == 'en' else ''}", 
                        cls="group inline-block"
                    ),
                    P(footer["role"], cls="text-xs text-zinc-400 font-mono mt-2"),
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
                    Span(footer["copyright"], cls="text-[11px] font-mono text-zinc-400"),
                    Span(footer["c_level"], cls="text-[11px] font-mono text-zinc-400"),
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

@rt("/")
def get():
    return render_portfolio("pt")

@rt("/en")
def get_en():
    return render_portfolio("en")

if __name__ == "__main__":
    serve()
