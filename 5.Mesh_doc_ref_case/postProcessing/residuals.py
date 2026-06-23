import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import os

base_dir = os.path.dirname(__file__)

# pasta para salvar figuras
fig_dir = os.path.join(base_dir, "figures")
os.makedirs(fig_dir, exist_ok=True)

plt.ion()

# =========================
# FUNÇÕES AUXILIARES
# =========================
def get_time_folders(path):
    folders = []
    for name in os.listdir(path):
        full_path = os.path.join(path, name)

        if os.path.isdir(full_path):
            try:
                folders.append(float(name))
            except:
                continue

    return sorted(folders)


# =========================
# RESIDUALS -> DATAFRAME
# =========================
def read_residuals_df(base_dir):
    residuals_dir = os.path.join(base_dir, 'residuals')

    data = []
    time_offset = 0

    try:
        folders = get_time_folders(residuals_dir)

        for t in folders:
            folder_name = str(int(t)) if t.is_integer() else str(t)
            file_path = os.path.join(residuals_dir, folder_name, 'residuals.dat')

            if not os.path.exists(file_path):
                continue

            local_times = []

            with open(file_path, "r") as f:
                for line in f:
                    if line.startswith("#"):
                        continue

                    parts = line.split()

                    if len(parts) < 7 or "N/A" in parts:
                        continue

                    local_time = float(parts[0])

                    if len(local_times) > 0 and local_time <= local_times[-1]:
                        continue

                    local_times.append(local_time)

                    data.append({
                        "time": local_time ,
                        "Ux": float(parts[1]),
                        "Uy": float(parts[2]),
                        "Uz": float(parts[3]),
                        "p": float(parts[4]),
                        "k": float(parts[5]),
                        "omega": float(parts[6])
                    })

            if local_times:
                time_offset += local_times[-1]

    except Exception as e:
        print("Erro residuals:", e)

    
    return pd.DataFrame(data)


# =========================
# YPLUS -> DATAFRAME
# =========================
def read_yplus_df(base_dir):
    yplus_dir = os.path.join(base_dir, 'yPlus')

    data = []
    time_offset = 0

    try:
        folders = get_time_folders(yplus_dir)

        for t in folders:
            folder_name = str(int(t)) if t.is_integer() else str(t)
            file_path = os.path.join(yplus_dir, folder_name, 'yPlus.dat')

            if not os.path.exists(file_path):
                continue

            local_times = []

            with open(file_path, "r") as f:
                for line in f:
                    if line.startswith("#"):
                        continue

                    parts = line.split()

                    if len(parts) < 5:
                        continue

                    if parts[1] != "tpms":
                        continue

                    local_time = float(parts[0])

                    if len(local_times) > 0 and local_time <= local_times[-1]:
                        continue

                    local_times.append(local_time)

                    data.append({
                        "time": local_time,
                        "y_min": float(parts[2]),
                        "y_max": float(parts[3]),
                        "y_avg": float(parts[4])
                    })

            if local_times:
                time_offset += local_times[-1]

    except Exception as e:
        print("Erro yPlus:", e)

    return pd.DataFrame(data)


# =========================
# FIGURAS
# =========================
fig1, ax1 = plt.subplots(figsize=(8,6))
fig2, ax2 = plt.subplots(figsize=(8,6))


# =========================
# LOOP PRINCIPAL
# =========================
while True:

    df_res = read_residuals_df(base_dir)
    df_y = read_yplus_df(base_dir)

    # =========================
    # PLOT RESIDUALS
    # =========================
    ax1.clear()

    if not df_res.empty:
        for col in ["Ux", "Uy", "Uz", "p", "k", "omega"]:
            ax1.semilogy(df_res["time"], df_res[col], 'o--', label=col)

    ax1.set_xlabel("Iteration contínua")
    ax1.set_ylabel("Residual")
    ax1.set_title("Residuals Convergence (contínuo)")
    ax1.legend()
    ax1.grid(True)

    fig1.canvas.draw()
    fig1.canvas.flush_events()

    # =========================
    # PLOT YPLUS
    # =========================
    ax2.clear()

    if not df_y.empty:
        for col in ["y_min", "y_max", "y_avg"]:
            ax2.semilogy(df_y["time"], df_y[col], 'o--', label=col)

    ax2.set_xlabel("Time contínuo")
    ax2.set_ylabel("y+")
    ax2.set_title("y+ (contínuo)")
    ax2.legend()
    ax2.grid(True)

    fig2.canvas.draw()
    fig2.canvas.flush_events()

    # salvar
    fig1.savefig(os.path.join(fig_dir, "residuals.png"), dpi=150)
    fig2.savefig(os.path.join(fig_dir, "yplus.png"), dpi=150)

    time.sleep(5)