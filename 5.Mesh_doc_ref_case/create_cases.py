#!/usr/bin/env python3

import os
import re
import shutil
import subprocess
from pathlib import Path
from tqdm import tqdm

# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

TEMPLATE_CASE = "ReXXXX"

# Água a 20°C
nu = 1e-6      # m²/s

# Diâmetro do bocal
D = 30e-3      # m

# Intensidade turbulenta
I = 0.05       # 5 %

# ==========================================================
# FUNÇÕES
# ==========================================================

def calc_properties(Re):

    U = Re * nu / D

    k = 1.5 * (I * U)**2

    omega = k / nu

    return U, k, omega


def replace_internal_field_U(text, U):

    pattern = r'internalField\s+uniform\s+\([^)]+\);'

    replacement = f'internalField   uniform ({U:.8f} 0 0);'

    return re.sub(pattern, replacement, text)


def replace_internal_field_scalar(text, value):

    pattern = r'internalField\s+uniform\s+[0-9eE\+\-\.]+;'

    replacement = f'internalField   uniform {value:.8e};'

    return re.sub(pattern, replacement, text)


def replace_boundary_value_U(text, U):

    pattern = r'value\s+uniform\s+\([^)]+\);'

    replacement = f'value           uniform ({U:.8f} 0 0);'

    return re.sub(pattern, replacement, text)


def replace_boundary_value_scalar(text, value):

    pattern = r'value\s+uniform\s+[0-9eE\+\-\.]+;'

    replacement = f'value           uniform {value:.8e};'

    return re.sub(pattern, replacement, text)


def update_file(path, value, field_type):

    with open(path, "r") as f:
        text = f.read()

    if field_type == "U":

        text = replace_internal_field_U(text, value)
        text = replace_boundary_value_U(text, value)

    else:

        text = replace_internal_field_scalar(text, value)
        text = replace_boundary_value_scalar(text, value)

    with open(path, "w") as f:
        f.write(text)


def run_case(case_dir):

    print(f"\nRodando {case_dir}")

    try:

        result = subprocess.run(
            ["bash", "./run_script"],
            cwd=case_dir,
            check=True
        )

        return True

    except Exception:

        print("run_script falhou. Tentando run_from_stop...")

        try:

            result = subprocess.run(
                ["bash", "./run_from_stop"],
                cwd=case_dir,
                check=True
            )

            return True

        except Exception:

            return False


# ==========================================================
# MAIN
# ==========================================================

if not Path(TEMPLATE_CASE).exists():

    raise FileNotFoundError(
        f"Pasta modelo '{TEMPLATE_CASE}' não encontrada."
    )

if not Path("reynolds.txt").exists():

    raise FileNotFoundError(
        "Arquivo reynolds.txt não encontrado."
    )

with open("reynolds.txt") as f:

    reynolds_list = [
        int(line.strip())
        for line in f
        if line.strip()
    ]

print("\nModo de execução:")
print("1 - Apenas criar casos")
print("2 - Criar e rodar")

option = input("\nEscolha: ").strip()

run_cases = option == "2"

errors = []

for Re in tqdm(reynolds_list, desc="Processando casos"):

    case_name = f"Re{Re}"

    U, k, omega = calc_properties(Re)

    print(f"\n{'='*60}")
    print(f"Caso: {case_name}")
    print(f"U     = {U:.6f} m/s")
    print(f"k     = {k:.6e}")
    print(f"omega = {omega:.6e}")
    print(f"{'='*60}")

    if not Path(case_name).exists():

        shutil.copytree(TEMPLATE_CASE, case_name)

    # --------------------------------------------------
    # Atualiza arquivos
    # --------------------------------------------------

    update_file(
        f"{case_name}/0/U",
        U,
        "U"
    )

    update_file(
        f"{case_name}/0/k",
        k,
        "k"
    )

    update_file(
        f"{case_name}/0/omega",
        omega,
        "omega"
    )

    # --------------------------------------------------
    # Roda caso
    # --------------------------------------------------

    if run_cases:

        success = run_case(case_name)

        if not success:

            errors.append(Re)

            print(
                f"\nERRO: Não foi possível rodar o caso Re={Re}"
            )

# ==========================================================
# RESUMO
# ==========================================================

print("\n")

if errors:

    print("="*60)
    print("CASOS COM ERRO")
    print("="*60)

    for Re in errors:
        print(f"Re{Re}")

else:

    print("="*60)
    print("TODOS OS CASOS FINALIZADOS")
    print("="*60)