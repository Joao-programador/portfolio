"""
Módulo de Internacionalização (i18n) para o Portfólio Executivo de João Barbosa.
Contém todo o conteúdo textual e metadados estruturados para 'pt' e 'en'.
Anti-slop: vocabulário rigoroso, autêntico e adaptado para tomadas de decisão C-Level.
"""

CONTENT = {
    "pt": {
        "meta": {
            "lang": "pt-BR",
            "title": "João Barbosa | Arquitetura de Dados & Inteligência Executiva (BI)",
            "desc": "Portfólio executivo de João Barbosa: Arquitetura de Dados, Analytics, Engenharia e Dashboards para decisões estratégicas.",
            "og_title": "João Barbosa | Portfólio de Dados & BI",
            "og_desc": "Arquitetura de Dados, Analytics e Visualização para Decisões C-Level."
        },
        "nav": {
            "about": "Sobre",
            "work": "Projetos",
            "philosophy": "Filosofia",
            "capabilities": "Engenharia",
            "diagnostic": "Diagnóstico",
            "cta": "Iniciar Conversa",
            "lang_pt": "PT",
            "lang_en": "EN"
        },
        "hero": {
            "badge": "Disponível para Projetos Estratégicos",
            "focus_tag": "FOCO ESTRATÉGICO",
            "focus_desc": "Arquitetura de Dados, Analytics e Visualização para Decisões Executivas.",
            "title_1": "EU SOU",
            "title_2": "JOÃO",
            "role_1": "DATA",
            "role_2": "ANALYST"
        },
        "metrics": [
            {"val": "+3 ANOS", "prefix": "Inteligência na ", "strong": "Pref. de São Paulo / SPP"},
            {"val": "CONCESSÕES", "prefix": "Auditoria de ", "strong": "Contratos Públicos & SLAs"},
            {"val": "STAR SCHEMA", "prefix": "Modelagem dimensional & ", "strong": "Integridade em SQL"},
            {"val": "DECISÃO C-LEVEL", "prefix": "Cockpits estratégicos de ", "strong": "Alta Adoção Executiva"}
        ],
        "about": {
            "tag": "TRAJETÓRIA & PROPÓSITO",
            "h2": "DADOS A SERVIÇO DE DECISÕES ESTRATÉGICAS NA MAIOR METRÓPOLE DA AMÉRICA LATINA.",
            "lead": "A ponte essencial entre a engenharia analítica e a tomada de decisão executiva.",
            "spp_badge": "ATUAÇÃO INSTITUCIONAL",
            "spp_title": "São Paulo Parcerias (SPP)",
            "spp_desc": "Estruturação analítica, auditoria e modelagem de dados para desestatizações, concessões e projetos estratégicos do município de São Paulo.",
            "p1": "Com atuação direta na modelagem e auditoria de dados para desestatizações e parcerias públicas, meu foco é transformar bases volumosas e dispersas em ecossistemas de decisão auditáveis, claros e de alta adoção.",
            "p2": "Inteligência de dados só tem valor real quando reduz a incerteza de diretores e gestores em segundos, unindo a robustez do código em Python e modelagem relacional a interfaces executivas de máxima clareza cognitiva.",
            "pillars": [
                {
                    "num": "01",
                    "title": "Rigor & Auditoria",
                    "desc": "Bases validadas e estruturadas para atender aos mais altos padrões de compliance e órgãos de controle."
                },
                {
                    "num": "02",
                    "title": "Automação de Ponta",
                    "desc": "Pipelines em Python que eliminam retrabalho manual e aceleram o fechamento de análises complexas."
                },
                {
                    "num": "03",
                    "title": "Design Cognitivo",
                    "desc": "Painéis executivos desenhados para que decisores encontrem respostas críticas com máxima agilidade."
                }
            ]
        },
        "work": {
            "tag": "PORTFÓLIO EXECUTIVO SELECIONADO",
            "h2": "PROJETOS RECENTES",
            "p": "Casos reais de modelagem analítica, infraestrutura e monitoramento executivo aplicados à gestão pública e estratégica.",
            "interactive_hint": "Cockpit Interativo • Clique para expandir",
            "btn_explore": "Abrir Cockpit Interativo",
            "modal_close": "ESC para fechar",
            "modal_new_tab": "Abrir em Nova Aba",
            "badge_interactive": "DEMO AO VIVO",
            "auditable_hint": "Auditável em Produção",
            "modal_hint": "Cockpit Interativo • Tecla ESC fecha",
            "modal_loading": "Carregando Cockpit Analítico...",
            "select_case": "SELECIONE UM CASO DE USO",
            "features": [
                {
                    "label": "Fiscalização de Concessões (DF%)",
                    "tag": "GovTech & PPPs • SP Parcerias",
                    "description": "Painel executivo com telemetria contínua, auditoria de ativos e apuração de índice de disponibilidade física contratual.",
                    "iframe_src": "/Projetos/Painel de Disponibilidade Fisica/index.html",
                    "glow": "rgba(59, 130, 246, 0.16)",
                    "accent": "text-blue-400",
                    "bar": "bg-blue-400",
                    "path": "spp.gov.br/fiscalizacao-df"
                },
                {
                    "label": "Análise de Prazos & SLAs",
                    "tag": "Gestão Estratégica",
                    "description": "Monitoramento de prazos processuais com Star Schema, categorização de criticidade e alertas preventivos para a liderança.",
                    "iframe_src": "/Projetos/Análise de Prazos - Ficticio.html",
                    "glow": "rgba(52, 211, 153, 0.16)",
                    "accent": "text-emerald-400",
                    "bar": "bg-emerald-400",
                    "path": "cockpit.spp.gov/prazos-sla"
                },
                {
                    "label": "Mapeamento Geoespacial SP",
                    "tag": "GIS & Mobilidade",
                    "description": "Painel geográfico de alta densidade correlacionando infraestrutura viária, zonas de estacionamento e fluxos metropolitanos.",
                    "iframe_src": "/Projetos/Mapa de Estacionamentos/index.html",
                    "glow": "rgba(139, 92, 246, 0.16)",
                    "accent": "text-purple-400",
                    "bar": "bg-purple-400",
                    "path": "geo.spp.gov/mobilidade-sp"
                },
                {
                    "label": "Gestão Operacional (SGO)",
                    "tag": "Eficiência Estratégica",
                    "description": "Cockpit executivo consolidado com KPIs de produtividade, gargalos de atendimento e controle operacional.",
                    "iframe_src": "/Projetos/Painel de Performance Operacional/index.html",
                    "glow": "rgba(245, 158, 11, 0.16)",
                    "accent": "text-amber-400",
                    "bar": "bg-amber-400",
                    "path": "cockpit.spp.gov/sgo-executivo"
                }
            ]
        },
        "philosophy": {
            "tag": "FILOSOFIA DE ENGENHARIA",
            "h2_line1": "DA ENTROPIA À",
            "h2_line2": "Clareza Estratégica.",
            "desc": "Uma experiência tridimensional interativa: veja como dados dispersos e caóticos são transformados em arquitetura relacional e decisões de alto impacto.",
            "stage_intro": "01 // BASES DISPERSAS & CAOS OPERACIONAL",
            "stage_metric_1": "Planilhas & Sistemas Isolados",
            "stage_mid": "02 // PIPELINE PYTHON & STAR SCHEMA SQL",
            "stage_metric_2": "Modelagem & Validação",
            "stage_metric_2_sub": "Tratamento de Anomalias",
            "stage_final": "03 // COCKPIT EXECUTIVO C-LEVEL",
            "stage_metric_3": "Consistência Auditável • Passe o mouse nos blocos para inspecionar",
            "mode_olap": "01. MATRIZ OLAP",
            "mode_star": "02. STAR SCHEMA 3D",
            "mode_gauss": "03. GAUSSIANA / BELL CURVE",
            "tt_id_label": "NÓ RELACIONAL",
            "tt_kpi_label": "KPI CONCESSÃO",
            "tt_conf_label": "CONFORMIDADE",
            "tt_lat_label": "LATÊNCIA",
            "h2_sub1": "Dashboards são fáceis.",
            "h2_sub2": "Decisões são difíceis.",
            "p_sub": "Qualquer um pode conectar um CSV a um visualizador comercial. Meu foco é estruturar dados para que reflitam rigorosamente a realidade operacional e respondam às perguntas estratégicas da liderança.",
            "cards": [
                {
                    "tag": "ETL & GOVERNANÇA",
                    "title": "Higienização & Pipeline",
                    "desc": "Garbage in, garbage out. Construo rotinas automatizadas e contratos de dados para tratar anomalias antes que elas contaminem reuniões de diretoria.",
                    "footer": "Dados auditáveis e consistentes"
                },
                {
                    "tag": "ARQUITETURA RELACIONAL",
                    "title": "Modelagem Dimensional",
                    "desc": "Modelos relacionais otimizados em Star Schema. Crio a fundação que permite consultas de alta performance e cruzamentos analíticos para bases públicas e operacionais complexas.",
                    "footer": "Consultas otimizadas em SQL"
                },
                {
                    "tag": "UI/UX & STORYTELLING",
                    "title": "Visualização Executiva",
                    "desc": "O cérebro humano é visual e seletivo. Projeto telas com hierarquia óptica limpa para que gestores absorvam conclusões críticas com rapidez e clareza.",
                    "footer": "Foco em alta adoção prática"
                }
            ]
        },
        "capabilities": {
            "tag": "CAPACIDADES TÉCNICAS",
            "h2": "ENGENHARIA & INTELIGÊNCIA EM DADOS",
            "desc": "Modelagem relacional rigorosa, governança e rastreabilidade da origem ao painel final.",
            "card1_tag": "AUDIT",
            "card1_title": "Integridade & Auditoria",
            "card1_desc": "Modelagem relacional com validações contínuas para prestação de contas aos órgãos de controle.",
            "card2_title": "Segurança & Governança",
            "card2_desc": "Controle rigoroso de acessos, conformidade e rastreabilidade total de linhagem de dados.",
            "card3_title": "Performance & Otimização",
            "card3_desc": "Consultas SQL otimizadas com Star Schema e tempos de resposta instantâneos.",
            "card4_title": "Pipelines Automatizados",
            "card4_desc": "Ingestão contínua com rotinas automatizadas, reexecução assistida e logs de auditoria.",
            "card5_title": "Adoção Executiva C-Level",
            "card5_desc": "Storytelling e métricas desenhadas sob medida para diretoria, gerência e analistas de ponta.",
            "roles": {
                "cdo": "Diretoria C-Level",
                "bi": "Liderança de Analytics",
                "ops": "Times de Negócio & Produto"
            }
        },
        "diagnostic": {
            "tag": "FERRAMENTA INTERATIVA SEM CADASTRO",
            "h2": "DIAGNÓSTICO DE MATURIDADE EM DADOS",
            "desc": "Quatro perguntas objetivas para mapear a maturidade analítica da sua operação e o próximo passo para alcançar decisões estratégicas.",
            "question_prefix": "Pergunta",
            "of": "de",
            "back": "← Voltar",
            "restart": "Refazer Diagnóstico",
            "cta_btn": "Falar sobre Próximos Passos",
            "result_badge": "DIAGNÓSTICO CONCLUÍDO",
            "analysis_label": "Análise Técnica:",
            "rec_label": "Próximo Passo Recomendado:"
        },
        "cta": {
            "badge": "DISPONÍVEL PARA PROJETOS ESTRATÉGICOS & POSIÇÕES EXECUTIVAS",
            "h2_line1": "VAMOS TRANSFORMAR DADOS",
            "h2_line2": "em Decisões de Alto Impacto?",
            "desc": "Seja para estruturar pipelines auditáveis em Python e SQL, desenhar cockpits executivos em Power BI ou elevar a governança analítica da sua operação em São Paulo ou remotamente.",
            "btn_start": "Iniciar Conversa Agora",
            "btn_copy": "Copiar E-mail Direto",
            "btn_copied": "E-mail Copiado: {email}",
            "subject": "Contato Estratégico via Portfólio | João Barbosa",
            "lk_label": "LINKEDIN EXECUTIVO",
            "gh_label": "REPOSITÓRIO GITHUB",
            "base_label": "BASE:",
            "base_val": "SÃO PAULO, SP • BRASIL"
        },
        "footer": {
            "role": "Arquitetura de Dados • Business Intelligence Executivo • FastHTML & SQL",
            "copyright": "© 2026 JOÃO BARBOSA. TODOS OS DIREITOS RESERVADOS.",
            "c_level": "DESENHADO PARA DECISÕES ESTRATÉGICAS C-LEVEL."
        }
    },
    "en": {
        "meta": {
            "lang": "en",
            "title": "João Barbosa | Data Architecture & Executive Intelligence (BI)",
            "desc": "Executive portfolio of João Barbosa: Data Architecture, Analytics Engineering, and Cockpits for strategic decision-making.",
            "og_title": "João Barbosa | Data & BI Architecture Portfolio",
            "og_desc": "Data Architecture, Analytics Engineering & Executive Visualization for C-Level Decision-Making."
        },
        "nav": {
            "about": "About",
            "work": "Projects",
            "philosophy": "Philosophy",
            "capabilities": "Engineering",
            "diagnostic": "Diagnostic",
            "cta": "Get in Touch",
            "lang_pt": "PT",
            "lang_en": "EN"
        },
        "hero": {
            "badge": "Available for Strategic Projects & Roles",
            "focus_tag": "STRATEGIC FOCUS",
            "focus_desc": "Data Architecture, Analytics Engineering & Decision-Grade Visualization for Leadership.",
            "title_1": "I AM",
            "title_2": "JOÃO",
            "role_1": "DATA",
            "role_2": "ARCHITECT & BI"
        },
        "metrics": [
            {"val": "+3 YEARS", "prefix": "Public Intelligence at ", "strong": "City of São Paulo / SPP"},
            {"val": "CONCESSIONS", "prefix": "Audit & Compliance for ", "strong": "Public Contracts & SLAs"},
            {"val": "STAR SCHEMA", "prefix": "Dimensional Modeling & ", "strong": "SQL Integrity"},
            {"val": "C-LEVEL IMPACT", "prefix": "Executive Cockpits with ", "strong": "High Leadership Adoption"}
        ],
        "about": {
            "tag": "CAREER & MISSION",
            "h2": "DATA ARCHITECTURE DRIVING STRATEGIC GOVERNANCE IN LATIN AMERICA'S LARGEST METROPOLIS.",
            "lead": "The essential bridge between analytics engineering and executive decision-making.",
            "spp_badge": "INSTITUTIONAL SCOPE",
            "spp_title": "São Paulo Parcerias (SPP)",
            "spp_desc": "Data architecture, compliance auditing, and relational modeling for public concessions, privatizations, and strategic infrastructure projects for the City of São Paulo.",
            "p1": "With hands-on experience modeling and auditing data for high-stakes public concessions and public-private partnerships, my mission is to transform fragmented, high-volume records into auditable, decisive, and highly adopted ecosystems.",
            "p2": "Data intelligence only delivers genuine value when it cuts through executive uncertainty in seconds, combining robust Python pipelines and relational modeling with dashboards engineered for immediate cognitive clarity.",
            "pillars": [
                {
                    "num": "01",
                    "title": "Rigor & Auditability",
                    "desc": "Databases validated and structured to satisfy strict regulatory compliance and government oversight bodies."
                },
                {
                    "num": "02",
                    "title": "High-End Automation",
                    "desc": "Python pipelines that eliminate manual toil and accelerate the turnaround of mission-critical analytics."
                },
                {
                    "num": "03",
                    "title": "Cognitive Design",
                    "desc": "Executive cockpits crafted so leadership discovers strategic answers instantly with zero visual friction."
                }
            ]
        },
        "work": {
            "tag": "SELECTED EXECUTIVE PORTFOLIO",
            "h2": "FEATURED PROJECTS",
            "p": "Real-world cases in analytical modeling, public infrastructure, and executive cockpits applied to strategic governance.",
            "interactive_hint": "Interactive Cockpit • Click to expand",
            "btn_explore": "Open Interactive Cockpit",
            "modal_close": "ESC to close",
            "modal_new_tab": "Open in New Tab",
            "badge_interactive": "LIVE DEMO",
            "auditable_hint": "Auditable in Production",
            "modal_hint": "Interactive Cockpit • Press ESC to close",
            "modal_loading": "Loading Analytical Cockpit...",
            "select_case": "SELECT A USE CASE",
            "features": [
                {
                    "label": "Concession Oversight (Availability %)",
                    "tag": "GovTech & PPPs • SP Parcerias",
                    "description": "Executive cockpit featuring continuous telemetry, asset auditing, and contractual physical availability compliance index.",
                    "iframe_src": "/Projetos/Painel de Disponibilidade Fisica/index.html",
                    "glow": "rgba(59, 130, 246, 0.16)",
                    "accent": "text-blue-400",
                    "bar": "bg-blue-400",
                    "path": "spp.gov.br/concessions-availability"
                },
                {
                    "label": "Deadline & SLA Compliance Analysis",
                    "tag": "Strategic Governance",
                    "description": "Procedural timeline tracking powered by Star Schema, severity tiers, and early-warning alerts for executive leadership.",
                    "iframe_src": "/Projetos/Análise de Prazos - Ficticio.html",
                    "glow": "rgba(52, 211, 153, 0.16)",
                    "accent": "text-emerald-400",
                    "bar": "bg-emerald-400",
                    "path": "cockpit.spp.gov/sla-timelines"
                },
                {
                    "label": "São Paulo Geospatial Mapping",
                    "tag": "GIS & Mobility",
                    "description": "High-density geospatial intelligence correlating urban parking assets, street infrastructure, and metropolitan traffic patterns.",
                    "iframe_src": "/Projetos/Mapa de Estacionamentos/index.html",
                    "glow": "rgba(139, 92, 246, 0.16)",
                    "accent": "text-purple-400",
                    "bar": "bg-purple-400",
                    "path": "geo.spp.gov/sp-mobility"
                },
                {
                    "label": "Operational Governance (SGO)",
                    "tag": "Strategic Efficiency",
                    "description": "Consolidated operations cockpit tracking team productivity metrics, resolution bottlenecks, and operational oversight.",
                    "iframe_src": "/Projetos/Painel de Performance Operacional/index.html",
                    "glow": "rgba(245, 158, 11, 0.16)",
                    "accent": "text-amber-400",
                    "bar": "bg-amber-400",
                    "path": "cockpit.spp.gov/sgo-operations"
                }
            ]
        },
        "philosophy": {
            "tag": "ENGINEERING PHILOSOPHY",
            "h2_line1": "FROM RAW ENTROPY TO",
            "h2_line2": "Strategic Clarity.",
            "desc": "An interactive 3D spatial experience: witness how fragmented, chaotic records transform into relational architecture and high-impact decisions.",
            "stage_intro": "01 // DISPERSED DATA & OPERATIONAL CHAOS",
            "stage_metric_1": "Siloed Spreadsheets & Disconnected Systems",
            "stage_mid": "02 // PYTHON PIPELINE & STAR SCHEMA SQL",
            "stage_metric_2": "Modeling & Validation",
            "stage_metric_2_sub": "Anomaly Remediation",
            "stage_final": "03 // C-LEVEL EXECUTIVE COCKPIT",
            "stage_metric_3": "Auditable Consistency • Hover over blocks to inspect",
            "mode_olap": "01. OLAP MATRIX",
            "mode_star": "02. 3D STAR SCHEMA",
            "mode_gauss": "03. GAUSSIAN BELL CURVE",
            "tt_id_label": "RELATIONAL NODE",
            "tt_kpi_label": "CONCESSION KPI",
            "tt_conf_label": "COMPLIANCE",
            "tt_lat_label": "LATENCY",
            "h2_sub1": "Dashboards are easy.",
            "h2_sub2": "Decisions are hard.",
            "p_sub": "Anyone can hook up a CSV to a off-the-shelf visualizer. My focus is structuring data so it strictly mirrors operational reality and answers critical leadership questions.",
            "cards": [
                {
                    "tag": "ETL & GOVERNANCE",
                    "title": "Pipeline & Data Contracts",
                    "desc": "Garbage in, garbage out. I engineer automated routines and data contracts to catch anomalies before they reach executive board meetings.",
                    "footer": "Auditable, consistent data"
                },
                {
                    "tag": "RELATIONAL ARCHITECTURE",
                    "title": "Dimensional Modeling",
                    "desc": "Star Schema dimensional architectures. I build the foundation enabling sub-second analytical queries across complex public and operational databases.",
                    "footer": "Optimized SQL execution"
                },
                {
                    "tag": "UI/UX & STORYTELLING",
                    "title": "Executive Visualization",
                    "desc": "The human brain is visual and selective. I design cockpits with optical hierarchy so executives extract mission-critical insights in seconds.",
                    "footer": "Maximum practical adoption"
                }
            ]
        },
        "capabilities": {
            "tag": "TECHNICAL CAPABILITIES",
            "h2": "DATA ENGINEERING & BUSINESS INTELLIGENCE",
            "desc": "Rigorous relational modeling, governance, and end-to-end lineage from ingestion to the executive suite.",
            "card1_tag": "AUDIT",
            "card1_title": "Integrity & Compliance",
            "card1_desc": "Relational modeling with continuous validation, tailored for government oversight and strict regulatory audits.",
            "card2_title": "Security & Governance",
            "card2_desc": "Strict role-based access controls, data lineage traceability, and regulatory compliance standards.",
            "card3_title": "Performance & Optimization",
            "card3_desc": "Star Schema architectures tuned for low-latency SQL execution and instant drill-downs.",
            "card4_title": "Automated Pipelines",
            "card4_desc": "Continuous ingestion routines with scheduled backfills, health telemetry, and full audit logs.",
            "card5_title": "C-Level Executive Adoption",
            "card5_desc": "Tailored storytelling and metric hierarchies designed specifically for C-suite directors and operational teams.",
            "roles": {
                "cdo": "C-Level Leadership",
                "bi": "Analytics Management",
                "ops": "Business & Ops Teams"
            }
        },
        "diagnostic": {
            "tag": "INTERACTIVE ASSESSMENT • NO REGISTRATION REQUIRED",
            "h2": "DATA MATURITY DIAGNOSTIC",
            "desc": "Four objective questions assessing your organization's analytics maturity and mapping the next strategic step.",
            "question_prefix": "Question",
            "of": "of",
            "back": "← Back",
            "restart": "Retake Diagnostic",
            "cta_btn": "Discuss Strategic Next Steps",
            "result_badge": "DIAGNOSTIC COMPLETED",
            "analysis_label": "Technical Assessment:",
            "rec_label": "Recommended Next Step:"
        },
        "cta": {
            "badge": "AVAILABLE FOR STRATEGIC PROJECTS & EXECUTIVE ROLES",
            "h2_line1": "READY TO TRANSFORM COMPLEX DATA",
            "h2_line2": "into Decisive Executive Impact?",
            "desc": "Whether architecting auditable Python & SQL pipelines, designing executive Power BI cockpits, or scaling analytical governance across your operation, in São Paulo or globally.",
            "btn_start": "Start a Conversation",
            "btn_copy": "Copy Direct Email",
            "btn_copied": "Email Copied: {email}",
            "subject": "Strategic Consultation via Portfolio | João Barbosa",
            "lk_label": "EXECUTIVE LINKEDIN",
            "gh_label": "GITHUB REPOSITORY",
            "base_label": "LOCATION:",
            "base_val": "SÃO PAULO, BRAZIL"
        },
        "footer": {
            "role": "Data Architecture • Executive Business Intelligence • FastHTML & SQL",
            "copyright": "© 2026 JOÃO BARBOSA. ALL RIGHTS RESERVED.",
            "c_level": "ENGINEERED FOR C-LEVEL STRATEGIC DECISION-MAKING."
        }
    }
}

DIAGNOSTICO_DATA = {
    "pt": {
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
                ["Horas de esforço manual sem documentação", 1],
                ["Algumas horas restaurando backup do banco de dados", 2],
                ["Minutos, através de infraestrutura como código e pipelines versionados", 3],
            ]},
        ],
        "niveis": [
            {
                "max": 3,
                "titulo": "Fase 1: Fundação a Construir",
                "recomendacao": "Sua operação se beneficiará de um BI Sprint para organizar fontes dispersas, eliminar retrabalho manual e publicar os primeiros cockpits executivos auditáveis."
            },
            {
                "max": 7,
                "titulo": "Fase 2: Base em Expansão",
                "recomendacao": "Você já possui dados relevantes. O próximo passo recomendado é consolidar a modelagem dimensional (Star Schema) e esteiras de ingestão contínua para garantir escala sem gargalos."
            },
            {
                "max": 12,
                "titulo": "Fase 3: Maturidade Avançada",
                "recomendacao": "Sua estrutura é sólida e madura. A evolução natural envolve observabilidade analítica de ponta a ponta, governança preditiva e redução de latência para consultas executivas."
            }
        ]
    },
    "en": {
        "max": 12,
        "perguntas": [
            {"q": "Where does your organization's core data live today?", "opcoes": [
                ["Dispersed spreadsheets and shared folder silos", 0],
                ["Multiple software systems with zero unified integration", 1],
                ["Centralized database, but plagued by manual reporting tasks", 2],
                ["Automated, cataloged, and audited data pipelines", 3],
            ]},
            {"q": "How frequently does executive leadership make decisions backed by auditable metrics?", "opcoes": [
                ["Rarely / Decisions are primarily driven by intuition", 0],
                ["Only during semi-annual or annual executive review meetings", 1],
                ["Monthly, but figures face recurrent disputes across departments", 2],
                ["Daily, driven by consolidated KPIs and active governance", 3],
            ]},
            {"q": "Does every strategic KPI have formal data documentation and clear ownership?", "opcoes": [
                ["No formal documentation exists", 0],
                ["Only for select isolated financial figures", 1],
                ["For most metrics, with occasional discrepancies", 2],
                ["Yes, documented in a formal data dictionary with active stewardship", 3],
            ]},
            {"q": "If your primary executive dashboard crashes today, how long does full recovery take?", "opcoes": [
                ["Days or weeks, relying entirely on one key individual", 0],
                ["Hours of manual reconstruction without documentation", 1],
                ["A few hours restoring database backups", 2],
                ["Minutes, orchestrated via code versioning and automated CI/CD", 3],
            ]},
        ],
        "niveis": [
            {
                "max": 3,
                "titulo": "Stage 1: Foundation to Build",
                "recomendacao": "Your operation would benefit from a focused BI Sprint to unify disparate sources, eliminate manual spreadsheet toil, and ship your first auditable executive cockpits."
            },
            {
                "max": 7,
                "titulo": "Stage 2: Expanding Base",
                "recomendacao": "You already possess valuable data. The recommended leap is implementing a Star Schema dimensional architecture and automated ETL pipelines to ensure scalability without bottlenecks."
            },
            {
                "max": 12,
                "titulo": "Stage 3: Advanced Governance",
                "recomendacao": "Your foundation is solid and mature. The natural evolution involves end-to-end analytical observability, predictive SLA compliance, and reduced decision latency for executive leadership."
            }
        ]
    }
}

def get_content(lang: str = "pt") -> dict:
    """Retorna o dicionário de conteúdo para o idioma solicitado ('pt' ou 'en')."""
    return CONTENT.get(lang, CONTENT["pt"])

def get_diagnostico_data(lang: str = "pt") -> dict:
    """Retorna a base de dados do Diagnóstico no idioma especificado."""
    return DIAGNOSTICO_DATA.get(lang, DIAGNOSTICO_DATA["pt"])
