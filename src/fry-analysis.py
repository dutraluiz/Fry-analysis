import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix

# ==================================================
# CREATE FIGURE DIRECTORY IF IT DOES NOT EXIST
# Cria a pasta Figure se não existir
# ==================================================
FIG_DIR = "Figure"
os.makedirs(FIG_DIR, exist_ok=True)

# ==================================================
# 1. DATA INPUT
# 1. Leitura dos dados
# ==================================================
# Excel file must contain columns: x, y (coordinates in meters)
# Arquivo Excel deve conter colunas: x, y (coordenadas em metros)
df = pd.read_excel("Deposits_example.xls")

pts = df[["X", "Y"]].values
n = len(pts)

print(f"Number of deposits / Número de depósitos: {n}")

# ==================================================
# 2. NEAREST NEIGHBOUR ANALYSIS (Carranza et al., 2009)
# 2. Análise do vizinho mais próximo (Carranza et al., 2009)
# ==================================================
# Distance matrix between all points
# Matriz de distâncias entre todos os pontos
Dmat = distance_matrix(pts, pts)
np.fill_diagonal(Dmat, np.inf)

# Maximum nearest-neighbour distance
# Distância máxima do vizinho mais próximo
r = np.linspace(0, Dmat[Dmat < np.inf].max(), 300)

# Cumulative probability of having ≤ 1 neighbour
# Probabilidade cumulativa de ter ≤ 1 vizinho
P_cum = []

for ri in r:
    counts = (Dmat <= ri).sum(axis=1)
    P_cum.append(np.mean(counts >= 1))

P_cum = np.array(P_cum)

# Characteristic distance: maximum slope / inflection
# (often interpreted visually, as in Carranza et al. (2009))
## This distance represents the minimum spatial scale at which most deposits cease to be spatially isolated.
## Esse valor representa a escala espacial mínima a partir da qual a maioria dos depósitos deixa de estar isolada.
grad = np.gradient(P_cum)
idx_char = np.argmax(grad)
D_char = r[idx_char]
P_char = P_cum[idx_char]

print(f"Characteristic distance (Carranza): {D_char/1000:.2f} km")

# Plot cumulative probability
# Probabilidade cumulativa
plt.figure(figsize=(6,4))
plt.plot(r / 1000, P_cum, color="black")

plt.vlines(D_char / 1000, ymin=0, ymax=P_char, color="red",
           linestyles="dashed", linewidth=1.5)
plt.scatter(D_char / 1000, P_char, color="red", s=50, zorder=5)
plt.annotate(f"D\u2095 = {D_char/1000:.1f} km", xy=(D_char / 1000, P_char),
             xytext=(D_char / 1000 + 5, P_char - 0.15),
             arrowprops=dict(arrowstyle="->", color="red"), fontsize=9)
plt.xlabel("Distance (km) from every P")
plt.ylabel("Probability of one neighbouring P")
plt.title("Nearest neighbour cumulative probability")
plt.grid(True)

plt.savefig(os.path.join(FIG_DIR, "Fig 1 - Nearest neighbor probability.png"), dpi=300, bbox_inches="tight")
plt.show()



# ==================================================
# 3. FRY POINTS
# 3. Geração dos pontos de Fry
# ==================================================
fry = []

for i in range(n):
    for j in range(n):
        if i != j:
            fry.append(pts[i] - pts[j])

fry = np.array(fry)

# Distance and azimuth of Fry points
# Distância e azimute dos pontos de Fry
dist_fry = np.sqrt(fry[:, 0]**2 + fry[:, 1]**2)

# Angle in Cartesian coordinates
# Ângulo em coordenadas cartesianas
theta = np.degrees(np.arctan2(fry[:, 1], fry[:, 0]))

# Conversion to geological azimuth (0–180°)
# Conversão para azimute geológico (0–180°)
az = (90 - theta) % 180

# ==================================================
# 4. FRY PLOT
# 4. Diagrama de Fry
# ==================================================
plt.figure(figsize=(6, 6))
plt.scatter(fry[:, 0] / 1000, fry[:, 1] / 1000, s=3, alpha=0.4)
plt.axhline(0)
plt.axvline(0)
plt.gca().set_aspect("equal")

plt.xlabel("ΔX (km)")
plt.ylabel("ΔY (km)")
plt.title("Fry plot")

plt.savefig(os.path.join(FIG_DIR, "Fig 2 - Fry plot.png"), dpi=300, bbox_inches="tight")
plt.show()

# ==================================================
# 5. ROSE DIAGRAM FUNCTION
# 5. Função para diagramas de rosa
# ==================================================
def rose_diagram(azimuths, filename, title):
    """
    Plot rose diagram from azimuth data (0–180°).
    Plota um diagrama de rosa a partir de azimutes (0–180°).
    """
    az_rad = np.deg2rad(azimuths)
    bins = np.deg2rad(np.arange(0, 190, 10))

    counts, edges = np.histogram(az_rad, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2

    fig = plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)

    ax.bar(centers, counts, width=np.diff(edges), alpha=0.7)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_thetagrids(range(0, 181, 30))
    ax.set_title(title)

    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.show()

# ==================================================
# 6. ROSE DIAGRAMS
# 6. Diagramas de rosa
# ==================================================

# All Fry point pairs
# Todos os pares de Fry points
rose_diagram(az, os.path.join(FIG_DIR, "Fig 3 - Rose diagram all Fry points.png"), "Rose diagram – all Fry points")

# Local Fry point pairs (≤ characteristic distance)
# Pares locais (≤ distância característica)
mask_local = dist_fry <= D_char

rose_diagram(az[mask_local], os.path.join(FIG_DIR, "Fig 4 - Rose diagram local Fry points.png"), f"Rose diagram – Fry points ≤ {D_char/1000:.1f} km")
