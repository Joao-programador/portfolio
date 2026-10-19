import json
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(20261015)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_JS = BASE_DIR / "mock_data.js"
OUTPUT_JSON = BASE_DIR / "mock_data.json"

LOCAIS = [
    {
        "id": "lote_1",
        "nome": "Lote 1 - Concessão Noroeste/Centro",
        "nome_curto": "Lote 1: Noroeste/Centro",
        "spe": "SPE ViaPaulista Concessões S.A.",
        "contrato": "CONC-SPP-001/2024",
        "baterias": [
            {"nome": "Terminal Barra Funda", "total": 18, "base_indisp": 2},
            {"nome": "Terminal Pinheiros", "total": 15, "base_indisp": 5},
            {"nome": "Terminal Princesa Isabel", "total": 14, "base_indisp": 0},
            {"nome": "Hub Urbano Luz", "total": 20, "base_indisp": 2},
            {"nome": "Parque Água Branca", "total": 12, "base_indisp": 0},
            {"nome": "Terminal Lapa", "total": 16, "base_indisp": 1},
            {"nome": "Mercado Municipal Paulistano", "total": 16, "base_indisp": 0},
        ],
    },
    {
        "id": "lote_2",
        "nome": "Lote 2 - Concessão Sul/Sudoeste",
        "nome_curto": "Lote 2: Sul/Sudoeste",
        "spe": "SPE Mobilidade Sul Parcerias S.A.",
        "contrato": "PPP-SPP-008/2023",
        "baterias": [
            {"nome": "Terminal Santo Amaro", "total": 20, "base_indisp": 3},
            {"nome": "Terminal Capelinha", "total": 16, "base_indisp": 2},
            {"nome": "Terminal Grajaú", "total": 16, "base_indisp": 5},
            {"nome": "Terminal Jardim Ângela", "total": 14, "base_indisp": 4},
            {"nome": "Parque Ibirapuera", "total": 20, "base_indisp": 1},
            {"nome": "Terminal Bandeira", "total": 15, "base_indisp": 0},
            {"nome": "Autódromo de Interlagos", "total": 18, "base_indisp": 0},
        ],
    },
    {
        "id": "lote_3",
        "nome": "Lote 3 - Concessão Leste/Sudeste",
        "nome_curto": "Lote 3: Leste/Sudeste",
        "spe": "SPE Conecta Leste Infraestrutura S.A.",
        "contrato": "CONC-SPP-014/2025",
        "baterias": [
            {"nome": "Terminal Itaquera", "total": 18, "base_indisp": 2},
            {"nome": "Terminal São Mateus", "total": 15, "base_indisp": 4},
            {"nome": "Terminal Sacomã", "total": 18, "base_indisp": 1},
            {"nome": "Terminal Vila Prudente", "total": 16, "base_indisp": 0},
            {"nome": "Parque do Carmo", "total": 12, "base_indisp": 0},
            {"nome": "Terminal Parque Dom Pedro II", "total": 20, "base_indisp": 2},
            {"nome": "Terminal Cidade Tiradentes", "total": 14, "base_indisp": 3},
        ],
    },
]

CATALOGO_ATIVOS = [
    ("Eletroposto Rápido 250kW", "Eletromobilidade"),
    ("Subestação Elétrica 13.8kV", "Infraestrutura Elétrica"),
    ("Plataforma de Embarque A", "Obras Civis & Hidráulica"),
    ("Sistema CCO / CFTV Analítico", "Sistemas & Telemetria"),
    ("Elevador de Acessibilidade Sul", "Segurança & Acessibilidade"),
    ("Bomba de Drenagem Pluvial", "Obras Civis & Hidráulica"),
    ("Escada Rolante Principal", "Segurança & Acessibilidade"),
    ("Painel PMV de Telemetria", "Sistemas & Telemetria"),
    ("Catracas de Bilhetagem Óptica", "Sistemas & Telemetria"),
    ("Gerador de Emergência QTA", "Infraestrutura Elétrica"),
    ("Eletroposto Ultrarrápido B", "Eletromobilidade"),
    ("Iluminação Telegestionada LED", "Infraestrutura Elétrica"),
    ("Sistema de Detecção Incêndio", "Segurança & Acessibilidade"),
    ("Reservatório de Reúso Hidráulico", "Obras Civis & Hidráulica"),
    ("Subestação Retificadora B", "Infraestrutura Elétrica"),
    ("Eletroposto Carga Rápida C", "Eletromobilidade"),
    ("Gateway Fibra Óptica Redundante", "Sistemas & Telemetria"),
    ("Elevador Transferência Norte", "Segurança & Acessibilidade"),
    ("Plataforma de Embarque B", "Obras Civis & Hidráulica"),
    ("Carregador Pantográfico Bus", "Eletromobilidade"),
]

STATUS_OPCOES = [
    "Em Atendimento pela SPE",
    "Autuado / Prazo Vencido",
    "Aguardando Peça Importada",
    "Em Vistoria Técnica",
]

MOTIVOS_POR_CATEGORIA = {
    "Infraestrutura Elétrica": [
        "Queda de Tensão na Subestação",
        "Manutenção Corretiva Emergencial",
    ],
    "Sistemas & Telemetria": [
        "Falha de Comunicação Fibra CCO",
        "Manutenção Corretiva Emergencial",
    ],
    "Obras Civis & Hidráulica": [
        "Vandalismo / Dano Físico",
        "Manutenção Corretiva Emergencial",
    ],
    "Eletromobilidade": [
        "Inoperância de Recarga Elétrica",
        "Queda de Tensão na Subestação",
    ],
    "Segurança & Acessibilidade": [
        "Vandalismo / Dano Físico",
        "Manutenção Corretiva Emergencial",
    ],
}


def calcular_prioridade(indisponiveis: int) -> str:
    if indisponiveis >= 3:
        return "P1"
    if indisponiveis >= 1:
        return "P2"
    return "Sem pendência"


def calcular_condicao(df_percentual: float) -> str:
    return "Operacional" if df_percentual >= 80.0 else "Abaixo do mínimo"


def gerar_bases():
    end_date = date(2026, 10, 15)
    days = 30
    start_date = end_date - timedelta(days=days - 1)

    disponibilidade_fisica = []
    pendencias = []
    chamado_seq = 400

    for day_idx in range(days):
        curr_date = start_date + timedelta(days=day_idx)
        date_str = curr_date.isoformat()
        is_last_day = (day_idx == days - 1)

        weather_stress = 1 if 13 <= day_idx <= 18 else 0

        for lote in LOCAIS:
            for bat_idx, bat in enumerate(lote["baterias"]):
                total = bat["total"]
                base_ind = bat["base_indisp"]

                if is_last_day:
                    indisp = base_ind
                else:
                    wave = ((day_idx + bat_idx * 3) % 7) - 3
                    delta = 0
                    if wave == 3:
                        delta = 1
                    elif wave == -3 and base_ind > 0:
                        delta = -1

                    if weather_stress and (bat_idx % 2 == 0):
                        delta += 1

                    if day_idx < 10 and base_ind >= 2:
                        delta += 1

                    indisp = max(0, min(total - 4, base_ind + delta))

                disp = total - indisp
                df_pct = round((disp / total) * 100.0, 1)
                prio = calcular_prioridade(indisp)
                cond = calcular_condicao(df_pct)

                rec_id = f"{lote['id']}_{bat_idx}_{date_str}"
                disponibilidade_fisica.append({
                    "id": rec_id,
                    "data": date_str,
                    "local_id": lote["id"],
                    "local": lote["nome"],
                    "local_curto": lote["nome_curto"],
                    "spe": lote["spe"],
                    "contrato": lote["contrato"],
                    "bateria": bat["nome"],
                    "total_ativos": total,
                    "disponiveis": disp,
                    "indisponiveis": indisp,
                    "df_percentual": df_pct,
                    "prioridade": prio,
                    "condicao": cond,
                })

                if indisp > 0:
                    indices_unidades = list(range(total))
                    rng = random.Random(f"{bat['nome']}_{date_str}")
                    unidades_afetadas = sorted(rng.sample(indices_unidades, indisp))

                    for rank_u, u_idx in enumerate(unidades_afetadas):
                        chamado_seq += 1
                        cat_item = CATALOGO_ATIVOS[u_idx % len(CATALOGO_ATIVOS)]
                        nome_ativo = f"Unid. {u_idx + 1:02d} - {cat_item[0]}"
                        categoria = cat_item[1]

                        status_str = STATUS_OPCOES[(u_idx + day_idx + bat_idx) % len(STATUS_OPCOES)]
                        motivos_lista = MOTIVOS_POR_CATEGORIA[categoria]
                        motivo_str = motivos_lista[(u_idx + bat_idx) % len(motivos_lista)]

                        prio_chamado = "P1" if (prio == "P1" and rank_u < 3) else ("P1" if prio == "P1" else "P2")
                        horas_abertas = 4 + ((u_idx * 7 + day_idx * 3) % 68)
                        glosa_brl = 18500 if prio_chamado == "P1" else 6200

                        pendencias.append({
                            "id_chamado": f"SPP-2026-{chamado_seq:04d}",
                            "data": date_str,
                            "local_id": lote["id"],
                            "local": lote["nome"],
                            "local_curto": lote["nome_curto"],
                            "spe": lote["spe"],
                            "bateria": bat["nome"],
                            "unidade_num": u_idx + 1,
                            "ciclone": nome_ativo,
                            "status": status_str,
                            "motivo": motivo_str,
                            "categoria": categoria,
                            "prioridade": prio_chamado,
                            "prioridade_complexo": prio,
                            "sla_horas": horas_abertas,
                            "glosa_brl": glosa_brl,
                        })

    catalogo_complexos = {}
    for lote in LOCAIS:
        for bat in lote["baterias"]:
            unidades = []
            for u_idx in range(bat["total"]):
                cat_item = CATALOGO_ATIVOS[u_idx % len(CATALOGO_ATIVOS)]
                unidades.append({
                    "unidade_num": u_idx + 1,
                    "ciclone": f"Unid. {u_idx + 1:02d} - {cat_item[0]}",
                    "categoria": cat_item[1],
                })
            catalogo_complexos[bat["nome"]] = {
                "bateria": bat["nome"],
                "local": lote["nome"],
                "spe": lote["spe"],
                "contrato": lote["contrato"],
                "total_ativos": bat["total"],
                "unidades": unidades,
            }

    datas_unicas = sorted(list({r["data"] for r in disponibilidade_fisica}))

    payload = {
        "meta": {
            "organizacao": "Prefeitura de São Paulo • São Paulo Parcerias (SPP)",
            "sistema": "Centro de Controle de Concessões e PPPs",
            "meta_contratual_df": 80.0,
            "data_atual": datas_unicas[-1],
            "data_inicio": datas_unicas[0],
            "total_dias": len(datas_unicas),
            "datas": datas_unicas,
            "locais": LOCAIS,
            "catalogo_complexos": catalogo_complexos,
        },
        "disponibilidade_fisica": disponibilidade_fisica,
        "pendencias": pendencias,
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    js_content = f"window.SPP_MOCK_DATA = {json.dumps(payload, ensure_ascii=False)};\n"
    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write(js_content)

    print("Dataset exclusivo Concessoes SP gerado com sucesso.")


if __name__ == "__main__":
    gerar_bases()
