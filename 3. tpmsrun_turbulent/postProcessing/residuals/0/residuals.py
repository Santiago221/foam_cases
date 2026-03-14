import numpy as np
import matplotlib.pyplot as plt

file_path = "residuals.dat"

time = []
Ux = []
Uy = []
Uz = []
p = []
k = []
omega = []

with open(file_path, "r") as f:
    for line in f:
        if line.startswith("#"):
            continue

        parts = line.split()

        if len(parts) < 7 or "N/A" in parts:
            continue

        time.append(float(parts[0]))
        Ux.append(float(parts[1]))
        Uy.append(float(parts[2]))
        Uz.append(float(parts[3]))
        p.append(float(parts[4]))
        k.append(float(parts[5]))
        omega.append(float(parts[6]))

plt.figure(figsize=(8,6))

plt.semilogy(time, Ux, label="Ux")
plt.semilogy(time, Uy, label="Uy")
plt.semilogy(time, Uz, label="Uz")
plt.semilogy(time, p, label="p")
plt.semilogy(time, k, label="k")
plt.semilogy(time, omega, label="omega")

plt.xlabel("Iteration / Time")
plt.ylabel("Residual")
plt.title("Residuals Convergence")
plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig("residuals_plot.png", dpi=300)
print("Gráfico salvo como residuals_plot.png")
