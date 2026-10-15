// Custom HTML Legend Plugin for Chart.js
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
      
      const borderDash = chart.data.datasets[item.datasetIndex].borderDash || [];
      const strokeStyle = item.strokeStyle || item.fillStyle;
      
      const boxSpan = document.createElement("span");
      boxSpan.style.display = "inline-block";
      boxSpan.style.width = "24px";
      boxSpan.style.height = "14px";
      boxSpan.style.flexShrink = "0";
      boxSpan.style.position = "relative";
      
      const svgNamespace = "http://www.w3.org/2000/svg";
      const svg = document.createElementNS(svgNamespace, "svg");
      svg.setAttribute("width", "24");
      svg.setAttribute("height", "14");
      svg.style.position = "absolute";
      svg.style.top = "0";
      svg.style.left = "0";
      
      const line = document.createElementNS(svgNamespace, "line");
      line.setAttribute("x1", "0");
      line.setAttribute("y1", "7");
      line.setAttribute("x2", "24");
      line.setAttribute("y2", "7");
      line.setAttribute("stroke", strokeStyle);
      line.setAttribute("stroke-width", "3");
      if (borderDash.length > 0) {
        line.setAttribute("stroke-dasharray", borderDash.join(","));
      }
      
      const circle = document.createElementNS(svgNamespace, "circle");
      circle.setAttribute("cx", "12");
      circle.setAttribute("cy", "7");
      circle.setAttribute("r", "4");
      circle.setAttribute("fill", strokeStyle);
      circle.setAttribute("stroke", "#0B0F19");
      circle.setAttribute("stroke-width", "1");
      
      svg.appendChild(line);
      svg.appendChild(circle);
      boxSpan.appendChild(svg);
      
      if (item.hidden) {
        boxSpan.style.opacity = "0.5";
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
      
      legendItemDiv.appendChild(boxSpan);
      legendItemDiv.appendChild(labelSpan);
      legendList.appendChild(legendItemDiv);
    });
  }
};

// Global State
let currentDashboardMode = "percepcao";
let currentPerformanceIndicator = "IPU";
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
let currentTimeView = "quarterly";

let selectedPeriodsList = [];
let selectedYearsList = [];
let selectedParksList = [];
let selectedPercepcaoIndicators = [];
let selectedVistoriasIndicators = [];
let allLivreIndicators = [];
let selectedLivreIndicators = [];
const parkColorMap = {};
let myChartInstance = null;

// DOM Selectors
const optionsParksElement = document.getElementById("options-parks");
const optionsPercepcaoIndicatorsElement = document.getElementById("options-indicators");
const optionsVistoriasIndicatorsElement = document.getElementById("options-indicators-vistoria");
const optionsLivreIndicatorsElement = document.getElementById("options-indicators-livre");
const exportButton = document.getElementById("export-btn");

// Initialization function
async function loadData() {
  try {
    const response = await fetch("./data.json");
    const data = await response.json();
    
    rawPercepcaoData = data.percepcao_social || [];
    rawFdeData = data.fde || [];
    rawFdepData = data.fdep || [];
    rawVistoriasData = data.vistorias || [];
    
    processAndInitializeData();
    renderFilterDropdowns();
    initializeChart();
    setTimeView("quarterly");
    updateChartData();
  } catch (error) {
    console.error("Error loading data:", error);
    alert("Erro ao carregar dados. Se estiver abrindo o arquivo HTML diretamente (file://), o navegador pode bloquear o fetch(). Tente rodar um servidor local, por exemplo: python -m http.server");
  }
}

// Normalize park names and key strings
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

// Process raw arrays and compile keys/dimensions
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
        const normalizedKey = normalizeName(key);
        percepcaoIndicatorsSet.add(normalizedKey);
        if (key !== normalizedKey) {
          row[normalizedKey] = row[key];
          delete row[key];
        }
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
        const normalizedKey = normalizeName(key);
        vistoriasIndicatorsSet.add(normalizedKey);
        if (key !== normalizedKey) {
          row[normalizedKey] = row[key];
          delete row[key];
        }
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
  allPercepcaoIndicators = Array.from(percepcaoIndicatorsSet).sort();
  allVistoriasIndicators = Array.from(vistoriasIndicatorsSet).sort();
  
  allLivreIndicators = [
    ...allPercepcaoIndicators.map(ind => `[PS] ${ind}`),
    ...allVistoriasIndicators.map(ind => `[Vistoria] ${ind}`),
    "[Desempenho] IPU",
    "[Desempenho] IPC"
  ];
  
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
  
  selectedPeriodsList = [...allPeriodsList];
  selectedYearsList = [...allYearsList];
  
  if (allParksList.includes("Média")) {
    selectedParksList = ["Média"];
  } else if (allParksList.length > 0) {
    selectedParksList = [allParksList[0]];
  }
  
  if (allPercepcaoIndicators.includes("IQX – Índice de Qualidade da Experiência")) {
    selectedPercepcaoIndicators = ["IQX – Índice de Qualidade da Experiência"];
  } else if (allPercepcaoIndicators.length > 0) {
    selectedPercepcaoIndicators = [allPercepcaoIndicators[0]];
  }
  
  if (allVistoriasIndicators.includes("IAT – Índice de Auditoria Técnica")) {
    selectedVistoriasIndicators = ["IAT – Índice de Auditoria Técnica"];
  } else if (allVistoriasIndicators.length > 0) {
    selectedVistoriasIndicators = [allVistoriasIndicators[0]];
  }
  
  selectedLivreIndicators = ["[Experiência] IQX", "[Auditoria] IAT"];
}

// Window Exposed Functions for dropdown and configuration triggers
window.toggleDropdown = function(dropdownId) {
  const optionsDiv = document.getElementById(`options-${dropdownId}`);
  if (optionsDiv) {
    if (optionsDiv.classList.contains("show")) {
      optionsDiv.classList.remove("show");
    } else {
      document.querySelectorAll(".select-options").forEach(el => el.classList.remove("show"));
      optionsDiv.classList.add("show");
    }
  }
};

document.addEventListener("click", event => {
  if (!event.target.closest(".custom-select")) {
    document.querySelectorAll(".select-options").forEach(el => el.classList.remove("show"));
  }
});

window.setDashboardMode = function(mode) {
  currentDashboardMode = mode;
  
  document.getElementById("btn-mode-percepcao").classList.toggle("active", mode === "percepcao");
  document.getElementById("btn-mode-vistorias").classList.toggle("active", mode === "vistorias");
  document.getElementById("btn-mode-desempenho").classList.toggle("active", mode === "desempenho");
  document.getElementById("btn-mode-livre").classList.toggle("active", mode === "livre");
  
  document.getElementById("indicators-percepcao").style.display = mode === "percepcao" ? "block" : "none";
  document.getElementById("indicators-vistorias").style.display = mode === "vistorias" ? "block" : "none";
  document.getElementById("indicators-desempenho").style.display = mode === "desempenho" ? "block" : "none";
  document.getElementById("indicators-livre").style.display = mode === "livre" ? "block" : "none";
  
  if (mode === "desempenho") {
    document.getElementById("group-parks").style.display = currentPerformanceIndicator === "IPU" ? "block" : "none";
  } else {
    document.getElementById("group-parks").style.display = "block";
  }
  
  if (typeof window.renderKPIs === "function") {
    window.renderKPIs(mode);
  }
  updateChartData();
};

window.setDesempenhoInd = function(indicator) {
  currentPerformanceIndicator = indicator;
  
  document.getElementById("btn-ind-ipu").classList.toggle("active", indicator === "IPU");
  document.getElementById("btn-ind-ipc").classList.toggle("active", indicator === "IPC");
  
  if (indicator === "IPC") {
    document.getElementById("group-parks").style.display = "none";
    document.getElementById("fde-info").style.display = "block";
  } else {
    document.getElementById("group-parks").style.display = "block";
    document.getElementById("fde-info").style.display = "none";
  }
  updateChartData();
};

window.setTimeView = function(view) {
  currentTimeView = view;
  
  document.getElementById("btn-quarterly").classList.toggle("active", view === "quarterly");
  document.getElementById("btn-annual").classList.toggle("active", view === "annual");
  document.getElementById("annual-info").style.display = view === "annual" ? "block" : "none";
  
  renderFilterDropdowns();
  updateChartData();
};

// Update labels on dropdown headers
function updateHeaderSelectText(prefix, selectedList, allList) {
  const headerElement = document.getElementById(`${prefix}-header-text`);
  if (headerElement) {
    if (selectedList.length === allList.length) {
      headerElement.textContent = "Todos selecionados";
    } else if (selectedList.length === 1) {
      let label = selectedList[0];
      if (label.length > 25) {
        label = label.substring(0, 25) + "...";
      }
      headerElement.textContent = label;
    } else {
      headerElement.textContent = `${selectedList.length} selecionados`;
    }
  }
}

// Construct and render period specific markup (chips/accordions)
function renderPeriodDropdown() {
  const periodDropdown = document.getElementById("options-period");
  if (!periodDropdown) return;
  periodDropdown.innerHTML = "";
  
  const buttonsContainer = document.createElement("div");
  buttonsContainer.style.display = "flex";
  buttonsContainer.style.width = "100%";
  buttonsContainer.style.justifyContent = "flex-start";
  buttonsContainer.style.gap = "16px";
  buttonsContainer.style.paddingBottom = "8px";
  buttonsContainer.style.marginTop = "-4px";
  
  const selectAllBtn = document.createElement("button");
  selectAllBtn.textContent = "SELECIONAR TODOS";
  selectAllBtn.className = "text-[10px] font-bold text-brand uppercase tracking-wider hover:underline transition-all";
  selectAllBtn.onclick = (e) => {
    e.stopPropagation();
    if (currentTimeView === "quarterly") {
      selectedPeriodsList = [...allPeriodsList];
    } else {
      selectedYearsList = [...allYearsList];
    }
    renderPeriodDropdown();
    updateChartData();
  };
  
  const clearBtn = document.createElement("button");
  clearBtn.textContent = "LIMPAR";
  clearBtn.className = "text-[10px] font-bold text-slate-400 hover:text-slate-600 uppercase tracking-wider hover:underline transition-all";
  clearBtn.onclick = (e) => {
    e.stopPropagation();
    if (currentTimeView === "quarterly") {
      if (allPeriodsList.length > 0) {
        selectedPeriodsList = [allPeriodsList[0]];
      }
    } else {
      if (allYearsList.length > 0) {
        selectedYearsList = [allYearsList[0]];
      }
    }
    renderPeriodDropdown();
    updateChartData();
  };
  
  buttonsContainer.appendChild(selectAllBtn);
  buttonsContainer.appendChild(clearBtn);
  periodDropdown.appendChild(buttonsContainer);
  
  if (currentTimeView === "annual") {
    const chipsRow = document.createElement("div");
    chipsRow.className = "chips-row";
    allYearsList.forEach(year => {
      const chip = document.createElement("div");
      chip.className = `chip ${selectedYearsList.includes(year) ? "active" : ""}`;
      chip.textContent = year;
      chip.onclick = (e) => {
        e.stopPropagation();
        handleFilterSelection(year, selectedYearsList, chip, "period", allYearsList);
        renderPeriodDropdown();
      };
      chipsRow.appendChild(chip);
    });
    periodDropdown.appendChild(chipsRow);
  } else {
    allYearsList.forEach(year => {
      const accordionGroup = document.createElement("div");
      accordionGroup.className = "accordion-group";
      
      const accordionHeader = document.createElement("div");
      accordionHeader.className = "accordion-header cursor-pointer flex justify-between items-center px-1 hover:bg-slate-50 rounded transition-colors";
      const isExpanded = expandedYearsSet.has(year);
      
      accordionHeader.innerHTML = `<span>${year}</span><span class="text-xs text-slate-400 transition-transform transform ${isExpanded ? "rotate-180" : ""}">▼</span>`;
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
      
      const periodCollection = Array.from(yearToPeriodsMap[year] || []).sort();
      periodCollection.forEach(period => {
        const chip = document.createElement("div");
        chip.className = `chip ${selectedPeriodsList.includes(period) ? "active" : ""}`;
        
        const periodParts = period.split(" - ");
        chip.textContent = periodParts.length > 1 ? periodParts[1] : period;
        chip.onclick = (e) => {
          e.stopPropagation();
          handleFilterSelection(period, selectedPeriodsList, chip, "period", allPeriodsList);
          renderPeriodDropdown();
        };
        chipsRow.appendChild(chip);
      });
      
      accordionGroup.appendChild(accordionContent);
      periodDropdown.appendChild(accordionGroup);
    });
  }
  
  updateHeaderSelectText("period", currentTimeView === "quarterly" ? selectedPeriodsList : selectedYearsList, currentTimeView === "quarterly" ? allPeriodsList : allYearsList);
}

// Render dynamic filter dropdowns options
function renderFilterDropdowns() {
  const populateCheckboxDropdown = (allList, selectedList, containerElement, typeKey) => {
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
      renderFilterDropdowns();
      updateChartData();
    };
    
    const clearBtn = document.createElement("button");
    clearBtn.textContent = "LIMPAR";
    clearBtn.className = "text-[10px] font-bold text-slate-400 hover:text-slate-600 uppercase tracking-wider hover:underline transition-all";
    clearBtn.onclick = (e) => {
      e.stopPropagation();
      if (allList.length > 0) {
        selectedList.length = 0;
        selectedList.push(allList[0]);
        renderFilterDropdowns();
        updateChartData();
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
        handleFilterSelection(item, selectedList, checkbox, typeKey, allList);
      });
      
      containerElement.appendChild(optionLabel);
    });
    
    updateHeaderSelectText(typeKey, selectedList, allList);
  };
  
  renderPeriodDropdown();
  populateCheckboxDropdown(allParksList, selectedParksList, optionsParksElement, "parks");
  populateCheckboxDropdown(allPercepcaoIndicators, selectedPercepcaoIndicators, optionsPercepcaoIndicatorsElement, "indicators");
  populateCheckboxDropdown(allVistoriasIndicators, selectedVistoriasIndicators, optionsVistoriasIndicatorsElement, "indicators-vistoria");
  populateCheckboxDropdown(allLivreIndicators, selectedLivreIndicators, optionsLivreIndicatorsElement, "indicators-livre");
}

// Handle checkbox updates and animation triggers
function handleFilterSelection(item, selectedList, element, typeKey, allList) {
  const index = selectedList.indexOf(item);
  if (index > -1) {
    if (selectedList.length > 1) {
      selectedList.splice(index, 1);
    } else {
      if (element) {
        if (element.tagName === "INPUT") {
          element.checked = true;
        }
        const selectContainer = element.closest(".custom-select") || element;
        if (selectContainer) {
          selectContainer.classList.add("shake");
          setTimeout(() => {
            selectContainer.classList.remove("shake");
          }, 400);
        }
      }
      return;
    }
  } else {
    selectedList.push(item);
  }
  
  if (selectedList === selectedPeriodsList || selectedList === selectedYearsList) {
    selectedList.sort();
  }
  
  updateHeaderSelectText(typeKey, selectedList, allList);
  updateChartData();
}

const jointPerformanceColors = ["#FF8200", "#3b82f6", "#10b981", "#f43f5e", "#8b5cf6", "#06b6d4", "#f59e0b", "#ec4899", "#14b8a6", "#6366f1"];

// Initialize Chart.js configuration
function initializeChart() {
  const ctx = document.getElementById("lineChart").getContext("2d");
  Chart.defaults.color = "#64748B";
  Chart.defaults.font.family = "'Outfit', sans-serif";
  
  myChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: []
    },
    plugins: [htmlLegendPlugin],
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: {
          top: 15,
          right: 0
        }
      },
      interaction: {
        mode: "index",
        intersect: false
      },
      plugins: {
        legend: {
          display: false
        },
        htmlLegend: {
          containerID: "html-legend-main"
        },
        tooltip: {
          backgroundColor: "rgba(255, 255, 255, 0.95)",
          titleColor: "#0F172A",
          bodyColor: "#334155",
          borderColor: "rgba(0,0,0,0.1)",
          borderWidth: 1,
          padding: 12,
          boxPadding: 6,
          usePointStyle: true,
          titleFont: {
            size: 16
          },
          bodyFont: {
            size: 16
          }
        }
      },
      scales: {
        x: {
          grid: {
            color: "rgba(0, 0, 0, 0.05)",
            drawBorder: false
          },
          ticks: {
            font: {
              size: 14
            }
          }
        },
        y: {
          min: 0,
          max: 1,
          grid: {
            color: "rgba(0, 0, 0, 0.05)",
            drawBorder: false
          },
          ticks: {
            font: {
              size: 14
            }
          }
        }
      }
    }
  });
  
  window.myChart = myChartInstance;
}

// Compute averages and bind dataset vectors to the Chart
function updateChartData() {
  if (!myChartInstance) return;
  
  const activePeriods = [...(currentTimeView === "quarterly" ? selectedPeriodsList : selectedYearsList)].sort();
  myChartInstance.data.labels = activePeriods;
  
  const datasets = [];
  const dashPatterns = [[], [5, 5], [2, 2], [10, 5], [10, 5, 2, 5]];
  
  if (currentDashboardMode === "percepcao") {
    selectedParksList.forEach(park => {
      selectedPercepcaoIndicators.forEach(indicator => {
        const dataValues = activePeriods.map(period => {
          let rows = [];
          if (currentTimeView === "quarterly") {
            rows = rawPercepcaoData.filter(r => (park === "Média" || (r.Unidade || r.Parque) === park) && r["Ano-periodo"] === period);
          } else {
            rows = rawPercepcaoData.filter(r => (park === "Média" || (r.Unidade || r.Parque) === park) && r["Ano-periodo"] && r["Ano-periodo"].startsWith(period));
          }
          
          if (rows.length > 0) {
            let sum = 0;
            let count = 0;
            rows.forEach(r => {
              const val = r[indicator];
              if (val != null && !isNaN(val)) {
                sum += val;
                count++;
              }
            });
            return count > 0 ? sum / count : null;
          }
          return null;
        });
        
        if (dataValues.some(v => v !== null)) {
          const color = parkColorMap[park] || "#000000";
          const dash = dashPatterns[selectedPercepcaoIndicators.indexOf(indicator) % dashPatterns.length];
          let label = `${park} - ${indicator}`;
          if (selectedParksList.length === 1 && selectedPercepcaoIndicators.length > 1) {
            label = indicator;
          }
          if (selectedPercepcaoIndicators.length === 1 && selectedParksList.length > 1) {
            label = park;
          }
          if (selectedParksList.length === 1 && selectedPercepcaoIndicators.length > 1) {
            label = `${park} (${indicator})`;
          }
          
          datasets.push({
            label: label,
            data: dataValues,
            borderColor: color,
            backgroundColor: color,
            borderDash: dash,
            borderWidth: 3,
            pointBackgroundColor: color,
            pointBorderColor: "#0B0F19",
            pointBorderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6,
            tension: 0.3,
            clip: false
          });
        }
      });
    });
  } else if (currentDashboardMode === "vistorias") {
    selectedParksList.forEach(park => {
      selectedVistoriasIndicators.forEach(indicator => {
        const dataValues = activePeriods.map(period => {
          let rows = [];
          if (currentTimeView === "quarterly") {
            rows = rawVistoriasData.filter(r => (park === "Média" || (r.Unidade || r.Parque) === park) && r["Ano-periodo"] === period);
          } else {
            rows = rawVistoriasData.filter(r => (park === "Média" || (r.Unidade || r.Parque) === park) && r["Ano-periodo"] && r["Ano-periodo"].startsWith(period));
          }
          
          if (rows.length > 0) {
            let sum = 0;
            let count = 0;
            rows.forEach(r => {
              const val = r[indicator];
              if (val != null && !isNaN(val)) {
                sum += val;
                count++;
              }
            });
            return count > 0 ? sum / count : null;
          }
          return null;
        });
        
        if (dataValues.some(v => v !== null)) {
          const color = parkColorMap[park] || "#000000";
          const dash = dashPatterns[selectedVistoriasIndicators.indexOf(indicator) % dashPatterns.length];
          let label = `${park} - ${indicator}`;
          if (selectedParksList.length === 1 && selectedVistoriasIndicators.length > 1) {
            label = indicator;
          }
          if (selectedVistoriasIndicators.length === 1 && selectedParksList.length > 1) {
            label = park;
          }
          if (selectedParksList.length === 1 && selectedVistoriasIndicators.length > 1) {
            label = `${park} (${indicator})`;
          }
          
          datasets.push({
            label: label,
            data: dataValues,
            borderColor: color,
            backgroundColor: color,
            borderDash: dash,
            borderWidth: 3,
            pointBackgroundColor: color,
            pointBorderColor: "#0B0F19",
            pointBorderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6,
            tension: 0.3,
            clip: false
          });
        }
      });
    });
  } else if (currentDashboardMode === "livre") {
    selectedParksList.forEach(park => {
      selectedLivreIndicators.forEach((fullIndicator, idx) => {
        let datasetToUse = [];
        let indicatorName = fullIndicator;
        if (fullIndicator.startsWith("[PS]")) {
          datasetToUse = rawPercepcaoData;
          indicatorName = fullIndicator.replace("[PS] ", "");
        } else if (fullIndicator.startsWith("[Vistoria]")) {
          datasetToUse = rawVistoriasData;
          indicatorName = fullIndicator.replace("[Vistoria] ", "");
        } else if (fullIndicator.startsWith("[Desempenho]")) {
          datasetToUse = fullIndicator === "[Desempenho] IPU" ? rawFdepData : rawFdeData;
          indicatorName = fullIndicator.replace("[Desempenho] ", "");
        }
        
        const dataValues = activePeriods.map(period => {
          let rows = [];
          if (currentTimeView === "quarterly") {
            if (indicatorName === "IPC") {
              rows = datasetToUse.filter(r => r["Ano-periodo"] === period);
            } else {
              rows = datasetToUse.filter(r => (park === "Média" || (r.Unidade || r.Parque) === park) && r["Ano-periodo"] === period);
            }
          } else {
            if (indicatorName === "IPC") {
              rows = datasetToUse.filter(r => r["Ano-periodo"] && r["Ano-periodo"].startsWith(period));
            } else {
              rows = datasetToUse.filter(r => (park === "Média" || (r.Unidade || r.Parque) === park) && r["Ano-periodo"] && r["Ano-periodo"].startsWith(period));
            }
          }
          
          if (rows.length > 0) {
            let sum = 0;
            let count = 0;
            rows.forEach(r => {
              const val = r[indicatorName];
              if (val != null && !isNaN(val)) {
                sum += val;
                count++;
              }
            });
            return count > 0 ? sum / count : null;
          }
          return null;
        });
        
        if (dataValues.some(v => v !== null)) {
          const color = indicatorName === "IPC" ? jointPerformanceColors[0] : parkColorMap[park] || "#000000";
          const dash = dashPatterns[idx % dashPatterns.length];
          let label = indicatorName === "IPC" ? "FDE Global" : `${park} - ${indicatorName}`;
          if (selectedParksList.length === 1 && selectedLivreIndicators.length > 1 && indicatorName !== "IPC") {
            label = indicatorName;
          }
          if (selectedLivreIndicators.length === 1 && selectedParksList.length > 1 && indicatorName !== "IPC") {
            label = park;
          }
          
          datasets.push({
            label: label,
            data: dataValues,
            borderColor: color,
            backgroundColor: color,
            borderDash: dash,
            borderWidth: 3,
            pointBackgroundColor: color,
            pointBorderColor: "#0B0F19",
            pointBorderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6,
            tension: 0.3,
            clip: false
          });
        }
      });
    });
  } else if (currentPerformanceIndicator === "IPU") {
    selectedParksList.forEach(park => {
      const dataValues = activePeriods.map(period => {
        let rows = [];
        if (currentTimeView === "quarterly") {
          rows = rawFdepData.filter(r => (park === "Média" || (r.Unidade || r.Parque) === park) && r["Ano-periodo"] === period);
        } else {
          rows = rawFdepData.filter(r => (park === "Média" || (r.Unidade || r.Parque) === park) && r["Ano-periodo"] && r["Ano-periodo"].startsWith(period));
        }
        
        if (rows.length > 0) {
          let sum = 0;
          let count = 0;
          rows.forEach(r => {
            const val = (r.IPU !== undefined ? r.IPU : r.FDEp);
            if (val != null && !isNaN(val)) {
              sum += val;
              count++;
            }
          });
          return count > 0 ? sum / count : null;
        }
        return null;
      });
      
      if (dataValues.some(v => v !== null)) {
        const color = parkColorMap[park] || "#000000";
        const dash = dashPatterns[0];
        
        datasets.push({
          label: `${park} - FDEp`,
          data: dataValues,
          borderColor: color,
          backgroundColor: color,
          borderDash: dash,
          borderWidth: 3,
          pointBackgroundColor: color,
          pointBorderColor: "#0B0F19",
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6,
          tension: 0.3,
          clip: false
        });
      }
    });
  } else if (currentPerformanceIndicator === "IPC") {
    const dataValues = activePeriods.map(period => {
      let rows = [];
      if (currentTimeView === "quarterly") {
        rows = rawFdeData.filter(r => r["Ano-periodo"] === period);
      } else {
        rows = rawFdeData.filter(r => r["Ano-periodo"] && r["Ano-periodo"].startsWith(period));
      }
      
      if (rows.length > 0) {
        let sum = 0;
        let count = 0;
        rows.forEach(r => {
          const val = (r.IPC !== undefined ? r.IPC : r.FDE);
          if (val != null && !isNaN(val)) {
            sum += val;
            count++;
          }
        });
        return count > 0 ? sum / count : null;
      }
      return null;
    });
    
    if (dataValues.some(v => v !== null)) {
      const color = jointPerformanceColors[0];
      
      datasets.push({
        label: "Nota Conjunta FDE",
        data: dataValues,
        borderColor: color,
        backgroundColor: color,
        borderWidth: 3,
        pointBackgroundColor: color,
        pointBorderColor: "#0B0F19",
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
        tension: 0.3,
        clip: false
      });
    }
  }
  
  myChartInstance.data.datasets = datasets;
  myChartInstance.update();
}

// High resolution print and export utility using html2canvas
if (exportButton) {
  exportButton.addEventListener("click", () => {
    const chartWrapper = document.querySelector(".chart-wrapper");
    const sidebar = document.querySelector(".sidebar");
    const chartTitle = document.getElementById("chart-title");
    
    const originalColor = Chart.defaults.color;
    const originalFontFamily = Chart.defaults.font.family;
    const originalOptionsCopy = JSON.parse(JSON.stringify(myChartInstance.options));
    
    Chart.defaults.color = "#333333";
    Chart.defaults.font.family = "'Arial', sans-serif";
    
    const exportColors = ["#00506E", "#F08200", "#598ea1", "#f5b466"];
    const exportPointStyles = ["rect", "triangle", "circle", "rectRot"];
    
    myChartInstance.data.datasets.forEach((dataset, idx) => {
      if (dataset.label && dataset.label.includes(" (")) {
        dataset.originalLabel = dataset.label;
        dataset.label = dataset.label.split(" (")[0].trim();
      }
      dataset.borderColor = exportColors[idx % exportColors.length];
      dataset.backgroundColor = exportColors[idx % exportColors.length];
      dataset.pointBackgroundColor = exportColors[idx % exportColors.length];
      dataset.pointBorderColor = exportColors[idx % exportColors.length];
      dataset.pointStyle = exportPointStyles[idx % exportPointStyles.length];
      dataset.borderWidth = 2.5;
      dataset.pointRadius = 6;
      dataset.pointHoverRadius = 8;
      dataset.tension = 0;
      dataset.clip = false;
      
      if (myChartInstance.options.plugins && myChartInstance.options.plugins.legend) {
        myChartInstance.options.plugins.legend.labels.font = { size: 16 };
        myChartInstance.options.plugins.legend.labels.padding = 20;
      }
    });
    
    myChartInstance.options.plugins.legend.labels.color = "#333333";
    chartTitle.style.display = "none";
    
    let indicatorsList = [];
    if (currentDashboardMode === "percepcao") {
      indicatorsList = selectedPercepcaoIndicators;
    } else if (currentDashboardMode === "vistorias") {
      indicatorsList = selectedVistoriasIndicators;
    } else {
      indicatorsList = [currentPerformanceIndicator];
    }
    
    myChartInstance.options.plugins.title = {
      display: true,
      text: indicatorsList.join(", "),
      font: {
        size: 16,
        weight: "bold",
        family: "'Arial', sans-serif"
      },
      color: "#333333",
      padding: {
        bottom: 20
      }
    };
    
    myChartInstance.options.layout = {
      padding: {
        top: 20
      }
    };
    
    myChartInstance.options.scales.x.grid = { display: false };
    myChartInstance.options.scales.x.border = { display: true, color: "#CCCCCC", width: 1 };
    myChartInstance.options.scales.x.ticks = { color: "#333333", font: { size: 14 } };
    
    myChartInstance.options.scales.y.grid = {
      color: "#CCCCCC",
      drawBorder: false,
      borderDash: [1, 3],
      lineWidth: 0.8
    };
    myChartInstance.options.scales.y.border = { display: true, color: "#CCCCCC", width: 1 };
    myChartInstance.options.scales.y.ticks = { color: "#333333", font: { size: 14 } };
    
    myChartInstance.update();
    
    document.body.classList.add("export-light-mode");
    sidebar.style.display = "none";
    
    setTimeout(() => {
      html2canvas(chartWrapper, {
        scale: 2,
        backgroundColor: "#FFFFFF",
        logging: false
      }).then(canvas => {
        document.body.classList.remove("export-light-mode");
        Chart.defaults.color = originalColor;
        Chart.defaults.font.family = originalFontFamily;
        
        myChartInstance.options = originalOptionsCopy;
        myChartInstance.data.datasets.forEach(dataset => {
          if (dataset.originalLabel) {
            dataset.label = dataset.originalLabel;
          }
        });
        
        chartTitle.style.display = "block";
        updateChartData();
        sidebar.style.display = "";
        
        const link = document.createElement("a");
        link.download = `dashboard-operacional-${new Date().getTime()}.png`;
        link.href = canvas.toDataURL("image/png");
        link.click();
      });
    }, 300);
  });
}

// Shake animation injection
const styleTag = document.createElement("style");
styleTag.innerHTML = `
@keyframes shake {
  0% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  50% { transform: translateX(4px); }
  75% { transform: translateX(-4px); }
  100% { transform: translateX(0); }
}
.shake { animation: shake 0.4s ease-in-out; }
`;
document.head.appendChild(styleTag);

// KPI strategic insights library
const kpiInsights = {
  percepcao: [
    {
      value: "89,1%",
      title: "Média de Experiência (IQX)",
      subtitle: "Satisfação estável com baixa variabilidade.",
      tooltip: "A curva de percepção e experiência dos usuários demonstra estabilidade histórica contínua, com notas consistentes entre os ciclos operacionais."
    },
    {
      value: "67,3%",
      title: "Ponto de Atenção",
      subtitle: "Serviços e Conveniência (IND-A10) registra a menor média.",
      tooltip: "Este indicador representa a menor pontuação apurada na amostragem, configurando uma alavanca prioritária de modernização nos serviços prestados."
    },
    {
      value: "Unidade Fictícia 06",
      title: "Mobilidade e Acessibilidade",
      subtitle: "Registra desafio estrutural no indicador IND-A06.",
      tooltip: "A Unidade Fictícia 06 demanda intervenções estruturais em mobilidade interna e acessibilidade conforme apontado na pesquisa amostral."
    }
  ],
  vistorias: [
    {
      value: "87,0%",
      title: "Média de Auditoria (IAT)",
      subtitle: "Índice equilibrado em Conformidade e Protocolos de Segurança.",
      tooltip: "As auditorias técnicas apontam conformidade consistente nos pilares fundamentais de conservação predial e segurança das unidades operacionais."
    },
    {
      value: "68,4%",
      title: "Oportunidade Técnica",
      subtitle: "Acompanhamento do indicador IND-B04.",
      tooltip: "A Gestão de Paisagismo e Ativos (IND-B04) registra médias técnicas mais modestas, indicando oportunidade de aprimoramento nos cronogramas preventivos."
    },
    {
      value: "Oscilações no IND-B05",
      title: "Conformidade em Resíduos",
      subtitle: "Oscilações pontuais registradas no indicador IND-B05.",
      tooltip: "Registros pontuais atípicos observados em auditorias anteriores, sugerindo aprimoramento contínuo nas rotinas de registro e fiscalização."
    },
    {
      value: "Unidade Fictícia 01",
      title: "Polo de Alto Fluxo",
      subtitle: "Comportamento associado à escala operacional.",
      tooltip: "A Unidade Fictícia 01 apresenta métricas características de polos corporativos de grande porte e alta circulação contínua."
    }
  ],
  desempenho: [
    {
      value: "88,7%",
      title: "Média Global (IPC)",
      subtitle: "Desvio padrão estatístico de apenas 2 pontos percentuais.",
      tooltip: "A métrica consolidada reflete alto nível de previsibilidade e regularidade nas entregas ao longo de todos os trimestres."
    },
    {
      value: "Unidades 02, 05 e 03",
      title: "Liderança de Desempenho",
      subtitle: "Unidades que sustentam o topo das avaliações.",
      tooltip: "As Unidades Fictícias 02, 05 e 03 sustentam o topo do ranking de pontuação, enquanto as unidades 04 e 06 representam oportunidades de evolução gradual."
    },
    {
      value: "80%",
      title: "Sensibilidade: IAT x IPU",
      subtitle: "Auditoria técnica pondera a variação do índice da unidade.",
      tooltip: "O Índice de Auditoria Técnica (IAT) exerce papel preponderante na calibração final do IPU de cada unidade operacional."
    },
    {
      value: "Ativos Estruturais",
      title: "Maior Potencial de Elevação",
      subtitle: "Forte impacto positivo na pontuação consolidada.",
      tooltip: "A elevação de conformidade no indicador IND-B04 representa a maior sensibilidade matemática para aprimorar o índice consolidado IPC."
    }
  ]
};

window.renderKPIs = function(mode) {
  const container = document.getElementById("kpi-container");
  if (!container) return;
  
  const insights = kpiInsights[mode] || [];
  container.innerHTML = "";
  
  insights.forEach(insight => {
    const card = document.createElement("div");
    card.className = "bg-white/80 backdrop-blur border border-slate-200 rounded-xl p-4 shadow-sm relative group transition-all hover:shadow-md hover:border-brand/30";
    card.innerHTML = `
      <div class="absolute top-4 right-4 text-slate-400 hover:text-brand cursor-help group/icon">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
          </svg>
          <!-- Tooltip flutuante Premium -->
          <div class="absolute z-[100] invisible group-hover/icon:visible opacity-0 group-hover/icon:opacity-100 transition-all duration-300 w-72 bg-white/95 backdrop-blur border border-slate-200 text-slate-600 text-[15px] leading-relaxed rounded-xl p-4 right-0 top-6 shadow-2xl origin-top-right transform scale-95 group-hover/icon:scale-100">
              <div class="font-bold text-slate-800 mb-2 border-b border-slate-100 pb-1 text-sm">Insight Estratégico</div>
              ${insight.tooltip}
          </div>
      </div>
      
      <div class="text-brand text-xs font-bold uppercase tracking-wider mb-1 pr-6">${insight.title}</div>
      <div class="text-2xl font-black text-slate-800 mb-1 leading-tight">${insight.value}</div>
      <div class="text-sm text-slate-500">${insight.subtitle}</div>
    `;
    container.appendChild(card);
  });
};

// Bootstrap the application
loadData();
window.renderKPIs(currentDashboardMode);

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
  glossaryModal.addEventListener("click", (e) => {
    if (e.target === glossaryModal) {
      glossaryModal.classList.remove("show");
    }
  });
}
