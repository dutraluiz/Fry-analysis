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
df = pd.read_excel("Deposits_example.xlsx")

pts = df[["X", "Y"]].values
n = len(pts)

print(f"Number of deposits / Número de depósitos: {n}")

# ==================================================
# 2. NEAREST NEIGHBOUR ANALYSIS
# 2. Análise do vizinho mais próximo
# ==================================================
# Distance matrix between all points
# Matriz de distâncias entre todos os pontos
Dmat = distance_matrix(pts, pts)
np.fill_diagonal(Dmat, np.inf)

# Nearest neighbour distance for each point
# Distância do vizinho mais próximo para cada ponto
nn_dist = Dmat.min(axis=1)

# Distance range
# Intervalo de distâncias
r = np.linspace(0, nn_dist.max(), 200)

# Probability of only one neighbour within distance r
# Probabilidade de apenas um vizinho dentro da distância r
P1 = []

for ri in r:
    counts = (Dmat <= ri).sum(axis=1)
    P1.append(np.mean(counts == 1))

P1 = np.array(P1)

# Plot: Distance vs Probability
# Gráfico: Distância vs Probabilidade
plt.figure(figsize=(6, 4))
plt.plot(r / 1000, P1)
plt.xlabel("Distance (km)")
plt.ylabel("Probability of one neighbour")
plt.title("Nearest neighbour probability")
plt.grid(True)

plt.savefig(os.path.join(FIG_DIR, "Fig 1 - Nearest neighbor probability.png"), dpi=300, bbox_inches="tight")
plt.show()

# Characteristic distance (maximum probability of one neighbour)
# Distância característica (máxima probabilidade de um vizinho)
D_char = r[np.argmax(P1)]
print(f"Characteristic distance / Distância característica: {D_char/1000:.2f} km")

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

rose_diagram(az[mask_local], os.path.join(FIG_DIR, "Fig 4 - Rose diagram local Fry points.png"), f"Rose diagram – Fry points ≤ {D_char/1000:.1f} km"D)
