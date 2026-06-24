#!/usr/bin/env python3

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit



# ==========================================================
# FUNÇÃO DE AJUSTE DARCY-FORCHHEIMER
# ==========================================================

def calcular_permeabilidade(
    Re,
    dP,
    L,
    D,
    rho,
    nu
):

    Re = np.asarray(Re, dtype=float)
    dP = np.asarray(dP, dtype=float)

    if len(Re) != len(dP):
        raise ValueError(
            "Os vetores Re e dP devem possuir o mesmo tamanho."
        )

    mu = rho * nu

    # velocidade superficial
    V = Re * nu / D

    # gradiente de pressão
    dpdx = dP / L

    def modelo(v, A, B):
        return A * v + B * v**2

    popt, _ = curve_fit(
        modelo,
        V,
        dpdx
    )

    A, B = popt

    K = mu / A
    Cf = B / rho

    dpdx_fit = modelo(
        V,
        *popt
    )

    ss_res = np.sum(
        (dpdx - dpdx_fit) ** 2
    )

    ss_tot = np.sum(
        (dpdx - np.mean(dpdx)) ** 2
    )

    r2 = 1 - ss_res / ss_tot

    return {
        "K": K,
        "Cf": Cf,
        "A": A,
        "B": B,
        "R2": r2
    }

# ==========================================================
# PARÂMETROS FIXOS
# ==========================================================

# Distância entre tomadas de pressão [m]
L = 0.064

# ==========================================================
# LEITURA DOS DADOS
# ==========================================================

arquivo = "dados.ods"

df = pd.read_excel(
    arquivo,
    engine="odf"
)

# ==========================================================
# DATAFRAME REDUZIDO
# ==========================================================

df_reduzido = (
    df[
        [
            "TPMS",
            "Re_Canal",
            "DeltaPTPMS",
            "Dh_Entrada(mm)",
            "Densidade(kg/m3)",
            "ν(m2/s)"
        ]
    ]
    .dropna()
    .copy()
)

df_reduzido = df_reduzido.sort_values(
    by=["TPMS", "Re_Canal"]
)

df_reduzido.to_excel(
    "dados_reduzidos.xlsx",
    index=False
)

# ==========================================================
# CONFIGURAÇÃO DOS GRÁFICOS
# ==========================================================

sns.set_theme(
    style="darkgrid",
    context="paper"
)

# ==========================================================
# CORES E MARCADORES FIXOS
# ==========================================================

tpms_unicos = sorted(
    df_reduzido["TPMS"].unique()
)

palette = sns.color_palette(
    "tab10",
    n_colors=len(tpms_unicos)
)

marcadores = [
    "o",
    "s",
    "^",
    "D",
    "v",
    "P",
    "X",
    "*",
    "<",
    ">"
]

cores_tpms = {
    tpms: palette[i]
    for i, tpms in enumerate(tpms_unicos)
}

marcadores_tpms = {
    tpms: marcadores[i % len(marcadores)]
    for i, tpms in enumerate(tpms_unicos)
}

# ==========================================================
# RESULTADOS
# ==========================================================

resultados_tpms = []

# ==========================================================
# GRÁFICO GERAL
# ==========================================================

fig_geral, ax = plt.subplots(
    figsize=(14, 9)
)

for tpms, dados in df_reduzido.groupby("TPMS"):

    dados = dados.sort_values(
        "Re_Canal"
    )

    Re = dados["Re_Canal"].to_numpy()
    dP = dados["DeltaPTPMS"].to_numpy()

    # ======================================================
    # PROPRIEDADES DO FLUIDO E GEOMETRIA
    # ======================================================

    D = (
        dados["Dh_Entrada(mm)"]
        .iloc[0]
        / 1000.0
    )

    rho = (
        dados["Densidade(kg/m3)"]
        .iloc[0]
    )

    nu = (
        dados["ν(m2/s)"]
        .iloc[0]
    )

    resultado = calcular_permeabilidade(
        Re=Re,
        dP=dP,
        L=L,
        D=D,
        rho=rho,
        nu=nu
    )

    resultados_tpms.append(
        {
            "TPMS": tpms,
            "Dh [m]": D,
            "ρ [kg/m³]": rho,
            "ν [m²/s]": nu,
            "K [m²]": resultado["K"],
            "Cf [1/m]": resultado["Cf"],
            "R²": resultado["R2"]
        }
    )

    cor = cores_tpms[tpms]
    marcador = marcadores_tpms[tpms]

    # ======================================================
    # DADOS CFD
    # ======================================================

    ax.scatter(
        Re,
        dP,
        color=cor,
        marker=marcador,
        s=80
    )

    # ======================================================
    # CURVA AJUSTADA
    # ======================================================

    Re_fit = np.linspace(
        Re.min(),
        Re.max(),
        300
    )

    V_fit = Re_fit * nu / D

    A = resultado["A"]
    B = resultado["B"]

    dpdx_fit = (
        A * V_fit +
        B * V_fit**2
    )

    dP_fit = dpdx_fit * L

    ax.plot(
        Re_fit,
        dP_fit,
        "--",
        color=cor,
        linewidth=2.5,
        label=(
            f"{tpms}\n"
            f"K = {resultado['K']:.2e} m²\n"
            f"Cf = {resultado['Cf']:.2e} 1/m\n"
            f"R² = {resultado['R2']:.4f}"
        )
    )

ax.set_xlabel(
    r"$Re_{D}$"
)

ax.set_ylabel(
    r"$\Delta P_{TPMS}$ [Pa]"
)

ax.set_title(
    "Perda de carga CFD e ajuste Darcy-Forchheimer"
)

ax.legend(
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    fontsize=9
)

fig_geral.tight_layout()

fig_geral.savefig(
    "Darcy_Forchheimer_Todos_TPMS.png",
    dpi=300,
    bbox_inches="tight"
)

# ==========================================================
# GRÁFICOS INDIVIDUAIS
# ==========================================================

for tpms, dados in df_reduzido.groupby("TPMS"):

    dados = dados.sort_values(
        "Re_Canal"
    )

    Re = dados["Re_Canal"].to_numpy()
    dP = dados["DeltaPTPMS"].to_numpy()

    D = (
        dados["Dh_Entrada(mm)"]
        .iloc[0]
        / 1000.0
    )

    rho = (
        dados["Densidade(kg/m3)"]
        .iloc[0]
    )

    nu = (
        dados["ν(m2/s)"]
        .iloc[0]
    )

    resultado = calcular_permeabilidade(
        Re=Re,
        dP=dP,
        L=L,
        D=D,
        rho=rho,
        nu=nu
    )

    cor = cores_tpms[tpms]
    marcador = marcadores_tpms[tpms]

    fig, ax = plt.subplots(
        figsize=(9, 6)
    )

    ax.scatter(
        Re,
        dP,
        color=cor,
        marker=marcador,
        s=80,
        label="CFD (OpenFOAM)"
    )

    Re_fit = np.linspace(
        Re.min(),
        Re.max(),
        300
    )

    V_fit = Re_fit * nu / D

    A = resultado["A"]
    B = resultado["B"]

    dpdx_fit = (
        A * V_fit +
        B * V_fit**2
    )

    dP_fit = dpdx_fit * L

    ax.plot(
        Re_fit,
        dP_fit,
        "--",
        color=cor,
        linewidth=3,
        label=(
            "Modelo Darcy-Forchheimer\n"
            f"K = {resultado['K']:.3e} m²\n"
            f"Cf = {resultado['Cf']:.3e} 1/m\n"
            f"R² = {resultado['R2']:.4f}"
        )
    )

    ax.set_xlabel(
        r"$Re_{D}$"
    )

    ax.set_ylabel(
        r"$\Delta P_{TPMS}$ [Pa]"
    )

    ax.set_title(
        f"TPMS: {tpms}"
    )

    ax.legend()

    fig.tight_layout()

    fig.savefig(
        f"Darcy_Forchheimer_{tpms}".replace(" ", "_") + ".png",
        dpi=300,
        bbox_inches="tight"
    )

# ==========================================================
# EXPORTAR RESULTADOS
# ==========================================================

df_resultados = pd.DataFrame(
    resultados_tpms
)

df_resultados.to_excel(
    "Coeficientes_Darcy_Forchheimer.xlsx",
    index=False
)

# ==========================================================
# RESUMO
# ==========================================================

print("\n========== RESULTADOS ==========\n")
print(df_resultados)

print("\nDistância entre tomadas de pressão:")
print(f"L = {L:.3f} m")

print("\nArquivos gerados:")
print("- dados_reduzidos.xlsx")
print("- Coeficientes_Darcy_Forchheimer.xlsx")
print("- Darcy_Forchheimer_Todos_TPMS.png")

for tpms in tpms_unicos:
    print(
        f"- Darcy_Forchheimer_{str(tpms).replace(' ','_')}.png"
    )

# ==========================================================
# MOSTRAR TODAS AS FIGURAS
# ==========================================================

plt.show()