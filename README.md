# Fry Spatial Analysis for Mineral Deposits

*English version below*

## 🇧🇷 Português (Análise Fry para depósitos minerais)

Este repositório apresenta uma implementação avançada em Python da **análise de Fry** aplicada ao estudo de **controles estruturais na distribuição espacial de depósitos minerais**.

A abordagem integra o método de Fry como uma técnica geométrica de autocorrelação espacial com ferramentas estatísticas modernas, conforme discutido por [Carranza (2009)](https://doi.org/10.1007/s00126-009-0250-6) e [Haddad-Martim et al. (2017)](http://dx.doi.org/10.1016/j.oregeorev.2016.09.038).

### 🚀 Objetivos
- Investigar direções preferenciais entre depósitos minerais usando Densidade de Kernel (KDE).
- Avaliar controles estruturais em múltiplas escalas espaciais ($D_{char}$ e $D_{p1}$).
- Integrar análise de Fry com estatística de vizinho mais próximo e exportação de dados UTM.

### 📊 Metodologia
1. Análise de vizinho mais próximo para determinar a **distância característica** ($D_{char}$) e a **distância de conectividade total** ($D_{p1}$).
2. Geração de Fry points ($n^2 − n$ pares) com cálculo de azimutes geológicos.
3. Análise de densidade via **KDE (Kernel Density Estimation)** para destacar lineamentos.
4. Análise direcional por diagramas de rosa em três escalas:
   - Todos os pares (Escala Regional).
   - Pares dentro da distância característica (Escala Local - Clusters).
   - Pares dentro da distância de conectividade total (Escala Intermediária).

### 📁 Entradas
Arquivo Excel contendo coordenadas UTM (X, Y) dos depósitos em metros.

### 📁 Saídas
Os resultados são salvos automaticamente na pasta `/Figure`:
* `Fig 1`: Gráfico de Probabilidade Acumulada ($D_{char}$ & $D_{p1}$).
* `Fig 2a/2b`: Diagrama Fry  simples e com densidade de Kernel (KDE).
* `Fig 3, 4 & 5`: Estereogramas comparativos por escala.
* `Fry_Statistical_Analysis.xls`: Relatório completo contendo:
    * **Aba Summary**: Resumo estatístico incluindo os valores de $D_{char}$ e $D_{p1}$ em metros e quilômetros.
    * **Aba Fry_Data**: Lista detalhada de todos os pares de pontos com:
        * Coordenadas UTM de origem e destino (X, Y).
        * Distâncias relativas ($\Delta X, \Delta Y$).
        * Distância absoluta (m) e Azimute Geológico (0-180°).

## 💻 Requisitos

```bash
pip install numpy pandas matplotlib scipy xlsxwriter openpyxl
```
---

## 🇨🇦 English

This repository provides an advanced Python implementation of **Fry analysis** applied to the investigation of **structural controls on the spatial distribution of mineral deposits**.

The methodology follows the modern use of the Fry method as a geometrical spatial autocorrelation technique, integrated with density estimation as described by [Carranza (2009)](https://doi.org/10.1007/s00126-009-0250-6) and [Haddad-Martim et al. (2017)](http://dx.doi.org/10.1016/j.oregeorev.2016.09.038).

### 🚀 Objectives
- Identify preferential orientations between mineral deposits using Kernel Density Estimation (KDE).
- Investigate structural controls at multiple spatial scales ($D_{char}$ and $D_{p1}$).
- Integrate Fry analysis with nearest neighbour statistics and UTM data export.

### 📊 Methodology
1. Nearest neighbour analysis to determine the **characteristic distance** ($D_{char}$) and **total connectivity distance** ($D_{p1}$).
2. Generation of Fry points ($n^2 − n$ pairs) with geological azimuth calculations.
3. Density analysis via **KDE (Kernel Density Estimation)** to highlight structural trends.
4. Directional analysis using rose diagrams across three scales:
   - All Fry points (Regional Scale).
   - Points within the characteristic distance (Local Scale - Clusters).
   - Points within the total connectivity distance (Intermediate Scale).

### 📁 Inputs
Excel file containing UTM coordinates (X, Y) of mineral deposits in meters.

### 📁 Outputs
The results are automatically saved in the `/Figure` directory:
* `Fig 1`: Cumulative Probability Plot ($D_{char}$ & $D_{p1}$).
* `Fig 2a/2b`: Simple Fry Plot and Fry Plot with Kernel Density Estimation (KDE).
* `Fig 3, 4 & 5`: Scale-dependent comparative Rose Diagrams.
* `Fry_Statistical_Analysis.xls`: Complete formatted report containing:
    * **Summary Tab**: Statistical results including $D_{char}$ and $D_{p1}$ values in meters and kilometers.
    * **Fry_Data Tab**: Comprehensive list of all point pairs with:
        * Source and Target UTM coordinates (X, Y).
        * Relative distances ($\Delta X, \Delta Y$).
        * Absolute distance (m) and Geological Azimuth (0-180°).

## 💻 Requirements

```bash
pip install numpy pandas matplotlib scipy xlsxwriter openpyxl
```
