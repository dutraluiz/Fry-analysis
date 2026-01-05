import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
from scipy.stats import gaussian_kde

# ==================================================
# GLOBAL PLOT CONFIGURATION
# Configuração global de fontes (Arial)
# ==================================================
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False

# ==================================================
# CREATE FIGURE DIRECTORY IF IT DOES NOT EXIST
# Cria a pasta Figure se não existir
# ==================================================
FIG_DIR = 'Figure'
os.makedirs(FIG_DIR, exist_ok=True)

# ==================================================
# 1. DATA INPUT
# 1. Leitura dos dados
# ==================================================
# Excel file must contain columns: x, y (coordinates in meters)
# Arquivo Excel deve conter colunas: x, y (coordenadas em metros)
df = pd.read_excel('Deposits_example.xls')

pts = df[['X', 'Y']].values
n = len(pts)

print(f'Number of deposits / Número de depósitos: {n}')

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

# Distance where P = 1 (Total connectivity)
# Distância onde P = 1 (Conectividade total)
idx_p1 = np.where(P_cum >= 1.0)[0][0]
D_p1 = r[idx_p1]

print(f"Characteristic distance (Carranza): {D_char/1000:.2f} km")
print(f"Distance where P=1: {D_p1/1000:.2f} km")

# Plot cumulative probability
# Probabilidade cumulativa
plt.figure(figsize=(6,4))
plt.plot(r / 1000, P_cum, color="black")

# Plot Dchar (Inflection point)
# Plota Dchar (Ponto de inflexão)
plt.vlines(D_char / 1000, ymin=0, ymax=P_char, color="red",
           linestyles="dashed", linewidth=1.5, label=f"Dchar: {D_char/1000:.1f} km")
plt.scatter(D_char / 1000, P_char, color="red", s=50, zorder=5)

# Plot Dp=1 (Saturation point)
# Plota Dp=1 (Ponto de saturação)
plt.vlines(D_p1 / 1000, ymin=0, ymax=1.0, color="blue",
           linestyles="dotted", linewidth=1.5, label=f"Dp=1: {D_p1/1000:.1f} km")
plt.scatter(D_p1 / 1000, 1.0, color="blue", s=50, zorder=5)

# Annotations
# Anotações
plt.text(D_char / 1000 + 0.5, 0.05, f"$D_{{char}}$ = {D_char/1000:.1f} km", 
         color="red", fontweight="bold", fontsize=10)

plt.text(D_p1 / 1000 - 10, 0.05, f"$D_{{p1}}$ = {D_p1/1000:.1f} km", 
         color="blue", fontweight="bold", fontsize=10)

plt.xlabel("Distance (km) from every deposit")
plt.ylabel("Probability of one neighbouring deposit")
plt.title("Nearest neighbour cumulative probability")

plt.xlim(0, (D_p1 / 1000) + 5)
plt.ylim(0, 1)

#plt.legend(loc="lower right")
plt.grid(True, alpha=0.3)

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
# Definir o limite máximo para garantir eixos simétricos e iguais (escala 1:1)
max_range = max(max(abs(fry[:, 0] / 1000)), max(abs(fry[:, 1] / 1000))) * 1.05

plt.figure(figsize=(6, 6))
plt.scatter(fry[:, 0] / 1000, fry[:, 1] / 1000, s=3, color='black', alpha=0.4)
plt.axhline(0, color='black', lw=1)
plt.axvline(0, color='black', lw=1)

# Adicionar círculo de referência da Distância Característica (Dchar)
circle_char = plt.Circle((0, 0), D_char/1000, color='red', fill=False, ls='--', 
                         lw=1.5, label=f'$D_{{char}}$ ({D_char/1000:.1f} km)')
plt.gca().add_patch(circle_char)

# Adicionar círculo de referência da Distância de Conectividade Total (Dp1)
circle_p1 = plt.Circle((0, 0), D_p1/1000, color='blue', fill=False, ls=':', 
                        lw=1.5, label=f'$D_{{p1}}$ ({D_p1/1000:.1f} km)')
plt.gca().add_patch(circle_p1)

plt.gca().set_aspect('equal')
plt.xlim(-max_range, max_range)
plt.ylim(-max_range, max_range)

plt.xlabel('ΔX (km)')
plt.ylabel('ΔY (km)')
plt.title('Fry plot (Equal Scale)')
plt.legend(loc='upper right', fontsize=8)

plt.savefig(os.path.join(FIG_DIR, 'Fig 2a - Fry plot.png'), dpi=300, bbox_inches='tight')
plt.show()

# ==================================================
# 5. ENHANCED FRY PLOT WITH KDE
# 5. Diagrama de Fry com Densidade de Kernel
# ==================================================
# 1. Preparar os dados (remover possíveis NaNs ou zeros se necessário)
x = fry[:, 0] / 1000
y = fry[:, 1] / 1000

# 2. Calcular o KDE
# O 'bw_method' controla a suavização. Valores menores mostram mais detalhes.
k = gaussian_kde([x, y], bw_method=0.15)

# 3. Criar uma grade simétrica para o mapeamento baseada no max_range
xi, yi = np.mgrid[-max_range:max_range:200j, -max_range:max_range:200j]
zi = k(np.vstack([xi.flatten(), yi.flatten()]))

# 4. Plotagem
plt.figure(figsize=(8, 7))

# Fundo com a densidade
plt.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='auto', cmap='magma')
plt.colorbar(label='Density of Fry Points')

# Sobrepor os pontos originais (opcional, com alpha baixo)
plt.scatter(x, y, s=1, color='white', alpha=0.1)

# Adicionar círculos também no KDE para referência de escala
circle_char_kde = plt.Circle((0, 0), D_char/1000, color='white', fill=False, ls='--', lw=1, alpha=0.8)
circle_p1_kde = plt.Circle((0, 0), D_p1/1000, color='cyan', fill=False, ls=':', lw=1, alpha=0.8)
plt.gca().add_patch(circle_char_kde)
plt.gca().add_patch(circle_p1_kde)

plt.axhline(0, color='white', linestyle='--', linewidth=0.5)
plt.axvline(0, color='white', linestyle='--', linewidth=0.5)

plt.gca().set_aspect('equal')
plt.xlim(-max_range, max_range)
plt.ylim(-max_range, max_range)

plt.xlabel('ΔX (km)')
plt.ylabel('ΔY (km)')
plt.title('Rose-Fry Density Plot (KDE)')

plt.savefig(os.path.join(FIG_DIR, 'Fig 2b - Fry KDE Plot.png'), dpi=300, bbox_inches='tight')
plt.show()

# ==================================================
# 6. RESULT EXPORT
# 6. Exportação dos resultados
# ==================================================
import xlsxwriter

output_path = os.path.join(FIG_DIR, 'Fry_Statistical_Analysis.xls')

# 1. Create a statistical summary DataFrame
# 1. Cria um DataFrame de resumo estatístico
summary_data = pd.DataFrame({
    'Parameter': ['Number of Deposits', 'D_char (m)', 'D_p1 (m)', 'D_char (km)', 'D_p1 (km)'],
    'Value': [n, D_char, D_p1, D_char/1000, D_p1/1000]
})

# 2. Build the Fry data list with UTM coordinates
# 2. Constrói a lista de dados Fry com coordenadas UTM
fry_list = []
idx = 0
for i in range(n):
    for j in range(n):
        if i != j:
            fry_list.append({
                'Origin_X': pts[i, 0], 'Origin_Y': pts[i, 1],
                'Relative_dX': fry[idx, 0], 'Relative_dY': fry[idx, 1],
                'Fry_UTM_X': pts[i, 0] + fry[idx, 0], 'Fry_UTM_Y': pts[i, 1] + fry[idx, 1],
                'Distance_m': dist_fry[idx], 'Azimuth_deg': az[idx]
            })
            idx += 1
df_fry_final = pd.DataFrame(fry_list)

# 3. Export data
# 3. Exporta dados
with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
    # Write data to different sheets
    # Escreve os dados em abas diferentes
    summary_data.to_excel(writer, sheet_name='Summary', index=False)
    df_fry_final.to_excel(writer, sheet_name='Fry_Data', index=False)
    
    workbook = writer.book

    # Format
    # Formatação
    fmt_arial10 = workbook.add_format({'font_name': 'Arial', 'font_size': 10})
    fmt_header = workbook.add_format({'font_name': 'Arial', 'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
    
    for sheet in ['Summary', 'Fry_Data']:
        ws = writer.sheets[sheet]
        ws.set_column('A:Z', 18, fmt_arial10)
        
        cols = summary_data.columns if sheet == 'Summary' else df_fry_final.columns
        for col_num, value in enumerate(cols):
            ws.write(0, col_num, value, fmt_header)

print(f"Full report exported successfully to: {output_path}")
# Relatório completo exportado com sucesso para:...

# ==================================================
# 7. ROSE DIAGRAM FUNCTION
# 7. Função para o estereograma
# ==================================================
def rose_diagram(azimuths, filename, title):
    # Duplicate the data to create 360-degree symmetry (geological pattern)
    # Duplicar os dados para criar a simetria de 360 graus (padrão geológico)
        az_full = np.concatenate([azimuths, azimuths + 180])
        az_rad = np.deg2rad(az_full)
    
    # 36 bins to cover 360 degrees (10 degrees each)
    # 36 bins para cobrir 360 graus (10 graus cada)
        bins = np.linspace(0, 2 * np.pi, 37)

        counts, edges = np.histogram(az_rad, bins=bins)
        centers = (edges[:-1] + edges[1:]) / 2

        fig = plt.figure(figsize=(6, 6))
        ax = plt.subplot(111, polar=True)

        ax.bar(centers, counts, width=np.diff(edges), color='skyblue', edgecolor='black', alpha=0.7)
        
        ax.set_theta_zero_location('N')  # North at the top | Norte no topo
        ax.set_theta_direction(-1)       # Clockwise | Sentido horário
        ax.set_thetagrids(range(0, 360, 30))
        ax.set_title(title, pad=20)

        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()

# ==================================================
# 8. ROSE DIAGRAMS
# 8. Estereograma
# ==================================================

# All Fry point pairs
# Todos os pares de Fry points (Escala Regional)
rose_diagram(az, os.path.join(FIG_DIR, "Fig 3 - Rose diagram all Fry points.png"), 
             "Rose diagram – all Fry points")

# Local Fry point pairs (≤ characteristic distance)
# Pares locais (≤ distância característica)
mask_char = dist_fry <= D_char
rose_diagram(az[mask_char], os.path.join(FIG_DIR, "Fig 4 - Rose diagram Dchar.png"), 
             f"Rose diagram – Fry points ≤ Dchar ({D_char/1000:.1f} km)")

# Fry point pairs within total connectivity distance (≤ Dp=1)
# Pares dentro da distância de conectividade total (≤ Dp=1)
mask_p1 = dist_fry <= D_p1
rose_diagram(az[mask_p1], os.path.join(FIG_DIR, "Fig 5 - Rose diagram Dp1.png"), 
             f"Rose diagram – Fry points ≤ Dp1 ({D_p1/1000:.1f} km)")
