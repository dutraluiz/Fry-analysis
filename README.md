# Fry Spatial Analysis for Mineral Deposits

## 🇧🇷 Português (Análise Fry para depósitos minerais)

Este repositório apresenta uma implementação em Python da **análise de Fry**
aplicada ao estudo de **controles estruturais na distribuição espacial de depósitos minerais**.

A abordagem segue o uso moderno do método de Fry como uma técnica geométrica
de autocorrelação espacial, conforme aplicado por autores como [Carranza (2009)](https://doi.org/10.1007/s00126-009-0250-6) e [Haddad-Martim et al. (2017)(http://dx.doi.org/10.1016/j.oregeorev.2016.09.038).

### Objetivos
- Investigar direções preferenciais entre depósitos minerais
- Avaliar controles estruturais em múltiplas escalas espaciais
- Integrar análise de Fry com estatística de vizinho mais próximo

### Metodologia
1. Análise de vizinho mais próximo para determinar a distância característica
   com máxima probabilidade de apenas um vizinho.
2. Geração de Fry points (n² − n pares).
3. Análise direcional por diagramas de rosa:
   - todos os pares (escala regional)
   - pares dentro da distância característica (escala local)

### Entradas
Arquivo Excel contendo coordenadas UTM (x, y) dos depósitos.

### Saídas
- Fry plot
- Gráfico Distance × Probability of one neighbour
- Rose diagrams por escala

---

## 🇬🇧 English

This repository provides a Python implementation of **Fry analysis**
applied to the investigation of **structural controls on the spatial distribution
of mineral deposits**.

The methodology follows the modern use of the Fry method as a geometrical
spatial autocorrelation technique, as described by [Carranza (2009)](https://doi.org/10.1007/s00126-009-0250-6) and [Haddad-Martim et al. (2017)(http://dx.doi.org/10.1016/j.oregeorev.2016.09.038).

### Objectives
- Identify preferential orientations between mineral deposits
- Investigate structural controls at multiple spatial scales
- Integrate Fry analysis with nearest neighbour statistics

### Methodology
1. Nearest neighbour analysis to determine the characteristic distance
   corresponding to the maximum probability of one neighbour.
2. Generation of Fry points (n² − n pairs).
3. Directional analysis using rose diagrams:
   - all Fry points (regional scale)
   - Fry points within the characteristic distance (local scale)

### Inputs
Excel file containing UTM coordinates (x, y) of mineral deposits.

### Outputs
- Fry plot
- Distance × Probability of one neighbour plot
- Scale-dependent rose diagrams
