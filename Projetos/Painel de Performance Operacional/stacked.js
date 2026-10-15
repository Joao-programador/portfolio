// Custom Legend Plugin for Chart.js in Stacked Layout (using circles as markers)
const htmlLegendPlugin = {
  id: "htmlLegend",
  afterUpdate(chart, args, options) {
    if (!options.containerID) return;
    const container = document.getElementById(options.containerID);
    if (!container) return;
    
    let legendList = container.querySelector("div.custom-legend-list");
    if (!legendList) {
      legendList = document.createElement("div");
      legendList.className = "custom-legend-list flex flex-col justify-center h-full";
      legendList.style.margin = 0;
      legendList.style.padding = 0;
      container.appendChild(legendList);
    }
    
    // Clear existing children
    while (legendList.firstChild) {
      legendList.firstChild.remove();
    }
    
    const legendItems = chart.options.plugins.legend.labels.generateLabels(chart);
    
    legendItems.forEach(item => {
      const legendItemDiv = document.createElement("div");
      legendItemDiv.style.alignItems = "center";
      legendItemDiv.style.cursor = "pointer";
      legendItemDiv.style.display = "flex";
      legendItemDiv.style.flexDirection = "row";
      legendItemDiv.style.marginBottom = "8px";
      legendItemDiv.style.gap = "8px";
      
      legendItemDiv.onclick = () => {
        chart.setDatasetVisibility(item.datasetIndex, !chart.isDatasetVisible(item.datasetIndex));
        chart.update();
      };
      
      const dotSpan = document.createElement("span");
      dotSpan.style.background = item.fillStyle;
      dotSpan.style.borderColor = "#0B0F19";
      dotSpan.style.borderWidth = "1px";
      dotSpan.style.display = "inline-block";
      dotSpan.style.height = "14px";
      dotSpan.style.width = "14px";
      dotSpan.style.borderRadius = "50%";
      dotSpan.style.flexShrink = "0";
      if (item.hidden) {
        dotSpan.style.opacity = "0.5";
      }
      
      const labelSpan = document.createElement("span");
      labelSpan.style.color = "#334155";
      labelSpan.style.margin = 0;
      labelSpan.style.padding = 0;
      labelSpan.style.fontFamily = "'Outfit', sans-serif";
      labelSpan.style.fontSize = "16px";
      labelSpan.style.fontWeight = "500";
      labelSpan.style.textDecoration = item.hidden ? "line-through" : "";
      labelSpan.style.whiteSpace = "normal";
      if (item.hidden) {
        labelSpan.style.opacity = "0.5";
      }
      labelSpan.appendChild(document.createTextNode(item.text));
      
      legendItemDiv.appendChild(dotSpan);
      legendItemDiv.appendChild(labelSpan);
      legendList.appendChild(legendItemDiv);
    });
  }
};

// Global State
let rawPercepcaoData = [];
let rawFdeData = [];
let rawFdepData = [];
let rawVistoriasData = [];

const expandedYearsSet = new Set();
let allPeriodsList = [];
let allYearsList = [];
const yearToPeriodsMap = {};
let allParksList = [];
let allPercepcaoIndicators = [];
let allVistoriasIndicators = [];
let isSyncEnabled = false;

const filterTargets = ["global", "ps", "vis", "des"];
const filterStates = {};

filterTargets.forEach(target => {
  filterStates[target] = {
    timeView: "quarterly",
    selectedPeriods: [],
    selectedYears: [],
    selectedParks: []
  };
});

let selectedPercepcaoIndicators = [];
let selectedVistoriasIndicators = [];
let currentPerformanceIndicator = "IPU";
const parkColorMap = {};

let chartPercepcaoInstance = null;
let chartVistoriasInstance = null;
let chartDesempenhoInstance = null;

// Initialization wrapper
async function initializeStackedDashboard() {
  try {
    const response = await fetch("./data.json");
    const data = await response.json();
    
    rawPercepcaoData = data.percepcao_social || [];
    rawFdeData = data.fde || [];
    rawFdepData = data.fdep || [];
    rawVistoriasData = data.vistorias || [];
    
    processAndInitializeData();
    
    // Set initial filter selection state for each layout group
    filterTargets.forEach(target => {
      filterStates[target].selectedPeriods = [...allPeriodsList];
      filterStates[target].selectedYears = [...allYearsList];
      
      if (allParksList.includes("Média")) {
        filterStates[target].selectedParks = ["Média"];
      } else if (allParksList.includes("Unidade Fictícia 01")) {
        filterStates[target].selectedParks = ["Unidade Fictícia 01"];
      } else if (allParksList.length > 0) {
        filterStates[target].selectedParks = [allParksList[0]];
      } else {
        filterStates[target].selectedParks = [];
      }
    });
    
    renderFilterPanels();
    initializeCharts();
    updateAllCharts();
    
    window.toggleSyncMode = toggleSyncMode;
    window.setTimeView = setTimeView;
    window.toggleDropdown = toggleDropdown;
    window.setDesempenhoInd = setPerformanceIndicator;
    
    document.addEventListener("click", event => {
      if (!event.target.closest(".custom-select")) {
        document.querySelectorAll(".select-options.show").forEach(el => {
          el.classList.remove("show");
        });
      }
    });
  } catch (error) {
    console.error("Error loading data:", error);
  }
}

// Normalize park names and prepositions
function normalizeName(name) {
  if (!name) return name;
  const lowerName = name.toLowerCase().trim();
  if (lowerName.includes("01")) return "Unidade Fictícia 01";
  if (lowerName.includes("02")) return "Unidade Fictícia 02";
  if (lowerName.includes("03")) return "Unidade Fictícia 03";
  if (lowerName.includes("04")) return "Unidade Fictícia 04";
  if (lowerName.includes("05")) return "Unidade Fictícia 05";
  if (lowerName.includes("06")) return "Unidade Fictícia 06";
  return name.trim();
}

// Map dimensions and datasets metadata
function processAndInitializeData() {
  const periodsSet = new Set();
  const parksSet = new Set();
  const percepcaoIndicatorsSet = new Set();
  const vistoriasIndicatorsSet = new Set();
  
  const collectPeriods = (row) => {
    if (row["Ano-periodo"]) {
      const period = row["Ano-periodo"];
      periodsSet.add(period);
      const year = period.substring(0, 4);
      if (!yearToPeriodsMap[year]) {
        yearToPeriodsMap[year] = new Set();
      }
      yearToPeriodsMap[year].add(period);
    }
  };
  
  rawPercepcaoData.forEach(row => {
    collectPeriods(row);
    if ((row.Unidade || row.Parque)) {
      const normalizedPark = normalizeName((row.Unidade || row.Parque));
      row.Unidade = normalizedPark; row.Parque = normalizedPark;
      parksSet.add(normalizedPark);
    }
    Object.keys(row).forEach(key => {
      if (key !== "Parque" && key !== "Unidade" && key !== "Ano-periodo") {
        percepcaoIndicatorsSet.add(key);
      }
    });
  });
  
  rawVistoriasData.forEach(row => {
    collectPeriods(row);
    if ((row.Unidade || row.Parque)) {
      const normalizedPark = normalizeName((row.Unidade || row.Parque));
      row.Unidade = normalizedPark; row.Parque = normalizedPark;
      parksSet.add(normalizedPark);
    }
    Object.keys(row).forEach(key => {
      if (key !== "Parque" && key !== "Unidade" && key !== "Ano-periodo") {
        vistoriasIndicatorsSet.add(key);
      }
    });
  });
  
  rawFdepData.forEach(row => {
    collectPeriods(row);
    if ((row.Unidade || row.Parque)) {
      const normalizedPark = normalizeName((row.Unidade || row.Parque));
      row.Unidade = normalizedPark; row.Parque = normalizedPark;
      parksSet.add(normalizedPark);
    }
  });
  
  rawFdeData.forEach(row => {
    collectPeriods(row);
  });
  
  allPeriodsList = Array.from(periodsSet).sort();
  allYearsList = Object.keys(yearToPeriodsMap).sort();
  allParksList = Array.from(parksSet).sort();
  allParksList.unshift("Média");
  
  const colorsList = ["#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#14b8a6", "#f97316", "#3b82f6"];
  let colorIndex = 0;
  allParksList.forEach(park => {
    if (park === "Média") {
      parkColorMap[park] = "#FF8200";
    } else if (park === "Unidade Fictícia 01") {
      parkColorMap[park] = "#0ea5e9";
    } else {
      parkColorMap[park] = colorsList[colorIndex % colorsList.length];
      colorIndex++;
    }
  });
  
  allPercepcaoIndicators = Array.from(percepcaoIndicatorsSet).sort();
  allVistoriasIndicators = Array.from(vistoriasIndicatorsSet).sort();
  
  if (allPercepcaoIndicators.includes("IND-A01 – Confiabilidade Estrutural")) {
    selectedPercepcaoIndicators = ["IND-A01 – Confiabilidade Estrutural"];
  } else if (allPercepcaoIndicators.length > 0) {
    selectedPercepcaoIndicators = [allPercepcaoIndicators[0]];
  }
  
  if (allVistoriasIndicators.includes("IAT – Índice de Auditoria Técnica")) {
    selectedVistoriasIndicators = ["IAT – Índice de Auditoria Técnica"];
  } else if (allVistoriasIndicators.length > 0) {
    selectedVistoriasIndicators = [allVistoriasIndicators[0]];
  }
}

// Toggle filters synchronization
function toggleSyncMode(syncEnabled) {
  isSyncEnabled = syncEnabled;
  const globalFilters = document.getElementById("global-filters");
  const individualFilters = document.querySelectorAll(".indiv-sync-hide");
  
  if (isSyncEnabled) {
    globalFilters.classList.remove("hidden", "hidden-state");
    individualFilters.forEach(el => {
      el.classList.add("hidden-state");
      setTimeout(() => el.classList.add("hidden"), 300);
    });
    
    const globalState = filterStates.global;
    ["ps", "vis", "des"].forEach(target => {
      filterStates[target].timeView = globalState.timeView;
      filterStates[target].selectedPeriods = [...globalState.selectedPeriods];
      filterStates[target].selectedYears = [...globalState.selectedYears];
      filterStates[target].selectedParks = [...globalState.selectedParks];
    });
  } else {
    globalFilters.classList.add("hidden", "hidden-state");
    individualFilters.forEach(el => {
      el.classList.remove("hidden");
      setTimeout(() => el.classList.remove("hidden-state"), 10);
    });
  }
  
  renderFilterPanels();
  updateAllCharts();
}

// Change time grouping scale
function setTimeView(view, target) {
  filterStates[target].timeView = view;
  renderFilterPanels();
  if (target === "global" && isSyncEnabled) {
    updateAllCharts();
  } else {
    updateChart(target);
  }
}

// Dropdown expansion helper
function toggleDropdown(dropdownId) {
  const parts = dropdownId.split("-");
  const prefix = parts.length > 1 ? parts[0] + "-" : "";
  const suffix = parts.pop();
  
  const optionsDiv = document.getElementById(`${prefix}options-${suffix}`);
  if (optionsDiv) {
    optionsDiv.classList.toggle("show");
  }
}

// Update performance index choice
function setPerformanceIndicator(indicator) {
  currentPerformanceIndicator = indicator;
  renderFilterPanels();
  updateChart("des");
}

// Add/Remove selection items
function handleFilterToggle(item, selectedList, target) {
  const index = selectedList.indexOf(item);
  if (index > -1) {
    if (selectedList.length > 1) {
      selectedList.splice(index, 1);
    }
  } else {
    selectedList.push(item);
  }
  
  renderFilterPanels();
  if (target === "global" && isSyncEnabled) {
    updateAllCharts();
  } else {
    updateChart(target);
  }
}

// Update labels showing how many items are checked
function updateHeaderSelectText(elementId, selectedList, allList) {
  const element = document.getElementById(elementId);
  if (element) {
    if (selectedList.length === allList.length) {
      element.textContent = "Todos selecionados";
    } else if (selectedList.length === 1) {
      let label = selectedList[0];
      if (label.length > 25) {
        label = label.substring(0, 25) + "...";
      }
      element.textContent = label;
    } else {
      element.textContent = `${selectedList.length} selecionados`;
    }
  }
}

// Construct and render dynamic panels markup
function renderFilterPanels() {
  const renderCheckboxDropdown = (allList, selectedList, containerElement, selectId, targetKey) => {
    if (!containerElement) return;
    containerElement.innerHTML = "";
    
    const headerDiv = document.createElement("div");
    headerDiv.style.display = "flex";
    headerDiv.style.justifyContent = "flex-start";
    headerDiv.style.gap = "16px";
    headerDiv.style.padding = "10px 16px";
    headerDiv.style.borderBottom = "1px solid #e2e8f0";
    
    const selectAllBtn = document.createElement("button");
    selectAllBtn.textContent = "SELECIONAR TODOS";
    selectAllBtn.className = "text-[10px] font-bold text-brand uppercase tracking-wider hover:underline transition-all";
    selectAllBtn.onclick = (e) => {
      e.stopPropagation();
      selectedList.length = 0;
      allList.forEach(item => selectedList.push(item));
      renderFilterPanels();
      if (targetKey === "global" && isSyncEnabled) {
        updateAllCharts();
      } else {
        updateChart(targetKey);
      }
    };
    
    const clearBtn = document.createElement("button");
    clearBtn.textContent = "LIMPAR";
    clearBtn.className = "text-[10px] font-bold text-slate-400 hover:text-slate-600 uppercase tracking-wider hover:underline transition-all";
    clearBtn.onclick = (e) => {
      e.stopPropagation();
      if (allList.length > 0) {
        selectedList.length = 0;
        selectedList.push(allList[0]);
        renderFilterPanels();
        if (targetKey === "global" && isSyncEnabled) {
          updateAllCharts();
        } else {
          updateChart(targetKey);
        }
      }
    };
    
    headerDiv.appendChild(selectAllBtn);
    headerDiv.appendChild(clearBtn);
    containerElement.appendChild(headerDiv);
    
    allList.forEach(item => {
      const optionLabel = document.createElement("label");
      optionLabel.className = "select-option";
      
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.checked = selectedList.includes(item);
      
      const labelSpan = document.createElement("span");
      labelSpan.textContent = item;
      
      optionLabel.appendChild(checkbox);
      optionLabel.appendChild(labelSpan);
      
      checkbox.addEventListener("change", () => {
        handleFilterToggle(item, selectedList, targetKey);
      });
      
      containerElement.appendChild(optionLabel);
    });
  };
  
  filterTargets.forEach(targetKey => {
    const state = filterStates[targetKey];
    const prefix = targetKey === "global" ? "g" : targetKey;
    
    const quarterlyBtn = document.getElementById(`${prefix}-btn-quarterly`);
    const annualBtn = document.getElementById(`${prefix}-btn-annual`);
    
    if (quarterlyBtn && annualBtn) {
      quarterlyBtn.classList.toggle("active", state.timeView === "quarterly");
      annualBtn.classList.toggle("active", state.timeView === "annual");
    }
    
    const periodOptionsContainer = document.getElementById(`${prefix}-options-period`);
    if (periodOptionsContainer) {
      periodOptionsContainer.innerHTML = "";
      
      const buttonsDiv = document.createElement("div");
      buttonsDiv.style.display = "flex";
      buttonsDiv.style.width = "100%";
      buttonsDiv.style.justifyContent = "flex-end";
      buttonsDiv.style.gap = "12px";
      buttonsDiv.style.paddingBottom = "4px";
      buttonsDiv.style.marginTop = "-4px";
      
      const selectAllBtn = document.createElement("button");
      selectAllBtn.textContent = "Selecionar Todos";
      selectAllBtn.className = "text-[10px] font-bold text-brand uppercase tracking-wider hover:underline transition-all";
      selectAllBtn.onclick = () => {
        if (state.timeView === "quarterly") {
          state.selectedPeriods = [...allPeriodsList];
        } else {
          state.selectedYears = [...allYearsList];
        }
        renderFilterPanels();
        if (targetKey === "global" && isSyncEnabled) {
          updateAllCharts();
        } else {
          updateChart(targetKey);
        }
      };
      
      const clearBtn = document.createElement("button");
      clearBtn.textContent = "Limpar";
      clearBtn.className = "text-[10px] font-bold text-slate-400 hover:text-slate-600 uppercase tracking-wider hover:underline transition-all";
      clearBtn.onclick = () => {
        if (state.timeView === "quarterly") {
          if (allPeriodsList.length > 0) {
            state.selectedPeriods = [allPeriodsList[0]];
          }
        } else {
          if (allYearsList.length > 0) {
            state.selectedYears = [allYearsList[0]];
          }
        }
        renderFilterPanels();
        if (targetKey === "global" && isSyncEnabled) {
          updateAllCharts();
        } else {
          updateChart(targetKey);
        }
      };
      
      buttonsDiv.appendChild(selectAllBtn);
      buttonsDiv.appendChild(clearBtn);
      periodOptionsContainer.appendChild(buttonsDiv);
      
      if (state.timeView === "annual") {
        const chipsRow = document.createElement("div");
        chipsRow.className = "chips-row mt-2";
        
        allYearsList.forEach(year => {
          const chip = document.createElement("div");
          chip.className = `chip ${state.selectedYears.includes(year) ? "active" : "cursor-pointer"}`;
          chip.textContent = year;
          chip.onclick = () => handleFilterToggle(year, state.selectedYears, targetKey);
          chipsRow.appendChild(chip);
        });
        
        periodOptionsContainer.appendChild(chipsRow);
      } else {
        allYearsList.forEach(year => {
          const accordionGroup = document.createElement("div");
          accordionGroup.className = "accordion-group mt-2";
          
          const accordionHeader = document.createElement("div");
          accordionHeader.className = "accordion-header text-brand cursor-pointer flex justify-between items-center px-1 hover:bg-slate-50 rounded transition-colors";
          
          const isExpanded = expandedYearsSet.has(year);
          accordionHeader.innerHTML = `<span>${year}</span><span class="text-sm text-brand/60 transition-transform transform ${isExpanded ? "rotate-180" : ""}">▼</span>`;
          accordionGroup.appendChild(accordionHeader);
          
          const accordionContent = document.createElement("div");
          accordionContent.className = `accordion-content ${isExpanded ? "expanded" : ""}`;
          
          const accordionInner = document.createElement("div");
          accordionInner.className = "accordion-inner pt-1";
          
          const chipsRow = document.createElement("div");
          chipsRow.className = "chips-row";
          
          accordionInner.appendChild(chipsRow);
          accordionContent.appendChild(accordionInner);
          
          accordionHeader.onclick = () => {
            if (expandedYearsSet.has(year)) {
              expandedYearsSet.delete(year);
              accordionContent.classList.remove("expanded");
              accordionHeader.querySelector("span:last-child").classList.remove("rotate-180");
            } else {
              expandedYearsSet.add(year);
              accordionContent.classList.add("expanded");
              accordionHeader.querySelector("span:last-child").classList.add("rotate-180");
            }
          };
          
          const yearPeriods = Array.from(yearToPeriodsMap[year] || []).sort();
          yearPeriods.forEach(period => {
            const chip = document.createElement("div");
            chip.className = `chip ${state.selectedPeriods.includes(period) ? "active" : "cursor-pointer"}`;
            
            const periodParts = period.split(" - ");
            chip.textContent = periodParts.length > 1 ? periodParts[1] : period;
            chip.onclick = (e) => {
              e.stopPropagation();
              handleFilterToggle(period, state.selectedPeriods, targetKey);
            };
            chipsRow.appendChild(chip);
          });
          
          accordionGroup.appendChild(accordionContent);
          periodOptionsContainer.appendChild(accordionGroup);
        });
      }
    }
    
    const activePeriodList = state.timeView === "quarterly" ? allPeriodsList : allYearsList;
    updateHeaderSelectText(`${prefix}-period`, state.timeView === "quarterly" ? state.selectedPeriods : state.selectedYears, activePeriodList);
    
    const parksOptionsContainer = document.getElementById(`${prefix}-options-parks`);
    renderCheckboxDropdown(allParksList, state.selectedParks, parksOptionsContainer, `${prefix}-parks`, targetKey);
    updateHeaderSelectText(`${prefix}-parks-header-text`, state.selectedParks, allParksList);
  });
  
  const desBtnIpu = document.getElementById("des-btn-ipu");
  const desBtnIpc = document.getElementById("des-btn-ipc");
  if (desBtnIpu && desBtnIpc) {
    desBtnIpu.classList.toggle("active", currentPerformanceIndicator === "IPU");
    desBtnIpc.classList.toggle("active", currentPerformanceIndicator === "IPC");
  }
  
  const desGroupParks = document.getElementById("des-group-parks");
  if (desGroupParks) {
    desGroupParks.style.display = currentPerformanceIndicator === "IPC" ? "none" : "block";
  }
  
  renderCheckboxDropdown(allPercepcaoIndicators, selectedPercepcaoIndicators, document.getElementById("ps-options-indicators"), "ps-indicators", "ps");
  updateHeaderSelectText("ps-indicators-header-text", selectedPercepcaoIndicators, allPercepcaoIndicators);
  
  renderCheckboxDropdown(allVistoriasIndicators, selectedVistoriasIndicators, document.getElementById("vis-options-indicators"), "vis-indicators", "vis");
  updateHeaderSelectText("vis-indicators-header-text", selectedVistoriasIndicators, allVistoriasIndicators);
}

// Get active filter state block
function getFilterState(target) {
  return isSyncEnabled ? filterStates.global : filterStates[target];
}

const strokeColors = ["#FF8200", "#2563eb", "#16a34a", "#dc2626", "#9333ea", "#ea580c", "#0d9488"];

// Initialize standard chart layouts
function initializeCharts() {
  const commonChartOptions = {
    type: "line",
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: "index",
        intersect: false
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          titleFont: { size: 16 },
          bodyFont: { size: 16 }
        }
      },
      layout: {
        padding: {
          top: 15,
          right: 10
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: {
            maxRotation: 0,
            autoSkip: true,
            autoSkipPadding: 15,
            font: { size: 14 },
            callback: function(val, index) {
              const label = this.getLabelForValue(val);
              if (label && label.includes(" - ")) {
                const parts = label.split(" - ");
                const shortYear = parts[0].slice(2);
                return parts[1].replace("Tri", "T") + " '" + shortYear;
              }
              return label;
            }
          }
        },
        y: {
          min: 0.5,
          max: 1,
          ticks: {
            font: { size: 14 }
          }
        }
      }
    }
  };
  
  const psCtx = document.getElementById("chart-ps").getContext("2d");
  let psConfig = JSON.parse(JSON.stringify(commonChartOptions));
  psConfig.plugins = [htmlLegendPlugin];
  psConfig.options.plugins.htmlLegend = { containerID: "html-legend-ps" };
  chartPercepcaoInstance = new Chart(psCtx, psConfig);
  
  const visCtx = document.getElementById("chart-vistoria").getContext("2d");
  let visConfig = JSON.parse(JSON.stringify(commonChartOptions));
  visConfig.plugins = [htmlLegendPlugin];
  visConfig.options.plugins.htmlLegend = { containerID: "html-legend-vis" };
  chartVistoriasInstance = new Chart(visCtx, visConfig);
  
  const desCtx = document.getElementById("chart-desempenho").getContext("2d");
  let desConfig = JSON.parse(JSON.stringify(commonChartOptions));
  desConfig.plugins = [htmlLegendPlugin];
  desConfig.options.plugins.htmlLegend = { containerID: "html-legend-des" };
  chartDesempenhoInstance = new Chart(desCtx, desConfig);
  
  window.chartPS = chartPercepcaoInstance;
  window.chartVis = chartVistoriasInstance;
  window.chartDes = chartDesempenhoInstance;
}

// Dispatches updates to the three stacked canvases
function updateAllCharts() {
  updateChart("ps");
  updateChart("vis");
  updateChart("des");
}

window.handleScaleChange = function(target) {
  if (isSyncEnabled) {
    updateAllCharts();
  } else {
    updateChart(target);
  }
};

window.resetScale = function(target) {
  const prefix = target === "global" ? "g" : target;
  const minInput = document.getElementById(`${prefix}-y-min`);
  const maxInput = document.getElementById(`${prefix}-y-max`);
  
  if (minInput) minInput.value = 0.5;
  if (maxInput) maxInput.value = 1;
  
  window.handleScaleChange(target);
};

// Calculate metrics and update target canvas
function updateChart(chartId) {
  const state = getFilterState(chartId);
  
  let rawDataset = [];
  let selectedIndicators = [];
  let chartInstance = null;
  
  if (chartId === "ps") {
    rawDataset = rawPercepcaoData;
    selectedIndicators = selectedPercepcaoIndicators;
    chartInstance = chartPercepcaoInstance;
  } else if (chartId === "vis") {
    rawDataset = rawVistoriasData;
    selectedIndicators = selectedVistoriasIndicators;
    chartInstance = chartVistoriasInstance;
  } else if (chartId === "des") {
    rawDataset = currentPerformanceIndicator === "IPU" ? rawFdepData : rawFdeData;
    selectedIndicators = [currentPerformanceIndicator];
    chartInstance = chartDesempenhoInstance;
  }
  
  if (!chartInstance) return;
  
  let periods = [];
  if (state.timeView === "quarterly") {
    periods = [...state.selectedPeriods].sort();
  } else {
    periods = [...state.selectedYears].sort();
  }
  
  const datasets = [];
  
  if (selectedIndicators.length === 1 && selectedIndicators[0] !== "IPC") {
    const indicator = selectedIndicators[0];
    state.selectedParks.forEach((park, idx) => {
      const dataValues = periods.map(period => {
        if (state.timeView === "quarterly") {
          if (park === "Média") {
            const matchingRows = rawDataset.filter(r => r["Ano-periodo"] === period);
            const vals = matchingRows.map(r => parseFloat(r[indicator])).filter(v => !isNaN(v));
            return vals.length === 0 ? null : vals.reduce((a, b) => a + b, 0) / vals.length;
          } else {
            const foundRow = rawDataset.find(r => (r.Unidade || r.Parque) === park && r["Ano-periodo"] === period);
            if (foundRow) {
              const val = parseFloat(foundRow[indicator]);
              return isNaN(val) ? null : val;
            }
            return null;
          }
        } else {
          let matchingRows = [];
          if (park === "Média") {
            matchingRows = rawDataset.filter(r => String(r["Ano-periodo"]).startsWith(period));
          } else {
            matchingRows = rawDataset.filter(r => (r.Unidade || r.Parque) === park && String(r["Ano-periodo"]).startsWith(period));
          }
          const vals = matchingRows.map(r => parseFloat(r[indicator])).filter(v => !isNaN(v));
          return vals.length === 0 ? null : vals.reduce((a, b) => a + b, 0) / vals.length;
        }
      });
      
      if (dataValues.some(v => v !== null)) {
        const color = parkColorMap[park] || strokeColors[idx % strokeColors.length];
        datasets.push({
          label: `   ${park} (${indicator})`,
          data: dataValues,
          borderColor: color,
          backgroundColor: color,
          borderWidth: 3,
          pointBackgroundColor: color,
          pointBorderColor: "#0B0F19",
          pointBorderWidth: 1,
          pointRadius: 3,
          pointHoverRadius: 6,
          tension: 0.3,
          clip: false
        });
      }
    });
  } else if (selectedIndicators.length > 1) {
    selectedIndicators.forEach((indicator, idx) => {
      const dataValues = periods.map(period => {
        if (state.timeView === "quarterly") {
          const matchingRows = rawDataset.filter(r => (state.selectedParks.includes("Média") || state.selectedParks.includes((r.Unidade || r.Parque))) && r["Ano-periodo"] === period);
          const vals = matchingRows.map(r => parseFloat(r[indicator])).filter(v => !isNaN(v));
          return vals.length === 0 ? null : vals.reduce((a, b) => a + b, 0) / vals.length;
        } else {
          const matchingRows = rawDataset.filter(r => (state.selectedParks.includes("Média") || state.selectedParks.includes((r.Unidade || r.Parque))) && String(r["Ano-periodo"]).startsWith(period));
          const vals = matchingRows.map(r => parseFloat(r[indicator])).filter(v => !isNaN(v));
          return vals.length === 0 ? null : vals.reduce((a, b) => a + b, 0) / vals.length;
        }
      });
      
      if (dataValues.some(v => v !== null)) {
        const label = state.selectedParks.length === 1 ? `   ${state.selectedParks[0]} (${indicator})` : `   Média ${indicator}`;
        datasets.push({
          label: label,
          data: dataValues,
          borderColor: strokeColors[idx % strokeColors.length],
          backgroundColor: strokeColors[idx % strokeColors.length],
          borderWidth: 3,
          pointBackgroundColor: strokeColors[idx % strokeColors.length],
          pointBorderColor: "#0B0F19",
          pointBorderWidth: 1,
          pointRadius: 3,
          pointHoverRadius: 6,
          tension: 0.3,
          clip: false
        });
      }
    });
  } else if (currentPerformanceIndicator === "IPC") {
    const dataValues = periods.map(period => {
      if (state.timeView === "quarterly") {
        const foundRow = rawDataset.find(r => r["Ano-periodo"] === period);
        if (foundRow) {
          const val = parseFloat(foundRow.IPC || foundRow.FDE);
          return isNaN(val) ? null : val;
        }
        return null;
      } else {
        const matchingRows = rawDataset.filter(r => String(r["Ano-periodo"]).startsWith(period));
        const vals = matchingRows.map(r => parseFloat(r.IPC || r.FDE)).filter(v => !isNaN(v));
        return vals.length === 0 ? null : vals.reduce((a, b) => a + b, 0) / vals.length;
      }
    });
    
    datasets.push({
      label: "   FDE Geral",
      data: dataValues,
      borderColor: strokeColors[0],
      backgroundColor: strokeColors[0],
      borderWidth: 3,
      pointBackgroundColor: strokeColors[0],
      pointBorderColor: "#0B0F19",
      pointBorderWidth: 1,
      pointRadius: 3,
      pointHoverRadius: 6,
      tension: 0.3,
      clip: false
    });
  }
  
  const prefix = isSyncEnabled ? "g" : chartId;
  const minInput = document.getElementById(`${prefix}-y-min`);
  const maxInput = document.getElementById(`${prefix}-y-max`);
  
  if (minInput && maxInput) {
    const minVal = parseFloat(minInput.value);
    const maxVal = parseFloat(maxInput.value);
    
    if (!isNaN(minVal)) {
      chartInstance.options.scales.y.min = minVal;
    }
    if (!isNaN(maxVal)) {
      chartInstance.options.scales.y.max = maxVal;
    }
  }
  
  chartInstance.data.labels = periods;
  chartInstance.data.datasets = datasets;
  chartInstance.update();
}

// Bootstrap application on DOMContentLoaded
window.addEventListener("DOMContentLoaded", initializeStackedDashboard);

// Glossary Modal listeners
const glossaryBtn = document.getElementById("glossary-btn");
const glossaryModal = document.getElementById("glossary-modal");
const closeGlossary = document.getElementById("close-glossary");
const confirmGlossary = document.getElementById("confirm-glossary");

if (glossaryBtn && glossaryModal && closeGlossary) {
  glossaryBtn.addEventListener("click", () => {
    glossaryModal.classList.add("show");
  });
  if (confirmGlossary) {
    confirmGlossary.addEventListener("click", () => {
      glossaryModal.classList.remove("show");
    });
  }
  closeGlossary.addEventListener("click", () => {
    glossaryModal.classList.remove("show");
  });
  glossaryModal.addEventListener("click", event => {
    if (event.target === glossaryModal) {
      glossaryModal.classList.remove("show");
    }
  });
}
