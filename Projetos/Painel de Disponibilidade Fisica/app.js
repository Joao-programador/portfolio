/*
 * Motor Analítico e Controlador SPA: Centro de Controle de Concessões e PPPs (PMSP / SP Parcerias)
 * Ultra-Clean High-Contrast Institucional Light Mode
 * Gerencia estado global, filtros e ciclo de vida das instâncias Chart.js nas 6 visões obrigatórias.
 */

(function () {
    "use strict";

    const DATA = window.SPP_MOCK_DATA;
    if (!DATA) {
        console.error("Base de dados SPP_MOCK_DATA não encontrada.");
        return;
    }

    const META_DF = DATA.meta.meta_contratual_df || 80.0;
    const ALL_DATES = DATA.meta.datas;
    const LAST_DATE = DATA.meta.data_atual;

    const state = {
        activePage: "visao_geral", // visao_geral | lote_1 | lote_2 | lote_3 | pendencias | historico
        filters: {
            periodo: "ultimo_dia", // ultimo_dia | media_7d | media_15d | media_30d | YYYY-MM-DD
            localId: "all",        // all | lote_1 | lote_2 | lote_3
            bateria: "all",        // all | nome da bateria
            categoria: "all",      // all | categoria
            prioridade: "all",     // all | P1 | P2 | Sem pendência
            searchQuery: "",       // texto de busca na pagina 5
            statusFilter: "all"    // filtro de status na pagina 5
        },
        drilldown: {
            selectedLocalId: "lote_2",
            selectedBateria: "Terminal Grajaú"
        },
        modalTicket: null
    };

    const chartInstances = {};

    function destroyAllCharts() {
        Object.keys(chartInstances).forEach((key) => {
            if (chartInstances[key]) {
                chartInstances[key].destroy();
                delete chartInstances[key];
            }
        });
    }

    function formatDateBR(isoStr) {
        if (!isoStr) return "";
        const parts = isoStr.split("-");
        if (parts.length !== 3) return isoStr;
        return `${parts[2]}/${parts[1]}/${parts[0]}`;
    }

    function formatShortDateBR(isoStr) {
        if (!isoStr) return "";
        const parts = isoStr.split("-");
        if (parts.length !== 3) return isoStr;
        return `${parts[2]}/${parts[1]}`;
    }

    function formatNumber(n) {
        return Number(n).toLocaleString("pt-BR");
    }

    function formatPercent(n) {
        return Number(n).toFixed(1).replace(".", ",") + "%";
    }

    function getActiveDates() {
        const p = state.filters.periodo;
        if (p === "ultimo_dia") return [LAST_DATE];
        if (p === "media_7d") return ALL_DATES.slice(-7);
        if (p === "media_15d") return ALL_DATES.slice(-15);
        if (p === "media_30d") return ALL_DATES.slice();
        if (ALL_DATES.includes(p)) return [p];
        return [LAST_DATE];
    }

    function getEffectiveLocalFilter() {
        if (state.activePage === "lote_1") return "lote_1";
        if (state.activePage === "lote_2") return "lote_2";
        if (state.activePage === "lote_3") return "lote_3";
        return state.filters.localId;
    }

    function getFilteredData() {
        const activeDates = new Set(getActiveDates());
        const effectiveLocal = getEffectiveLocalFilter();
        const fBat = state.filters.bateria;
        const fCat = state.filters.categoria;
        const fPrio = state.filters.prioridade;

        const rawPendencias = DATA.pendencias.filter((p) => {
            if (!activeDates.has(p.data)) return false;
            if (effectiveLocal !== "all" && p.local_id !== effectiveLocal) return false;
            if (fBat !== "all" && p.bateria !== fBat) return false;
            if (fCat !== "all" && p.categoria !== fCat) return false;
            return true;
        });

        const rawDF = DATA.disponibilidade_fisica.filter((r) => {
            if (!activeDates.has(r.data)) return false;
            if (effectiveLocal !== "all" && r.local_id !== effectiveLocal) return false;
            if (fBat !== "all" && r.bateria !== fBat) return false;
            return true;
        });

        const byBateria = {};
        rawDF.forEach((r) => {
            if (!byBateria[r.bateria]) {
                byBateria[r.bateria] = {
                    bateria: r.bateria,
                    local_id: r.local_id,
                    local: r.local,
                    local_curto: r.local_curto,
                    spe: r.spe,
                    contrato: r.contrato,
                    total_ativos: r.total_ativos,
                    sum_disp: 0,
                    sum_indisp: 0,
                    count: 0
                };
            }
            byBateria[r.bateria].sum_disp += r.disponiveis;
            byBateria[r.bateria].sum_indisp += r.indisponiveis;
            byBateria[r.bateria].count += 1;
        });

        const pendByBatCount = {};
        if (fCat !== "all") {
            rawPendencias.forEach((p) => {
                pendByBatCount[p.bateria] = (pendByBatCount[p.bateria] || 0) + 1;
            });
        }

        let consolidatedDF = Object.values(byBateria).map((item) => {
            const daysCount = Math.max(1, item.count);
            let indisp = Math.round(item.sum_indisp / daysCount);
            if (fCat !== "all") {
                indisp = Math.round((pendByBatCount[item.bateria] || 0) / daysCount);
            }
            const disp = Math.max(0, item.total_ativos - indisp);
            const df_pct = Number(((disp / item.total_ativos) * 100).toFixed(1));
            const prio = indisp >= 3 ? "P1" : (indisp >= 1 ? "P2" : "Sem pendência");
            const cond = df_pct >= META_DF ? "Operacional" : "Abaixo do mínimo";

            return {
                bateria: item.bateria,
                local_id: item.local_id,
                local: item.local,
                local_curto: item.local_curto,
                spe: item.spe,
                contrato: item.contrato,
                total_ativos: item.total_ativos,
                disponiveis: disp,
                indisponiveis: indisp,
                df_percentual: df_pct,
                prioridade: prio,
                condicao: cond
            };
        });

        if (fPrio !== "all") {
            consolidatedDF = consolidatedDF.filter((c) => c.prioridade === fPrio);
        }

        const validBaterias = new Set(consolidatedDF.map((c) => c.bateria));
        const latestInSelection = getActiveDates()[getActiveDates().length - 1];

        const snapshotPendencias = rawPendencias.filter((p) => {
            if (!validBaterias.has(p.bateria)) return false;
            if (fPrio !== "all" && p.prioridade_complexo !== fPrio && p.prioridade !== fPrio) return false;
            return p.data === latestInSelection;
        });

        return {
            dfList: consolidatedDF,
            pendenciasList: snapshotPendencias,
            allPeriodPendencias: rawPendencias.filter((p) => validBaterias.has(p.bateria))
        };
    }

    function computeKPIs(dfList, pendenciasList) {
        const totalAtivos = dfList.reduce((acc, r) => acc + r.total_ativos, 0);
        const disponiveis = dfList.reduce((acc, r) => acc + r.disponiveis, 0);
        const indisponiveis = dfList.reduce((acc, r) => acc + r.indisponiveis, 0);
        const dfGeral = totalAtivos > 0 ? Number(((disponiveis / totalAtivos) * 100).toFixed(1)) : 0.0;
        const condicaoGeral = dfGeral >= META_DF ? "Operacional" : "Abaixo do mínimo";
        const totalPendencias = pendenciasList.length;
        const complexosAbaixoMeta = dfList.filter((r) => r.df_percentual < META_DF).length;
        const totalP1 = dfList.filter((r) => r.prioridade === "P1").length;
        const totalP2 = dfList.filter((r) => r.prioridade === "P2").length;
        const totalSemPend = dfList.filter((r) => r.prioridade === "Sem pendência").length;
        const glosaEstimada = pendenciasList.reduce((acc, p) => acc + (p.glosa_brl || 0), 0);

        return {
            totalAtivos,
            disponiveis,
            indisponiveis,
            dfGeral,
            condicaoGeral,
            totalPendencias,
            complexosAbaixoMeta,
            totalComplexos: dfList.length,
            totalP1,
            totalP2,
            totalSemPend,
            glosaEstimada
        };
    }

    function animateCountUp(el, targetVal, isPercent, duration = 500) {
        if (!el) return;
        const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        if (prefersReduced) {
            el.textContent = isPercent ? formatPercent(targetVal) : formatNumber(targetVal);
            return;
        }
        const startVal = parseFloat(el.dataset.currentVal || "0") || 0;
        el.dataset.currentVal = String(targetVal);
        const startTime = performance.now();

        function step(now) {
            const elapsed = now - startTime;
            const progress = Math.min(1, elapsed / duration);
            const eased = 1 - Math.pow(1 - progress, 3);
            const curr = startVal + (targetVal - startVal) * eased;
            if (isPercent) {
                el.textContent = curr.toFixed(1).replace(".", ",") + "%";
            } else {
                el.textContent = Math.round(curr).toLocaleString("pt-BR");
            }
            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                el.textContent = isPercent ? formatPercent(targetVal) : formatNumber(targetVal);
            }
        }
        requestAnimationFrame(step);
    }

    const tk = {
        textPrimary: "#0F172A",
        textSecondary: "#64748B",
        gridColor: "rgba(15, 23, 42, 0.035)",
        tooltipBg: "#FFFFFF",
        tooltipBorder: "#E2E8F0",
        sppOrange: "#F08200",
        sppBlue: "#004B6E",
        emerald: "#059669",
        emeraldText: "#047857",
        amber: "#D97706",
        amberText: "#B45309",
        crimson: "#E11D48",
        crimsonText: "#BE123C",
        royal: "#004B6E",
        indigo: "#4F46E5",
        violet: "#7C3AED",
        cyan: "#0284C7"
    };

    function priorityBadgeHTML(prio) {
        if (prio === "P1") {
            return `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-mono font-semibold bg-rose-50 text-rose-700 border border-rose-200">
                <span class="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse"></span>P1 • Crítico
            </span>`;
        }
        if (prio === "P2") {
            return `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-mono font-semibold bg-amber-50 text-amber-800 border border-amber-200">
                <span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>P2 • Alerta
            </span>`;
        }
        return `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-mono font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>Sem pendência
        </span>`;
    }

    function condicaoBadgeHTML(cond) {
        if (cond === "Operacional") {
            return `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-mono font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">
                ✓ Operacional (≥80%)
            </span>`;
        }
        return `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-mono font-semibold bg-rose-50 text-rose-700 border border-rose-200">
            ⚠ Abaixo do mínimo (<80%)
        </span>`;
    }

    const metaLinePlugin = {
        id: "sppMetaLine",
        afterDatasetsDraw(chart, args, options) {
            if (!options || !options.enabled) return;
            const { ctx, chartArea: { left, right }, scales: { y } } = chart;
            if (!y) return;
            const yPos = y.getPixelForValue(options.value || 80.0);
            if (yPos < chart.chartArea.top || yPos > chart.chartArea.bottom) return;

            ctx.save();
            ctx.beginPath();
            ctx.setLineDash([4, 4]);
            ctx.lineWidth = 1.2;
            ctx.strokeStyle = "rgba(217, 119, 6, 0.65)";
            ctx.moveTo(left, yPos);
            ctx.lineTo(right, yPos);
            ctx.stroke();

            const labelText = options.label || "Meta: 80,0%";
            ctx.font = "500 10px 'Geist Mono', monospace";
            const textWidth = ctx.measureText(labelText).width;
            const padX = 6;
            const boxX = right - textWidth - padX * 2 - 4;
            const boxY = yPos - 18;

            ctx.fillStyle = "#FFFBEB";
            ctx.strokeStyle = "#FDE68A";
            ctx.lineWidth = 1;
            ctx.setLineDash([]);
            ctx.beginPath();
            ctx.roundRect(boxX, boxY, textWidth + padX * 2, 16, 4);
            ctx.fill();
            ctx.stroke();

            ctx.fillStyle = "#B45309";
            ctx.fillText(labelText, boxX + padX, boxY + 12);
            ctx.restore();
        }
    };

    if (window.Chart) {
        Chart.defaults.font.family = "'Geist', sans-serif";
        Chart.defaults.color = "#64748B";
        Chart.defaults.plugins.tooltip.backgroundColor = "#FFFFFF";
        Chart.defaults.plugins.tooltip.titleColor = "#0F172A";
        Chart.defaults.plugins.tooltip.bodyColor = "#475569";
        Chart.defaults.plugins.tooltip.borderColor = "#E2E8F0";
        Chart.defaults.plugins.tooltip.borderWidth = 1;
        Chart.defaults.plugins.tooltip.padding = 10;
        Chart.defaults.plugins.tooltip.cornerRadius = 8;
        Chart.defaults.plugins.tooltip.boxPadding = 4;
        Chart.defaults.plugins.tooltip.usePointStyle = true;
        Chart.defaults.plugins.tooltip.titleFont = { family: "'Geist', sans-serif", weight: "600", size: 12 };
        Chart.defaults.plugins.tooltip.bodyFont = { family: "'Geist Mono', monospace", size: 11 };
        Chart.register(metaLinePlugin);
    }

    function populateFilterDropdowns() {
        const selLocal = document.getElementById("select-local");
        const selBateria = document.getElementById("select-bateria");
        const selCat = document.getElementById("select-categoria");
        const selPeriodo = document.getElementById("select-periodo");

        if (selPeriodo && selPeriodo.options.length <= 4) {
            const group = document.createElement("optgroup");
            group.label = "Datas Específicas (Série 30 Dias)";
            ALL_DATES.slice().reverse().forEach((d) => {
                const opt = document.createElement("option");
                opt.value = d;
                opt.textContent = `Dia ${formatDateBR(d)}`;
                group.appendChild(opt);
            });
            selPeriodo.appendChild(group);
        }

        if (selLocal) {
            const currentVal = getEffectiveLocalFilter();
            selLocal.innerHTML = `<option value="all">Todos os Lotes Regionais</option>`;
            DATA.meta.locais.forEach((l) => {
                const opt = document.createElement("option");
                opt.value = l.id;
                opt.textContent = l.nome;
                selLocal.appendChild(opt);
            });
            selLocal.value = currentVal;
            selLocal.disabled = ["lote_1", "lote_2", "lote_3"].includes(state.activePage);
        }

        if (selBateria) {
            const currentBat = state.filters.bateria;
            const effLocal = getEffectiveLocalFilter();
            selBateria.innerHTML = `<option value="all">Todos os Complexos Concedidos</option>`;
            DATA.meta.locais.forEach((l) => {
                if (effLocal !== "all" && l.id !== effLocal) return;
                l.baterias.forEach((b) => {
                    const opt = document.createElement("option");
                    opt.value = b.nome;
                    opt.textContent = b.nome;
                    selBateria.appendChild(opt);
                });
            });
            if ([...selBateria.options].some((o) => o.value === currentBat)) {
                selBateria.value = currentBat;
            } else {
                state.filters.bateria = "all";
                selBateria.value = "all";
            }
        }

        if (selCat) {
            const currCat = state.filters.categoria;
            const cats = [
                "Infraestrutura Elétrica",
                "Sistemas & Telemetria",
                "Obras Civis & Hidráulica",
                "Eletromobilidade",
                "Segurança & Acessibilidade"
            ];
            selCat.innerHTML = `<option value="all">Todas as Categorias</option>`;
            cats.forEach((c) => {
                const opt = document.createElement("option");
                opt.value = c;
                opt.textContent = c;
                selCat.appendChild(opt);
            });
            selCat.value = currCat;
        }

        let activeCount = 0;
        if (state.filters.periodo !== "ultimo_dia") activeCount++;
        if (state.filters.localId !== "all" && !["lote_1", "lote_2", "lote_3"].includes(state.activePage)) activeCount++;
        if (state.filters.bateria !== "all") activeCount++;
        if (state.filters.categoria !== "all") activeCount++;
        if (state.filters.prioridade !== "all") activeCount++;

        const badge = document.getElementById("active-filters-count");
        if (badge) {
            if (activeCount > 0) {
                badge.textContent = String(activeCount);
                badge.classList.remove("hidden");
            } else {
                badge.classList.add("hidden");
            }
        }
    }

    function renderKPIStrip(containerId, kpis, scopeLabel) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const isOp = kpis.dfGeral >= META_DF;
        const deltaMeta = (kpis.dfGeral - META_DF).toFixed(1).replace(".", ",");
        const deltaSignal = kpis.dfGeral >= META_DF ? `+${deltaMeta} p.p. acima da meta` : `${deltaMeta} p.p. abaixo do mínimo`;
        const dispPct = kpis.totalAtivos > 0 ? ((kpis.disponiveis / kpis.totalAtivos) * 100).toFixed(1).replace(".", ",") : "0,0";

        container.innerHTML = `
            <!-- Card Focal Primario: DF Geral (%) + Semaforo Contratual -->
            <div class="col-span-1 sm:col-span-2 lg:col-span-2 rounded-2xl p-5 border transition-all relative overflow-hidden ${isOp ? 'kpi-focal-emerald' : 'kpi-focal-crimson'}">
                <div class="flex items-start justify-between gap-3 mb-2">
                    <div>
                        <span class="text-[11px] font-mono uppercase tracking-wider text-slate-500 block">DF Geral (%) • ${scopeLabel}</span>
                        <div class="flex items-baseline gap-3 mt-1">
                            <span id="kpi-val-df" data-current-val="0" class="text-4xl sm:text-5xl font-mono font-bold tracking-tight ${isOp ? 'text-emerald-700' : 'text-rose-700'}">${formatPercent(kpis.dfGeral)}</span>
                            <span class="text-xs font-mono text-slate-500">Meta: 80,0%</span>
                        </div>
                    </div>
                    <div>
                        ${condicaoBadgeHTML(kpis.condicaoGeral)}
                    </div>
                </div>
                <div class="w-full h-2 rounded-full bg-slate-200 overflow-hidden my-3 relative">
                    <div class="h-full rounded-full transition-all duration-500 ${isOp ? 'bg-emerald-500' : 'bg-rose-500'}" style="width: ${Math.min(100, kpis.dfGeral)}%"></div>
                    <div class="absolute top-0 bottom-0 w-0.5 bg-amber-500" style="left: 80%" title="Meta Contratual: 80%"></div>
                </div>
                <div class="flex items-center justify-between text-xs font-mono">
                    <span class="${isOp ? 'text-emerald-700' : 'text-rose-700'} font-semibold">${deltaSignal}</span>
                    <span class="text-slate-500">${isOp ? 'Adimplente ao Caderno de Encargos' : 'Sujeito a Glosa na Contraprestação'}</span>
                </div>
            </div>

            <!-- Card KPI 1: Total de Ativos Monitorados -->
            <div class="surface-card rounded-2xl p-5 border flex flex-col justify-between">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-mono uppercase tracking-wider text-slate-500">Total de Ativos</span>
                    <span class="p-2 rounded-lg bg-blue-50 text-blue-700 border border-blue-200">
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
                    </span>
                </div>
                <div class="my-2">
                    <span id="kpi-val-total" class="text-3xl font-mono font-bold tracking-tight text-slate-900">${formatNumber(kpis.totalAtivos)}</span>
                </div>
                <div class="text-xs text-slate-500 flex items-center justify-between">
                    <span>${kpis.totalComplexos} complexos</span>
                    <span class="font-mono text-blue-700 font-medium">100% auditado</span>
                </div>
            </div>

            <!-- Card KPI 2: Ativos Disponiveis -->
            <div class="surface-card rounded-2xl p-5 border flex flex-col justify-between">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-mono uppercase tracking-wider text-slate-500">Ativos Disponíveis</span>
                    <span class="p-2 rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-200">
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    </span>
                </div>
                <div class="my-2 flex items-baseline gap-2.5">
                    <span id="kpi-val-disp" class="text-3xl font-mono font-bold tracking-tight text-emerald-700">${formatNumber(kpis.disponiveis)}</span>
                    <span class="text-xs font-mono text-emerald-700">(${dispPct}%)</span>
                </div>
                <div class="text-xs text-slate-500">Em operação normal no período</div>
            </div>

            <!-- Card KPI 3: Ativos Indisponiveis -->
            <div class="surface-card rounded-2xl p-5 border flex flex-col justify-between">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-mono uppercase tracking-wider text-slate-500">Ativos Indisponíveis</span>
                    <span class="p-2 rounded-lg bg-rose-50 text-rose-700 border border-rose-200">
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                    </span>
                </div>
                <div class="my-2 flex items-baseline gap-2.5">
                    <span id="kpi-val-indisp" class="text-3xl font-mono font-bold tracking-tight ${kpis.indisponiveis > 0 ? 'text-rose-700' : 'text-emerald-700'}">${formatNumber(kpis.indisponiveis)}</span>
                    <span class="text-xs font-mono text-slate-500">unidades</span>
                </div>
                <div class="text-xs text-slate-500 flex items-center justify-between">
                    <span class="font-semibold text-rose-700">${kpis.totalP1} em P1</span>
                    <span class="font-mono text-amber-700">${kpis.totalP2} em P2</span>
                </div>
            </div>

            <!-- Card KPI 5 & 6 Combinados -->
            <div class="surface-card rounded-2xl p-5 border flex flex-col justify-between">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-mono uppercase tracking-wider text-slate-500">Pendências Abertas (SPE)</span>
                    <span class="p-2 rounded-lg bg-amber-50 text-amber-700 border border-amber-200">
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
                    </span>
                </div>
                <div class="my-2 flex items-baseline justify-between">
                    <span id="kpi-val-pend" class="text-3xl font-mono font-bold tracking-tight text-slate-900">${formatNumber(kpis.totalPendencias)}</span>
                    <span class="text-xs font-mono text-rose-700 font-medium" title="Impacto financeiro estimado">R$ ${(kpis.glosaEstimada / 1000).toFixed(1).replace(".", ",")}k glosa</span>
                </div>
                <div class="text-xs text-slate-500 flex items-center justify-between border-t border-slate-100 pt-2 mt-1">
                    <span>Complexos Abaixo da Meta:</span>
                    <span class="font-mono font-bold ${kpis.complexosAbaixoMeta > 0 ? 'text-rose-700' : 'text-emerald-700'}">${kpis.complexosAbaixoMeta} de ${kpis.totalComplexos}</span>
                </div>
            </div>
        `;

        animateCountUp(document.getElementById("kpi-val-df"), kpis.dfGeral, true);
        animateCountUp(document.getElementById("kpi-val-total"), kpis.totalAtivos, false);
        animateCountUp(document.getElementById("kpi-val-disp"), kpis.disponiveis, false);
        animateCountUp(document.getElementById("kpi-val-indisp"), kpis.indisponiveis, false);
        animateCountUp(document.getElementById("kpi-val-pend"), kpis.totalPendencias, false);
    }

    // =========================================================================
    // PAGINA 1: VISAO GERAL (MUNICIPIO DE SAO PAULO)
    // =========================================================================
    function renderVisaoGeral(dfList, pendenciasList, kpis) {
        const view = document.getElementById("main-view-container");
        if (!view) return;

        if (dfList.length === 0) {
            view.innerHTML = renderEmptyState();
            return;
        }

        const ranking = dfList.slice().sort((a, b) => {
            if (a.df_percentual !== b.df_percentual) return a.df_percentual - b.df_percentual;
            return b.indisponiveis - a.indisponiveis;
        });

        view.innerHTML = `
            <div id="overview-kpis" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4 mb-6"></div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6">
                <!-- Grafico Principal 1: Comparativo de DF (%) entre os 3 Lotes -->
                <div class="lg:col-span-7 surface-card rounded-2xl p-6 border flex flex-col justify-between">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
                        <div>
                            <span class="text-[11px] font-mono uppercase tracking-wider text-blue-700 font-semibold block">DESEMPENHO REGIONAL • META CONTRATUAL 80,0%</span>
                            <h2 class="text-base sm:text-lg font-bold tracking-tight text-slate-900 mt-0.5">Disponibilidade Física (DF%) por Lote Regional vs. Meta de 80%</h2>
                            <p class="text-xs text-slate-500 mt-0.5">Comparativo direto entre os 3 lotes concedidos e a linha de corte contratual (80,0%)</p>
                        </div>
                        <div class="flex items-center gap-3 text-xs font-mono shrink-0">
                            <span class="inline-flex items-center gap-1.5 text-emerald-800 font-medium"><span class="w-2.5 h-2.5 rounded-sm bg-emerald-500"></span>≥ 80%</span>
                            <span class="inline-flex items-center gap-1.5 text-rose-800 font-medium"><span class="w-2.5 h-2.5 rounded-sm bg-rose-500"></span>&lt; 80%</span>
                        </div>
                    </div>
                    <div class="relative h-72 w-full">
                        <canvas id="chart-overview-lotes"></canvas>
                    </div>
                </div>

                <!-- Grafico Principal 2: Pendencias por Categoria -->
                <div class="lg:col-span-5 surface-card rounded-2xl p-6 border flex flex-col justify-between">
                    <div class="mb-4">
                        <span class="text-[11px] font-mono uppercase tracking-wider text-amber-700 font-semibold block">DIAGNÓSTICO TÉCNICO DE FALHAS</span>
                        <h2 class="text-base sm:text-lg font-bold tracking-tight text-slate-900 mt-0.5">Pendências Contratuais por Categoria Técnica</h2>
                        <p class="text-xs text-slate-500 mt-0.5">Distribuição das ordens de serviço ativas segundo a natureza do sistema</p>
                    </div>
                    <div class="relative h-72 w-full flex items-center justify-center">
                        <canvas id="chart-overview-categorias"></canvas>
                    </div>
                </div>
            </div>

            <!-- Tabela de Criticidade: Ranking das Baterias Mais Criticas -->
            <div class="surface-card rounded-2xl border overflow-hidden">
                <div class="p-6 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div>
                        <span class="text-[11px] font-mono uppercase tracking-wider text-rose-700 font-semibold block">AUDITORIA DE DISPONIBILIDADE FÍSICA & GATILHOS P1/P2</span>
                        <h2 class="text-lg font-bold tracking-tight text-slate-900 mt-0.5">Ranking de Criticidade dos Complexos Concedidos</h2>
                        <p class="text-xs text-slate-500 mt-0.5">Ordenado pelos menores índices de Disponibilidade Física (DF%) e maior volume de ativos indisponíveis</p>
                    </div>
                    <div class="flex flex-wrap items-center gap-2 text-xs font-mono">
                        <span class="px-2.5 py-1 rounded-md bg-rose-50 text-rose-700 border border-rose-200 font-medium">P1 (≥3 indisp.): ${kpis.totalP1}</span>
                        <span class="px-2.5 py-1 rounded-md bg-amber-50 text-amber-800 border border-amber-200 font-medium">P2 (1-2 indisp.): ${kpis.totalP2}</span>
                        <span class="px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200 font-medium">100% Disp.: ${kpis.totalSemPend}</span>
                    </div>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="border-b border-slate-200 text-[11px] font-mono uppercase tracking-wider text-slate-500 bg-slate-50">
                                <th class="py-3.5 px-4">Pos.</th>
                                <th class="py-3.5 px-4">Complexo Concedido</th>
                                <th class="py-3.5 px-4">Lote Regional / SPE</th>
                                <th class="py-3.5 px-4 text-center">Prioridade</th>
                                <th class="py-3.5 px-4 text-right">Total</th>
                                <th class="py-3.5 px-4 text-right">Disp.</th>
                                <th class="py-3.5 px-4 text-right">Indisp.</th>
                                <th class="py-3.5 px-4 w-52">Disponibilidade (DF%)</th>
                                <th class="py-3.5 px-4">Condição Contratual</th>
                                <th class="py-3.5 px-4 text-right">Ação</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 text-sm">
                            ${ranking.map((r, idx) => {
                                const isCrit = r.df_percentual < META_DF;
                                const barColor = isCrit ? "bg-rose-500" : (r.df_percentual < 90 ? "bg-amber-500" : "bg-emerald-500");
                                const textColor = isCrit ? "text-rose-700" : "text-emerald-700";
                                return `
                                <tr class="table-row-hover transition-colors">
                                    <td class="py-3.5 px-4 font-mono text-xs text-slate-400 font-semibold">#${String(idx + 1).padStart(2, "0")}</td>
                                    <td class="py-3.5 px-4 font-semibold text-slate-900">${r.bateria}</td>
                                    <td class="py-3.5 px-4">
                                        <div class="text-xs font-medium text-slate-800">${r.local_curto}</div>
                                        <div class="text-[11px] font-mono text-slate-500">${r.spe}</div>
                                    </td>
                                    <td class="py-3.5 px-4 text-center">${priorityBadgeHTML(r.prioridade)}</td>
                                    <td class="py-3.5 px-4 text-right font-mono text-slate-700">${r.total_ativos}</td>
                                    <td class="py-3.5 px-4 text-right font-mono text-emerald-700 font-medium">${r.disponiveis}</td>
                                    <td class="py-3.5 px-4 text-right font-mono font-bold ${r.indisponiveis >= 3 ? 'text-rose-700' : (r.indisponiveis > 0 ? 'text-amber-700' : 'text-slate-400')}">${r.indisponiveis}</td>
                                    <td class="py-3.5 px-4">
                                        <div class="flex items-center justify-between text-xs font-mono mb-1">
                                            <span class="font-bold ${textColor}">${formatPercent(r.df_percentual)}</span>
                                            <span class="text-[10px] text-slate-400">Meta 80%</span>
                                        </div>
                                        <div class="w-full h-2 bg-slate-100 rounded-full overflow-hidden relative">
                                            <div class="h-full ${barColor} rounded-full" style="width: ${Math.min(100, r.df_percentual)}%"></div>
                                            <div class="absolute top-0 bottom-0 w-0.5 bg-slate-400" style="left: 80%"></div>
                                        </div>
                                    </td>
                                    <td class="py-3.5 px-4">${condicaoBadgeHTML(r.condicao)}</td>
                                    <td class="py-3.5 px-4 text-right">
                                        <button type="button" data-drill-local="${r.local_id}" data-drill-bat="${r.bateria}" class="btn-drilldown inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-semibold bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 transition-colors cursor-pointer">
                                            Raio-X
                                            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                                        </button>
                                    </td>
                                </tr>`;
                            }).join("")}
                        </tbody>
                    </table>
                </div>
            </div>
        `;

        renderKPIStrip("overview-kpis", kpis, "Município de SP");
        bindDrilldownButtons();
        buildOverviewCharts(dfList, pendenciasList);
    }

    function buildOverviewCharts(dfList, pendenciasList) {
        const lotesAgg = DATA.meta.locais.map((l) => {
            const sub = dfList.filter((r) => r.local_id === l.id);
            const tot = sub.reduce((a, b) => a + b.total_ativos, 0);
            const disp = sub.reduce((a, b) => a + b.disponiveis, 0);
            const indisp = sub.reduce((a, b) => a + b.indisponiveis, 0);
            const df = tot > 0 ? Number(((disp / tot) * 100).toFixed(1)) : 0;
            return {
                label: l.nome_curto,
                df,
                tot,
                disp,
                indisp
            };
        });

        const ctx1 = document.getElementById("chart-overview-lotes");
        if (ctx1 && window.Chart) {
            chartInstances.overviewLotes = new Chart(ctx1, {
                type: "bar",
                data: {
                    labels: lotesAgg.map((x) => x.label),
                    datasets: [{
                        label: "Disponibilidade Física (DF%)",
                        data: lotesAgg.map((x) => x.df),
                        backgroundColor: lotesAgg.map((x) => x.df >= META_DF ? "rgba(16, 185, 129, 0.85)" : "rgba(244, 63, 94, 0.85)"),
                        borderColor: lotesAgg.map((x) => x.df >= META_DF ? "#059669" : "#E11D48"),
                        borderWidth: 1,
                        borderRadius: 8,
                        maxBarThickness: 48, borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        sppMetaLine: {
                            enabled: true,
                            value: META_DF,
                            color: "#D97706",
                            label: "Meta Contratual: 80,0%"
                        },
                        tooltip: {
                            backgroundColor: tk.tooltipBg,
                            titleColor: "#FFFFFF",
                            bodyColor: "#E2E8F0",
                            borderColor: tk.tooltipBorder,
                            borderWidth: 1,
                            padding: 12,
                            callbacks: {
                                label(ctx) {
                                    const item = lotesAgg[ctx.dataIndex];
                                    return [
                                        `DF Consolidada: ${formatPercent(item.df)} (Meta: 80,0%)`,
                                        `Disponíveis: ${item.disp} de ${item.tot} ativos`,
                                        `Indisponíveis: ${item.indisp} ativos`
                                    ];
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: { display: false },
                            ticks: { color: tk.textPrimary, font: { family: "'Geist', sans-serif", weight: "600", size: 12 } }
                        },
                        y: {
                            min: 50,
                            max: 100,
                            grid: { color: tk.gridColor },
                            ticks: {
                                color: tk.textSecondary,
                                font: { family: "'Geist Mono', monospace", size: 11 },
                                callback: (v) => v + "%"
                            }
                        }
                    }
                }
            });
        }

        const catCounts = {};
        pendenciasList.forEach((p) => {
            catCounts[p.categoria] = (catCounts[p.categoria] || 0) + 1;
        });
        const catEntries = Object.entries(catCounts).sort((a, b) => b[1] - a[1]);
        const palette = [tk.sppOrange, tk.sppBlue, tk.emerald, tk.indigo, tk.crimson];

        const ctx2 = document.getElementById("chart-overview-categorias");
        if (ctx2 && window.Chart) {
            chartInstances.overviewCat = new Chart(ctx2, {
                type: "doughnut",
                data: {
                    labels: catEntries.map((e) => e[0]),
                    datasets: [{
                        data: catEntries.map((e) => e[1]),
                        backgroundColor: palette,
                        borderColor: "#FFFFFF",
                        borderWidth: 2,
                        hoverOffset: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: "76%",
                    plugins: {
                        legend: {
                            position: "right",
                            labels: {
                                color: tk.textPrimary,
                                font: { family: "'Geist', sans-serif", size: 11 },
                                padding: 14,
                                usePointStyle: true
                            }
                        },
                        tooltip: {
                            backgroundColor: tk.tooltipBg,
                            titleColor: "#FFFFFF",
                            bodyColor: "#E2E8F0",
                            borderColor: tk.tooltipBorder,
                            borderWidth: 1,
                            padding: 12,
                            callbacks: {
                                label(ctx) {
                                    const val = ctx.parsed;
                                    const total = Math.max(1, pendenciasList.length);
                                    const pct = ((val / total) * 100).toFixed(1).replace(".", ",");
                                    return ` ${val} chamados (${pct}% do total)`;
                                }
                            }
                        }
                    }
                }
            });
        }
    }

    // =========================================================================
    // PAGINAS 2, 3 E 4: DETALHES POR LOCAL (LOTE 1, LOTE 2 E LOTE 3)
    // =========================================================================
    function renderLoteView(loteId, dfList, pendenciasList, kpis) {
        const view = document.getElementById("main-view-container");
        if (!view) return;

        const loteMeta = DATA.meta.locais.find((l) => l.id === loteId) || DATA.meta.locais[0];

        if (dfList.length === 0) {
            view.innerHTML = renderEmptyState();
            return;
        }

        const sortedBaterias = dfList.slice().sort((a, b) => a.df_percentual - b.df_percentual);

        view.innerHTML = `
            <!-- Banner Institucional do Lote -->
            <div class="surface-card rounded-2xl p-5 border mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <div class="flex flex-wrap items-center gap-2.5 mb-1">
                        <span class="px-2.5 py-0.5 rounded-md text-xs font-mono font-semibold bg-blue-50 text-blue-700 border border-blue-200">${loteMeta.contrato}</span>
                        <span class="text-xs font-mono text-slate-500">Concessionária Responsável: <strong class="text-slate-800">${loteMeta.spe}</strong></span>
                    </div>
                    <h2 class="text-xl sm:text-2xl font-bold tracking-tight text-slate-900">${loteMeta.nome}</h2>
                </div>
                <div class="flex items-center gap-3">
                    <div class="text-right font-mono">
                        <span class="text-[11px] text-slate-500 block uppercase">Complexos em P1 no Lote</span>
                        <span class="text-lg font-bold ${kpis.totalP1 > 0 ? 'text-rose-700' : 'text-emerald-700'}">${kpis.totalP1} de ${kpis.totalComplexos}</span>
                    </div>
                </div>
            </div>

            <div id="lote-kpis" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4 mb-6"></div>

            <!-- Linha 1 de Graficos do Lote -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6">
                <div class="lg:col-span-6 surface-card rounded-2xl p-6 border">
                    <div class="mb-4">
                        <span class="text-[11px] font-mono uppercase tracking-wider text-blue-700 font-semibold block">AUDITORIA POR COMPLEXO CONCEDIDO</span>
                        <h3 class="text-base sm:text-lg font-bold tracking-tight text-slate-900 mt-0.5">Disponibilidade Física (DF%) por Terminal e Complexo</h3>
                        <p class="text-xs text-slate-500 mt-0.5">Índice contratual individual frente à meta estrita de 80,0%</p>
                    </div>
                    <div class="relative h-72 w-full">
                        <canvas id="chart-lote-df"></canvas>
                    </div>
                </div>

                <div class="lg:col-span-6 surface-card rounded-2xl p-6 border">
                    <div class="mb-4">
                        <span class="text-[11px] font-mono uppercase tracking-wider text-emerald-700 font-semibold block">BALANÇO FÍSICO DE UNIDADES</span>
                        <h3 class="text-base sm:text-lg font-bold tracking-tight text-slate-900 mt-0.5">Ativos Disponíveis vs. Indisponíveis por Complexo</h3>
                        <p class="text-xs text-slate-500 mt-0.5">Volume de unidades ativas (verde) e paradas (vermelho) por equipamento concedido</p>
                    </div>
                    <div class="relative h-72 w-full">
                        <canvas id="chart-lote-stacked"></canvas>
                    </div>
                </div>
            </div>

            <!-- Linha 2 do Lote: Ranking de Prioridades + Categorias -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6">
                <div class="lg:col-span-7 surface-card rounded-2xl p-6 border">
                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <span class="text-[11px] font-mono uppercase tracking-wider text-rose-700 font-semibold block">MATRIZ DE PRIORIDADE OPERACIONAL</span>
                            <h3 class="text-base sm:text-lg font-bold tracking-tight text-slate-900 mt-0.5">Ranking de Prioridades do Lote (P1, P2 e Sem Pendência)</h3>
                        </div>
                    </div>
                    <div class="space-y-3">
                        ${sortedBaterias.map((b) => {
                            const isCrit = b.df_percentual < META_DF;
                            return `
                            <div class="p-3.5 rounded-xl border border-slate-200 bg-slate-50/60 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                                <div class="flex items-center gap-3">
                                    ${priorityBadgeHTML(b.prioridade)}
                                    <div>
                                        <div class="font-semibold text-sm text-slate-900">${b.bateria}</div>
                                        <div class="text-xs font-mono text-slate-500">${b.disponiveis}/${b.total_ativos} disponíveis • ${b.indisponiveis} parados</div>
                                    </div>
                                </div>
                                <div class="flex items-center gap-4">
                                    <div class="w-32">
                                        <div class="flex justify-between text-xs font-mono mb-1">
                                            <span class="font-bold ${isCrit ? 'text-rose-700' : 'text-emerald-700'}">${formatPercent(b.df_percentual)}</span>
                                            <span class="text-[10px] text-slate-500">${b.condicao}</span>
                                        </div>
                                        <div class="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                                            <div class="h-full ${isCrit ? 'bg-rose-500' : 'bg-emerald-500'}" style="width: ${b.df_percentual}%"></div>
                                        </div>
                                    </div>
                                    <button type="button" data-drill-local="${b.local_id}" data-drill-bat="${b.bateria}" class="btn-drilldown px-2.5 py-1.5 rounded-lg text-xs font-mono bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 cursor-pointer">
                                        Inspecionar
                                    </button>
                                </div>
                            </div>`;
                        }).join("")}
                    </div>
                </div>

                <div class="lg:col-span-5 surface-card rounded-2xl p-6 border flex flex-col justify-between">
                    <div class="mb-4">
                        <span class="text-[11px] font-mono uppercase tracking-wider text-amber-700 font-semibold block">PERFIL DE FALHAS DA CONCESSÃO</span>
                        <h3 class="text-base sm:text-lg font-bold tracking-tight text-slate-900 mt-0.5">Pendências por Categoria no Lote</h3>
                        <p class="text-xs text-slate-500 mt-0.5">Volume de chamados abertos filtrado para ${loteMeta.nome_curto}</p>
                    </div>
                    <div class="relative h-72 w-full">
                        <canvas id="chart-lote-categorias"></canvas>
                    </div>
                </div>
            </div>

            <!-- Tabela Detalhada de Pendencias por Unidade do Lote -->
            <div class="surface-card rounded-2xl border overflow-hidden">
                <div class="p-6 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div>
                        <span class="text-[11px] font-mono uppercase tracking-wider text-blue-700 font-semibold block">CHAMADOS CONTRATUAIS ATIVOS NO LOTE</span>
                        <h3 class="text-lg font-bold tracking-tight text-slate-900 mt-0.5">Tabela de Pendências por Ativo (${pendenciasList.length} registros)</h3>
                    </div>
                </div>
                ${renderPendenciasTableHTML(pendenciasList)}
            </div>
        `;

        renderKPIStrip("lote-kpis", kpis, loteMeta.nome_curto);
        bindDrilldownButtons();
        bindTicketModalButtons();
        buildLoteCharts(sortedBaterias, pendenciasList);
    }

    function buildLoteCharts(sortedBaterias, pendenciasList) {
        const labels = sortedBaterias.map((b) => b.bateria.replace("Terminal ", "Term. "));

        const ctxDF = document.getElementById("chart-lote-df");
        if (ctxDF && window.Chart) {
            chartInstances.loteDF = new Chart(ctxDF, {
                type: "bar",
                data: {
                    labels,
                    datasets: [{
                        label: "DF (%)",
                        data: sortedBaterias.map((b) => b.df_percentual),
                        backgroundColor: sortedBaterias.map((b) => b.df_percentual >= META_DF ? "rgba(37, 99, 235, 0.85)" : "rgba(244, 63, 94, 0.85)"),
                        borderColor: sortedBaterias.map((b) => b.df_percentual >= META_DF ? "#1D4ED8" : "#E11D48"),
                        borderWidth: 1,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        sppMetaLine: {
                            enabled: true,
                            value: META_DF,
                            color: "#D97706",
                            label: "Meta: 80,0%"
                        },
                        tooltip: {
                            backgroundColor: tk.tooltipBg,
                            titleColor: "#FFFFFF",
                            bodyColor: "#E2E8F0",
                            borderColor: tk.tooltipBorder,
                            borderWidth: 1
                        }
                    },
                    scales: {
                        x: {
                            grid: { display: false },
                            ticks: { color: tk.textSecondary, font: { size: 11 } }
                        },
                        y: {
                            min: 40,
                            max: 105,
                            grid: { color: tk.gridColor },
                            ticks: { color: tk.textSecondary, font: { family: "'Geist Mono', monospace", size: 11 }, callback: (v) => v + "%" }
                        }
                    }
                }
            });
        }

        const ctxStack = document.getElementById("chart-lote-stacked");
        if (ctxStack && window.Chart) {
            chartInstances.loteStacked = new Chart(ctxStack, {
                type: "bar",
                data: {
                    labels,
                    datasets: [
                        {
                            label: "Disponíveis",
                            data: sortedBaterias.map((b) => b.disponiveis),
                            backgroundColor: "rgba(16, 185, 129, 0.85)",
                            borderColor: "#059669",
                            borderWidth: 1,
                            borderRadius: 4
                        },
                        {
                            label: "Indisponíveis",
                            data: sortedBaterias.map((b) => b.indisponiveis),
                            backgroundColor: "rgba(244, 63, 94, 0.88)",
                            borderColor: "#E11D48",
                            borderWidth: 1,
                            borderRadius: 4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: "top",
                            labels: { color: tk.textPrimary, usePointStyle: true, font: { size: 11 } }
                        },
                        tooltip: {
                            backgroundColor: tk.tooltipBg,
                            titleColor: "#FFFFFF",
                            bodyColor: "#E2E8F0",
                            borderColor: tk.tooltipBorder,
                            borderWidth: 1
                        }
                    },
                    scales: {
                        x: { stacked: true, grid: { display: false }, ticks: { color: tk.textSecondary, font: { size: 11 } } },
                        y: { stacked: true, grid: { color: tk.gridColor }, ticks: { color: tk.textSecondary, font: { family: "'Geist Mono', monospace", size: 11 } } }
                    }
                }
            });
        }

        const catCounts = {};
        pendenciasList.forEach((p) => {
            catCounts[p.categoria] = (catCounts[p.categoria] || 0) + 1;
        });
        const entries = Object.entries(catCounts).sort((a, b) => b[1] - a[1]);

        const ctxCat = document.getElementById("chart-lote-categorias");
        if (ctxCat && window.Chart) {
            chartInstances.loteCat = new Chart(ctxCat, {
                type: "bar",
                data: {
                    labels: entries.map((e) => e[0]),
                    datasets: [{
                        label: "Pendências",
                        data: entries.map((e) => e[1]),
                        backgroundColor: "rgba(240, 130, 0, 0.85)",
                        borderColor: "#D97200",
                        borderWidth: 1,
                        borderRadius: 6
                    }]
                },
                options: {
                    indexAxis: "y",
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: { grid: { color: tk.gridColor }, ticks: { color: tk.textSecondary, stepSize: 1 } },
                        y: { grid: { display: false }, ticks: { color: tk.textPrimary, font: { size: 11 } } }
                    }
                }
            });
        }
    }

    // =========================================================================
    // PAGINA 5: GESTAO DE PENDENCIAS (DRILL-DOWN 3 NIVEIS + DATA GRID)
    // =========================================================================
    function renderPendenciasView(dfList, pendenciasList) {
        const view = document.getElementById("main-view-container");
        if (!view) return;

        const activeLocais = DATA.meta.locais;
        if (!activeLocais.some((l) => l.id === state.drilldown.selectedLocalId)) {
            state.drilldown.selectedLocalId = activeLocais[0].id;
        }
        const currLoteObj = activeLocais.find((l) => l.id === state.drilldown.selectedLocalId);
        const bateriasDoLote = dfList.filter((r) => r.local_id === state.drilldown.selectedLocalId);
        if (bateriasDoLote.length > 0 && !bateriasDoLote.some((b) => b.bateria === state.drilldown.selectedBateria)) {
            state.drilldown.selectedBateria = bateriasDoLote[0].bateria;
        }

        const catComplexo = DATA.meta.catalogo_complexos[state.drilldown.selectedBateria];
        const pendenciasComplexoMap = {};
        pendenciasList.filter((p) => p.bateria === state.drilldown.selectedBateria).forEach((p) => {
            pendenciasComplexoMap[p.unidade_num] = p;
        });

        const q = state.filters.searchQuery.trim().toLowerCase();
        const stFilter = state.filters.statusFilter;
        const filteredGrid = pendenciasList.filter((p) => {
            if (stFilter !== "all" && p.status !== stFilter) return false;
            if (!q) return true;
            return (
                p.id_chamado.toLowerCase().includes(q) ||
                p.bateria.toLowerCase().includes(q) ||
                p.ciclone.toLowerCase().includes(q) ||
                p.motivo.toLowerCase().includes(q) ||
                p.categoria.toLowerCase().includes(q)
            );
        });

        view.innerHTML = `
            <!-- Explorador de Drill-Down Interativo em 3 Niveis -->
            <div class="surface-card rounded-2xl p-6 border mb-6">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-5">
                    <div>
                        <span class="text-[11px] font-mono uppercase tracking-wider text-blue-700 font-semibold block">EXPLORADOR HIERÁRQUICO DE FISCALIZAÇÃO</span>
                        <h2 class="text-lg sm:text-xl font-bold tracking-tight text-slate-900 mt-0.5">Drill-Down: Lote Regional → Complexo Concedido → Ativo Físico</h2>
                    </div>
                    <span class="text-xs font-mono text-slate-500">Selecione o Lote e o Complexo para visualizar o raio-x individual dos ativos</span>
                </div>

                <!-- NIVEL 1: Cards dos 3 Lotes -->
                <div class="mb-5">
                    <div class="text-xs font-mono uppercase tracking-wider text-slate-500 mb-2.5">Nível 1 • Selecione o Lote Regional:</div>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        ${activeLocais.map((l) => {
                            const sub = dfList.filter((r) => r.local_id === l.id);
                            const tot = sub.reduce((a, b) => a + b.total_ativos, 0);
                            const disp = sub.reduce((a, b) => a + b.disponiveis, 0);
                            const indisp = sub.reduce((a, b) => a + b.indisponiveis, 0);
                            const df = tot > 0 ? ((disp / tot) * 100).toFixed(1).replace(".", ",") : "0,0";
                            const isSel = state.drilldown.selectedLocalId === l.id;
                            return `
                            <button type="button" data-dd-local="${l.id}" class="dd-local-btn text-left p-4 rounded-xl border transition-all cursor-pointer ${isSel ? 'bg-blue-50/90 border-blue-500 shadow-md ring-2 ring-blue-500/20' : 'bg-slate-50 border-slate-200 hover:border-slate-300'}">
                                <div class="flex items-center justify-between mb-1">
                                    <span class="text-xs font-mono font-bold ${isSel ? 'text-blue-700' : 'text-slate-500'}">${l.contrato}</span>
                                    <span class="text-sm font-mono font-bold ${parseFloat(df) >= 80 ? 'text-emerald-700' : 'text-rose-700'}">DF ${df}%</span>
                                </div>
                                <div class="font-bold text-sm sm:text-base text-slate-900 mb-1">${l.nome_curto}</div>
                                <div class="text-xs font-mono text-slate-500 flex items-center justify-between">
                                    <span>${sub.length} complexos</span>
                                    <span class="text-rose-700 font-semibold">${indisp} indisponíveis</span>
                                </div>
                            </button>`;
                        }).join("")}
                    </div>
                </div>

                <!-- NIVEL 2: Complexos do Lote Selecionado -->
                <div class="mb-5 pt-4 border-t border-slate-200">
                    <div class="text-xs font-mono uppercase tracking-wider text-slate-500 mb-2.5">Nível 2 • Complexos em ${currLoteObj.nome_curto}:</div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                        ${bateriasDoLote.map((b) => {
                            const isSel = state.drilldown.selectedBateria === b.bateria;
                            return `
                            <button type="button" data-dd-bat="${b.bateria}" class="dd-bat-btn text-left p-3.5 rounded-xl border transition-all cursor-pointer ${isSel ? 'bg-blue-50 border-blue-500 shadow-sm ring-2 ring-blue-500/20' : 'bg-slate-50/70 border-slate-200 hover:border-slate-300'}">
                                <div class="flex items-center justify-between gap-2 mb-1.5">
                                    <span class="font-semibold text-xs sm:text-sm text-slate-900 truncate">${b.bateria}</span>
                                    <span class="text-xs font-mono font-bold ${b.df_percentual >= 80 ? 'text-emerald-700' : 'text-rose-700'}">${formatPercent(b.df_percentual)}</span>
                                </div>
                                <div class="flex items-center justify-between">
                                    ${priorityBadgeHTML(b.prioridade)}
                                    <span class="text-[11px] font-mono text-slate-500">${b.indisponiveis} parados</span>
                                </div>
                            </button>`;
                        }).join("")}
                    </div>
                </div>

                <!-- NIVEL 3: Raio-X dos Ativos do Complexo Selecionado -->
                <div class="pt-4 border-t border-slate-200">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
                        <div class="text-xs font-mono uppercase tracking-wider text-emerald-800 font-semibold">
                            Nível 3 • Raio-X dos Ativos Físicos em <strong>${catComplexo ? catComplexo.bateria : ""}</strong>:
                        </div>
                        <span class="text-xs font-mono text-slate-500">Clique em um ativo com falha para abrir a Ficha de Fiscalização</span>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                        ${catComplexo ? catComplexo.unidades.map((u) => {
                            const pend = pendenciasComplexoMap[u.unidade_num];
                            if (pend) {
                                return `
                                <button type="button" data-ticket-id="${pend.id_chamado}" class="btn-open-ticket text-left p-3 rounded-xl border border-rose-300 bg-rose-50/80 hover:bg-rose-100/90 transition-all cursor-pointer">
                                    <div class="flex items-center justify-between text-[11px] font-mono mb-1">
                                        <span class="text-rose-700 font-bold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse"></span>${pend.id_chamado}</span>
                                        <span class="px-1.5 py-0.5 rounded bg-rose-200 text-rose-800 font-bold">${pend.prioridade}</span>
                                    </div>
                                    <div class="font-semibold text-xs text-slate-900 truncate mb-0.5">${u.ciclone}</div>
                                    <div class="text-[11px] text-rose-800 truncate">${pend.motivo}</div>
                                </button>`;
                            }
                            return `
                            <div class="p-3 rounded-xl border border-slate-200 bg-slate-50">
                                <div class="flex items-center justify-between text-[11px] font-mono mb-1">
                                    <span class="text-emerald-700 font-semibold">● OPERACIONAL</span>
                                    <span class="text-slate-400">100%</span>
                                </div>
                                <div class="font-medium text-xs text-slate-800 truncate mb-0.5">${u.ciclone}</div>
                                <div class="text-[11px] text-slate-500 truncate">${u.categoria}</div>
                            </div>`;
                        }).join("") : ""}
                    </div>
                </div>
            </div>

            <!-- 4 Visuais de Gestao: Status, Motivo, Categoria e Prioridade -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-6">
                <div class="surface-card rounded-2xl p-5 border">
                    <span class="text-[10px] font-mono uppercase tracking-wider text-blue-700 font-semibold block">GESTÃO DE SLA</span>
                    <h3 class="text-sm font-bold text-slate-900 mt-0.5 mb-3">Por Status do Chamado</h3>
                    <div class="relative h-48 w-full"><canvas id="chart-pend-status"></canvas></div>
                </div>
                <div class="surface-card rounded-2xl p-5 border">
                    <span class="text-[10px] font-mono uppercase tracking-wider text-amber-700 font-semibold block">CAUSA RAIZ</span>
                    <h3 class="text-sm font-bold text-slate-900 mt-0.5 mb-3">Por Motivo da Falha</h3>
                    <div class="relative h-48 w-full"><canvas id="chart-pend-motivo"></canvas></div>
                </div>
                <div class="surface-card rounded-2xl p-5 border">
                    <span class="text-[10px] font-mono uppercase tracking-wider text-emerald-700 font-semibold block">DISCIPLINA TÉCNICA</span>
                    <h3 class="text-sm font-bold text-slate-900 mt-0.5 mb-3">Por Categoria</h3>
                    <div class="relative h-48 w-full"><canvas id="chart-pend-cat"></canvas></div>
                </div>
                <div class="surface-card rounded-2xl p-5 border">
                    <span class="text-[10px] font-mono uppercase tracking-wider text-rose-700 font-semibold block">IMPACTO CONTRATUAL</span>
                    <h3 class="text-sm font-bold text-slate-900 mt-0.5 mb-3">Severidade (P1 vs P2)</h3>
                    <div class="relative h-48 w-full"><canvas id="chart-pend-prio"></canvas></div>
                </div>
            </div>

            <!-- Data Grid Completo de Fiscalizacao -->
            <div class="surface-card rounded-2xl border overflow-hidden">
                <div class="p-6 border-b border-slate-200 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                    <div>
                        <span class="text-[11px] font-mono uppercase tracking-wider text-blue-700 font-semibold block">DATA GRID DE AUDITORIA E FISCALIZAÇÃO</span>
                        <h3 class="text-lg font-bold tracking-tight text-slate-900 mt-0.5">Registro Geral de Não-Conformidades (${filteredGrid.length} de ${pendenciasList.length})</h3>
                    </div>
                    <div class="flex flex-wrap items-center gap-3">
                        <div class="relative">
                            <input id="input-grid-search" type="search" value="${state.filters.searchQuery}" placeholder="Buscar chamado, complexo, ativo..." class="input-control pl-9 pr-4 py-2 rounded-xl text-xs font-mono w-64 border focus:outline-none focus:ring-2 focus:ring-blue-500" />
                            <svg class="w-4 h-4 text-slate-400 absolute left-3 top-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                        </div>
                        <select id="select-grid-status" class="input-control px-3 py-2 rounded-xl text-xs font-mono border focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="all">Todos os Status</option>
                            <option value="Em Atendimento pela SPE" ${stFilter === "Em Atendimento pela SPE" ? "selected" : ""}>Em Atendimento</option>
                            <option value="Autuado / Prazo Vencido" ${stFilter === "Autuado / Prazo Vencido" ? "selected" : ""}>Autuado / Prazo Vencido</option>
                            <option value="Aguardando Peça Importada" ${stFilter === "Aguardando Peça Importada" ? "selected" : ""}>Aguardando Peça</option>
                            <option value="Em Vistoria Técnica" ${stFilter === "Em Vistoria Técnica" ? "selected" : ""}>Em Vistoria Técnica</option>
                        </select>
                    </div>
                </div>
                ${renderPendenciasTableHTML(filteredGrid)}
            </div>
        `;

        document.querySelectorAll(".dd-local-btn").forEach((btn) => {
            btn.addEventListener("click", () => {
                state.drilldown.selectedLocalId = btn.getAttribute("data-dd-local");
                const sub = dfList.filter((r) => r.local_id === state.drilldown.selectedLocalId);
                if (sub.length > 0) state.drilldown.selectedBateria = sub[0].bateria;
                renderAll();
            });
        });

        document.querySelectorAll(".dd-bat-btn").forEach((btn) => {
            btn.addEventListener("click", () => {
                state.drilldown.selectedBateria = btn.getAttribute("data-dd-bat");
                renderAll();
            });
        });

        const searchInput = document.getElementById("input-grid-search");
        if (searchInput) {
            searchInput.addEventListener("input", (e) => {
                state.filters.searchQuery = e.target.value;
                renderAll();
                const el = document.getElementById("input-grid-search");
                if (el) {
                    el.focus();
                    el.setSelectionRange(el.value.length, el.value.length);
                }
            });
        }

        const statusSelect = document.getElementById("select-grid-status");
        if (statusSelect) {
            statusSelect.addEventListener("change", (e) => {
                state.filters.statusFilter = e.target.value;
                renderAll();
            });
        }

        bindTicketModalButtons();
        buildPendenciasCharts(pendenciasList);
    }

    function renderPendenciasTableHTML(list) {
        if (list.length === 0) {
            return `
                <div class="p-10 text-center">
                    <p class="text-sm font-semibold text-slate-800 mb-1">Nenhuma pendência encontrada para os critérios selecionados.</p>
                    <p class="text-xs text-slate-500">Ajuste a busca textual ou limpe os filtros no cabeçalho para visualizar todos os chamados.</p>
                </div>
            `;
        }
        return `
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="border-b border-slate-200 text-[11px] font-mono uppercase tracking-wider text-slate-500 bg-slate-50">
                            <th class="py-3.5 px-4">ID Chamado</th>
                            <th class="py-3.5 px-4">Data</th>
                            <th class="py-3.5 px-4">Lote Regional</th>
                            <th class="py-3.5 px-4">Complexo Concedido</th>
                            <th class="py-3.5 px-4">Ativo Afetado</th>
                            <th class="py-3.5 px-4">Status</th>
                            <th class="py-3.5 px-4">Motivo da Pendência</th>
                            <th class="py-3.5 px-4">Categoria</th>
                            <th class="py-3.5 px-4 text-center">Prioridade</th>
                            <th class="py-3.5 px-4 text-right">Ficha</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100 text-xs sm:text-sm">
                        ${list.map((p) => {
                            const isAutuado = p.status.includes("Autuado");
                            return `
                            <tr class="table-row-hover transition-colors">
                                <td class="py-3 px-4 font-mono font-bold text-blue-700">${p.id_chamado}</td>
                                <td class="py-3 px-4 font-mono text-xs text-slate-500">${formatDateBR(p.data)}</td>
                                <td class="py-3 px-4 text-xs text-slate-700">${p.local_curto}</td>
                                <td class="py-3 px-4 font-semibold text-slate-900">${p.bateria}</td>
                                <td class="py-3 px-4 font-mono text-xs text-slate-800">${p.ciclone}</td>
                                <td class="py-3 px-4">
                                    <span class="px-2 py-0.5 rounded text-xs font-mono font-medium ${isAutuado ? 'bg-rose-50 text-rose-700 border border-rose-200' : 'bg-slate-100 text-slate-700'}">${p.status}</span>
                                </td>
                                <td class="py-3 px-4 text-xs text-slate-700">${p.motivo}</td>
                                <td class="py-3 px-4 text-xs text-slate-500">${p.categoria}</td>
                                <td class="py-3 px-4 text-center">${priorityBadgeHTML(p.prioridade)}</td>
                                <td class="py-3 px-4 text-right">
                                    <button type="button" data-ticket-id="${p.id_chamado}" class="btn-open-ticket px-2.5 py-1 rounded-lg text-xs font-mono bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 cursor-pointer">
                                        Ficha
                                    </button>
                                </td>
                            </tr>`;
                        }).join("")}
                    </tbody>
                </table>
            </div>
        `;
    }

    function buildPendenciasCharts(pendenciasList) {
        function countBy(fn) {
            const m = {};
            pendenciasList.forEach((p) => {
                const k = fn(p);
                m[k] = (m[k] || 0) + 1;
            });
            return Object.entries(m).sort((a, b) => b[1] - a[1]);
        }

        const stEntries = countBy((p) => p.status);
        const motEntries = countBy((p) => p.motivo);
        const catEntries = countBy((p) => p.categoria);
        const prioEntries = countBy((p) => p.prioridade);

        const commonBarOpts = (color) => ({
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { color: tk.gridColor }, ticks: { color: tk.textSecondary, font: { size: 10 }, stepSize: 1 } },
                y: { grid: { display: false }, ticks: { color: tk.textPrimary, font: { size: 10 } } }
            }
        });

        const c1 = document.getElementById("chart-pend-status");
        if (c1 && window.Chart) {
            chartInstances.pendStatus = new Chart(c1, {
                type: "bar",
                data: {
                    labels: stEntries.map((e) => e[0]),
                    datasets: [{ data: stEntries.map((e) => e[1]), backgroundColor: tk.royal, borderRadius: 4 }]
                },
                options: commonBarOpts(tk.royal)
            });
        }

        const c2 = document.getElementById("chart-pend-motivo");
        if (c2 && window.Chart) {
            chartInstances.pendMotivo = new Chart(c2, {
                type: "bar",
                data: {
                    labels: motEntries.map((e) => e[0]),
                    datasets: [{ data: motEntries.map((e) => e[1]), backgroundColor: tk.amber, borderRadius: 4 }]
                },
                options: commonBarOpts(tk.amber)
            });
        }

        const c3 = document.getElementById("chart-pend-cat");
        if (c3 && window.Chart) {
            chartInstances.pendCat = new Chart(c3, {
                type: "bar",
                data: {
                    labels: catEntries.map((e) => e[0]),
                    datasets: [{ data: catEntries.map((e) => e[1]), backgroundColor: tk.emerald, borderRadius: 4 }]
                },
                options: commonBarOpts(tk.emerald)
            });
        }

        const c4 = document.getElementById("chart-pend-prio");
        if (c4 && window.Chart) {
            chartInstances.pendPrio = new Chart(c4, {
                type: "doughnut",
                data: {
                    labels: prioEntries.map((e) => e[0]),
                    datasets: [{
                        data: prioEntries.map((e) => e[1]),
                        backgroundColor: prioEntries.map((e) => e[0] === "P1" ? tk.crimson : tk.amber),
                        borderWidth: 2,
                        borderColor: "#FFFFFF"
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: "60%",
                    plugins: {
                        legend: { position: "bottom", labels: { color: tk.textPrimary, font: { size: 11 } } }
                    }
                }
            });
        }
    }

    // =========================================================================
    // PAGINA 6: HISTORICO E EVOLUCAO CONTRATUAL (SERIE DE 30 DIAS)
    // =========================================================================
    function renderHistoricoView() {
        const view = document.getElementById("main-view-container");
        if (!view) return;

        view.innerHTML = `
            <div class="surface-card rounded-2xl p-6 border mb-6">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
                    <div>
                        <span class="text-[11px] font-mono uppercase tracking-wider text-emerald-800 font-semibold block">SÉRIE HISTÓRICA DE 30 DIAS • ${formatDateBR(DATA.meta.data_inicio)} A ${formatDateBR(DATA.meta.data_atual)}</span>
                        <h2 class="text-lg sm:text-xl font-bold tracking-tight text-slate-900 mt-0.5">1. Evolução da Disponibilidade Física Geral (DF%) vs. Meta Contratual (80,0%)</h2>
                        <p class="text-xs text-slate-500 mt-0.5">Comportamento diário consolidado considerando os filtros de Lote e Complexo ativos</p>
                    </div>
                </div>
                <div class="relative h-72 w-full">
                    <canvas id="chart-hist-df-geral"></canvas>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                <!-- Grafico 2: Evolucao diaria de Indisponiveis -->
                <div class="surface-card rounded-2xl p-6 border">
                    <span class="text-[11px] font-mono uppercase tracking-wider text-amber-700 font-semibold block">VOLUME DE INDISPONIBILIDADE</span>
                    <h3 class="text-base font-bold tracking-tight text-slate-900 mt-0.5 mb-3">2. Evolução Diária de Ativos Indisponíveis</h3>
                    <div class="relative h-60 w-full"><canvas id="chart-hist-indisp"></canvas></div>
                </div>

                <!-- Grafico 3: Evolucao do volume de Pendencias Abertas -->
                <div class="surface-card rounded-2xl p-6 border">
                    <span class="text-[11px] font-mono uppercase tracking-wider text-blue-700 font-semibold block">CHAMADOS CONTRATUAIS</span>
                    <h3 class="text-base font-bold tracking-tight text-slate-900 mt-0.5 mb-3">3. Evolução de Pendências Abertas no Tempo</h3>
                    <div class="relative h-60 w-full"><canvas id="chart-hist-pend"></canvas></div>
                </div>

                <!-- Grafico 4: Evolucao exclusiva dos P1 -->
                <div class="surface-card rounded-2xl p-6 border">
                    <span class="text-[11px] font-mono uppercase tracking-wider text-rose-700 font-semibold block">GATILHO DE SEVERIDADE MÁXIMA</span>
                    <h3 class="text-base font-bold tracking-tight text-slate-900 mt-0.5 mb-3">4. Evolução Exclusiva de Críticos (P1 • ≥3 Indisp.)</h3>
                    <div class="relative h-60 w-full"><canvas id="chart-hist-p1"></canvas></div>
                </div>
            </div>

            <!-- Grafico 5: Comparativo Historico 3 Lotes -->
            <div class="surface-card rounded-2xl p-6 border">
                <div class="mb-4">
                    <span class="text-[11px] font-mono uppercase tracking-wider text-indigo-700 font-semibold block">BENCHMARKING TEMPORAL ENTRE REGIÕES</span>
                    <h2 class="text-lg font-bold tracking-tight text-slate-900 mt-0.5">5. Comparativo Histórico de DF (%) entre os 3 Lotes Regionais (30 Dias)</h2>
                    <p class="text-xs text-slate-500 mt-0.5">Análise comparativa das 3 curvas de concessão demonstrando o impacto do evento climático nos dias 30/09 a 04/10 e a recuperação contratual</p>
                </div>
                <div class="relative h-80 w-full">
                    <canvas id="chart-hist-lotes"></canvas>
                </div>
            </div>
        `;

        buildHistoricoCharts();
    }

    function buildHistoricoCharts() {
        const effLocal = getEffectiveLocalFilter();
        const fBat = state.filters.bateria;
        const fCat = state.filters.categoria;

        const labels = ALL_DATES.map(formatShortDateBR);
        const seriesDF = [];
        const seriesIndisp = [];
        const seriesPend = [];
        const seriesP1 = [];

        const lotesCurves = {
            lote_1: [],
            lote_2: [],
            lote_3: []
        };

        ALL_DATES.forEach((d) => {
            const dayDF = DATA.disponibilidade_fisica.filter((r) => {
                if (r.data !== d) return false;
                if (effLocal !== "all" && r.local_id !== effLocal) return false;
                if (fBat !== "all" && r.bateria !== fBat) return false;
                return true;
            });

            const dayPend = DATA.pendencias.filter((p) => {
                if (p.data !== d) return false;
                if (effLocal !== "all" && p.local_id !== effLocal) return false;
                if (fBat !== "all" && p.bateria !== fBat) return false;
                if (fCat !== "all" && p.categoria !== fCat) return false;
                return true;
            });

            const tot = dayDF.reduce((a, b) => a + b.total_ativos, 0);
            const disp = dayDF.reduce((a, b) => a + b.disponiveis, 0);
            const indisp = dayDF.reduce((a, b) => a + b.indisponiveis, 0);
            const dfPct = tot > 0 ? Number(((disp / tot) * 100).toFixed(1)) : 0;
            const p1Count = dayDF.filter((r) => r.prioridade === "P1").length;

            seriesDF.push(dfPct);
            seriesIndisp.push(indisp);
            seriesPend.push(dayPend.length);
            seriesP1.push(p1Count);

            ["lote_1", "lote_2", "lote_3"].forEach((lid) => {
                const sub = DATA.disponibilidade_fisica.filter((r) => r.data === d && r.local_id === lid);
                const tL = sub.reduce((a, b) => a + b.total_ativos, 0);
                const dL = sub.reduce((a, b) => a + b.disponiveis, 0);
                lotesCurves[lid].push(tL > 0 ? Number(((dL / tL) * 100).toFixed(1)) : 0);
            });
        });

        const c1 = document.getElementById("chart-hist-df-geral");
        if (c1 && window.Chart) {
            const ctx = c1.getContext("2d");
            const grad = ctx.createLinearGradient(0, 0, 0, 280);
            grad.addColorStop(0, "rgba(5, 150, 105, 0.08)");
            grad.addColorStop(1, "rgba(16, 185, 129, 0.0)");

            chartInstances.histDF = new Chart(c1, {
                type: "line",
                data: {
                    labels,
                    datasets: [{
                        label: "DF Geral (%)",
                        data: seriesDF,
                        borderColor: "#059669",
                        backgroundColor: grad,
                        borderWidth: 2,
                        fill: true,
                        tension: 0.32,
                        pointRadius: 0, pointHoverRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        sppMetaLine: {
                            enabled: true,
                            value: META_DF,
                            color: "#D97706",
                            label: "Meta Contratual: 80,0%"
                        }
                    },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: tk.textSecondary, font: { family: "'Geist Mono', monospace", size: 10 } } },
                        y: { min: 70, max: 100, grid: { color: tk.gridColor }, ticks: { color: tk.textSecondary, font: { family: "'Geist Mono', monospace", size: 11 }, callback: (v) => v + "%" } }
                    }
                }
            });
        }

        const c2 = document.getElementById("chart-hist-indisp");
        if (c2 && window.Chart) {
            chartInstances.histIndisp = new Chart(c2, {
                type: "bar",
                data: {
                    labels,
                    datasets: [{
                        label: "Indisponíveis",
                        data: seriesIndisp,
                        backgroundColor: "rgba(245, 158, 11, 0.85)",
                        borderRadius: 3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: tk.textSecondary, font: { size: 9 }, maxTicksLimit: 10 } },
                        y: { grid: { color: tk.gridColor }, ticks: { color: tk.textSecondary, font: { family: "'Geist Mono', monospace", size: 10 } } }
                    }
                }
            });
        }

        const c3 = document.getElementById("chart-hist-pend");
        if (c3 && window.Chart) {
            chartInstances.histPend = new Chart(c3, {
                type: "line",
                data: {
                    labels,
                    datasets: [{
                        label: "Pendências Abertas",
                        data: seriesPend,
                        borderColor: tk.royal,
                        backgroundColor: "rgba(37, 99, 235, 0.06)",
                        fill: true,
                        tension: 0.3,
                        borderWidth: 2,
                        pointRadius: 0, pointHoverRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: tk.textSecondary, font: { size: 9 }, maxTicksLimit: 10 } },
                        y: { grid: { color: tk.gridColor }, ticks: { color: tk.textSecondary, font: { family: "'Geist Mono', monospace", size: 10 } } }
                    }
                }
            });
        }

        const c4 = document.getElementById("chart-hist-p1");
        if (c4 && window.Chart) {
            chartInstances.histP1 = new Chart(c4, {
                type: "line",
                data: {
                    labels,
                    datasets: [{
                        label: "Complexos em P1",
                        data: seriesP1,
                        borderColor: tk.crimson,
                        backgroundColor: "rgba(225, 29, 72, 0.06)",
                        fill: true,
                        tension: 0.25,
                        borderWidth: 2,
                        pointRadius: 0, pointHoverRadius: 4,
                        pointBackgroundColor: tk.crimson
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: tk.textSecondary, font: { size: 9 }, maxTicksLimit: 10 } },
                        y: { beginAtZero: true, grid: { color: tk.gridColor }, ticks: { color: tk.textSecondary, stepSize: 1, font: { family: "'Geist Mono', monospace", size: 10 } } }
                    }
                }
            });
        }

        const c5 = document.getElementById("chart-hist-lotes");
        if (c5 && window.Chart) {
            const lNames = DATA.meta.locais.map((l) => l.nome_curto);
            chartInstances.histLotes = new Chart(c5, {
                type: "line",
                data: {
                    labels,
                    datasets: [
                        {
                            label: lNames[0],
                            data: lotesCurves.lote_1,
                            borderColor: tk.royal,
                            backgroundColor: "transparent",
                            borderWidth: 2,
                            tension: 0.32,
                            pointRadius: 0, pointHoverRadius: 4
                        },
                        {
                            label: lNames[1],
                            data: lotesCurves.lote_2,
                            borderColor: tk.sppOrange,
                            backgroundColor: "transparent",
                            borderWidth: 2,
                            tension: 0.32,
                            pointRadius: 0, pointHoverRadius: 4
                        },
                        {
                            label: lNames[2],
                            data: lotesCurves.lote_3,
                            borderColor: tk.emerald,
                            backgroundColor: "transparent",
                            borderWidth: 2,
                            tension: 0.32,
                            pointRadius: 0, pointHoverRadius: 4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: "top",
                            labels: { color: tk.textPrimary, usePointStyle: true, font: { size: 12 } }
                        },
                        sppMetaLine: {
                            enabled: true,
                            value: META_DF,
                            color: "#D97706",
                            label: "Meta Contratual: 80,0%"
                        }
                    },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: tk.textSecondary, font: { family: "'Geist Mono', monospace", size: 10 } } },
                        y: { min: 65, max: 100, grid: { color: tk.gridColor }, ticks: { color: tk.textSecondary, font: { family: "'Geist Mono', monospace", size: 11 }, callback: (v) => v + "%" } }
                    }
                }
            });
        }
    }

    function renderEmptyState() {
        return `
            <div class="surface-card rounded-2xl p-12 border text-center my-8 max-w-xl mx-auto">
                <div class="w-12 h-12 rounded-2xl bg-blue-50 border border-blue-200 text-blue-700 flex items-center justify-center mx-auto mb-4">
                    <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/></svg>
                </div>
                <h3 class="text-lg font-bold text-slate-900 mb-2">Nenhum complexo ou ativo corresponde à combinação de filtros</h3>
                <p class="text-xs sm:text-sm text-slate-500 mb-6">A combinação atual de Período, Complexo, Categoria e Prioridade retornou zero registros. Limpe os filtros para restaurar a visão consolidada.</p>
                <button type="button" id="btn-empty-reset" class="px-5 py-2.5 rounded-xl text-xs font-mono font-semibold bg-blue-600 hover:bg-blue-700 text-white transition-colors cursor-pointer">
                    Restaurar Todos os Filtros
                </button>
            </div>
        `;
    }

    function bindDrilldownButtons() {
        document.querySelectorAll(".btn-drilldown").forEach((btn) => {
            btn.addEventListener("click", () => {
                const lid = btn.getAttribute("data-drill-local");
                const bat = btn.getAttribute("data-drill-bat");
                state.drilldown.selectedLocalId = lid;
                state.drilldown.selectedBateria = bat;
                setActivePage("pendencias");
            });
        });

        const emptyReset = document.getElementById("btn-empty-reset");
        if (emptyReset) {
            emptyReset.addEventListener("click", resetFilters);
        }
    }

    function bindTicketModalButtons() {
        document.querySelectorAll(".btn-open-ticket").forEach((btn) => {
            btn.addEventListener("click", () => {
                const tid = btn.getAttribute("data-ticket-id");
                const ticket = DATA.pendencias.find((p) => p.id_chamado === tid);
                if (ticket) openTicketModal(ticket);
            });
        });
    }

    function openTicketModal(ticket) {
        state.modalTicket = ticket;
        const modal = document.getElementById("ticket-modal");
        const content = document.getElementById("ticket-modal-body");
        if (!modal || !content) return;

        content.innerHTML = `
            <div class="flex items-center justify-between border-b border-slate-200 pb-4 mb-4">
                <div>
                    <span class="text-xs font-mono text-blue-700 font-semibold block">Auto de Infração / Chamado</span>
                    <h3 class="text-xl font-mono font-bold text-slate-900 mt-0.5">${ticket.id_chamado}</h3>
                </div>
                ${priorityBadgeHTML(ticket.prioridade)}
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs mb-5">
                <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
                    <span class="text-slate-500 font-mono block mb-0.5">Lote Regional:</span>
                    <strong class="text-sm text-slate-900">${ticket.local}</strong>
                </div>
                <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
                    <span class="text-slate-500 font-mono block mb-0.5">Complexo Concedido:</span>
                    <strong class="text-sm text-slate-900">${ticket.bateria}</strong>
                </div>
                <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
                    <span class="text-slate-500 font-mono block mb-0.5">Ativo Monitorado:</span>
                    <strong class="text-sm font-mono text-amber-800">${ticket.ciclone}</strong>
                </div>
                <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
                    <span class="text-slate-500 font-mono block mb-0.5">Concessionária Responsável:</span>
                    <strong class="text-sm text-slate-900">${ticket.spe}</strong>
                </div>
                <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
                    <span class="text-slate-500 font-mono block mb-0.5">Categoria Técnica:</span>
                    <strong class="text-sm text-slate-900">${ticket.categoria}</strong>
                </div>
                <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
                    <span class="text-slate-500 font-mono block mb-0.5">Motivo da Não-Conformidade:</span>
                    <strong class="text-sm text-rose-700">${ticket.motivo}</strong>
                </div>
                <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
                    <span class="text-slate-500 font-mono block mb-0.5">Status Atual:</span>
                    <strong class="text-sm text-slate-900">${ticket.status}</strong>
                </div>
                <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
                    <span class="text-slate-500 font-mono block mb-0.5">Tempo Decorrido & Glosa:</span>
                    <strong class="text-sm font-mono text-slate-900">${ticket.sla_horas}h em aberto • Glosa: R$ ${formatNumber(ticket.glosa_brl)}</strong>
                </div>
            </div>
            <div class="p-3.5 rounded-xl bg-blue-50 border border-blue-200 text-xs text-slate-700 flex items-center justify-between">
                <span>Registro auditado pelo Centro de Controle de Concessões (${formatDateBR(ticket.data)})</span>
                <span class="font-mono text-blue-700 font-semibold">Meta DF ≥ 80,0%</span>
            </div>
        `;

        modal.classList.remove("hidden");
        modal.classList.add("flex");
    }

    function closeTicketModal() {
        const modal = document.getElementById("ticket-modal");
        if (!modal) return;
        modal.classList.add("hidden");
        modal.classList.remove("flex");
        state.modalTicket = null;
    }

    function exportCurrentCSV() {
        const { dfList } = getFilteredData();
        const headers = ["Lote_Regional", "Complexo_Concedido", "Total_Ativos", "Disponiveis", "Indisponiveis", "DF_Percentual", "Prioridade", "Condicao"];
        const rows = dfList.map((r) => [
            `"${r.local}"`,
            `"${r.bateria}"`,
            r.total_ativos,
            r.disponiveis,
            r.indisponiveis,
            r.df_percentual,
            `"${r.prioridade}"`,
            `"${r.condicao}"`
        ]);
        const csv = [headers.join(";"), ...rows.map((r) => r.join(";"))].join("\n");
        const blob = new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8;" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `relatorio_df_spp_${state.activePage}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    function setActivePage(pageId) {
        state.activePage = pageId;
        document.querySelectorAll("[data-nav-id]").forEach((btn) => {
            if (btn.getAttribute("data-nav-id") === pageId) {
                btn.classList.add("nav-item-active");
            } else {
                btn.classList.remove("nav-item-active");
            }
        });
        const sidebar = document.getElementById("app-sidebar");
        if (sidebar && window.innerWidth < 1024) {
            sidebar.classList.add("-translate-x-full");
        }
        renderAll();
    }

    function resetFilters() {
        state.filters = {
            periodo: "ultimo_dia",
            localId: "all",
            bateria: "all",
            categoria: "all",
            prioridade: "all",
            searchQuery: "",
            statusFilter: "all"
        };
        const selP = document.getElementById("select-periodo");
        const selPrio = document.getElementById("select-prioridade");
        if (selP) selP.value = "ultimo_dia";
        if (selPrio) selPrio.value = "all";
        renderAll();
    }

    function renderAll() {
        destroyAllCharts();
        populateFilterDropdowns();

        const { dfList, pendenciasList } = getFilteredData();
        const kpis = computeKPIs(dfList, pendenciasList);

        if (state.activePage === "visao_geral") {
            renderVisaoGeral(dfList, pendenciasList, kpis);
        } else if (["lote_1", "lote_2", "lote_3"].includes(state.activePage)) {
            renderLoteView(state.activePage, dfList, pendenciasList, kpis);
        } else if (state.activePage === "pendencias") {
            renderPendenciasView(dfList, pendenciasList);
        } else if (state.activePage === "historico") {
            renderHistoricoView();
        }
    }

    function initEvents() {
        document.querySelectorAll("[data-nav-id]").forEach((btn) => {
            btn.addEventListener("click", () => {
                setActivePage(btn.getAttribute("data-nav-id"));
            });
        });

        const selP = document.getElementById("select-periodo");
        if (selP) {
            selP.addEventListener("change", (e) => {
                state.filters.periodo = e.target.value;
                renderAll();
            });
        }

        const selL = document.getElementById("select-local");
        if (selL) {
            selL.addEventListener("change", (e) => {
                state.filters.localId = e.target.value;
                state.filters.bateria = "all";
                renderAll();
            });
        }

        const selB = document.getElementById("select-bateria");
        if (selB) {
            selB.addEventListener("change", (e) => {
                state.filters.bateria = e.target.value;
                renderAll();
            });
        }

        const selC = document.getElementById("select-categoria");
        if (selC) {
            selC.addEventListener("change", (e) => {
                state.filters.categoria = e.target.value;
                renderAll();
            });
        }

        const selPrio = document.getElementById("select-prioridade");
        if (selPrio) {
            selPrio.addEventListener("change", (e) => {
                state.filters.prioridade = e.target.value;
                renderAll();
            });
        }

        const btnReset = document.getElementById("btn-reset-filters");
        if (btnReset) {
            btnReset.addEventListener("click", resetFilters);
        }

        const btnExport = document.getElementById("btn-export-csv");
        if (btnExport) {
            btnExport.addEventListener("click", exportCurrentCSV);
        }

        const btnCloseModal = document.getElementById("btn-close-modal");
        const modalBackdrop = document.getElementById("ticket-modal");
        if (btnCloseModal) btnCloseModal.addEventListener("click", closeTicketModal);
        if (modalBackdrop) {
            modalBackdrop.addEventListener("click", (e) => {
                if (e.target === modalBackdrop) closeTicketModal();
            });
        }
        window.addEventListener("keydown", (e) => {
            if (e.key === "Escape") closeTicketModal();
        });

        const btnMobileMenu = document.getElementById("btn-mobile-sidebar");
        const sidebar = document.getElementById("app-sidebar");
        if (btnMobileMenu && sidebar) {
            btnMobileMenu.addEventListener("click", () => {
                sidebar.classList.toggle("-translate-x-full");
            });
        }
    }

    document.addEventListener("DOMContentLoaded", () => {
        initEvents();
        setActivePage("visao_geral");
    });
})();
