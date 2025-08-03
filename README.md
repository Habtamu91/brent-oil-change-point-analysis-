# 📈 Brent Oil Change Point Analysis

**Interim Report Submission – Week 10 Challenge**  
**Author:** Habtamu Belay Tessema 
**Affiliation:** 10 Academy – Birhan Energies  
**Submission Date:** August 2, 2025  
**GitHub Repository:** [https://github.com/Habtamu91/brent-oil-change-point-analysis]

---

## 🔍 Project Overview

This project aims to analyze historical Brent crude oil prices and identify **significant structural changes** in the time series using **Bayesian Change Point Detection**. The goal is to **quantify the impact of major geopolitical, economic, and OPEC-related events** on Brent oil price behavior over the past three decades.

The analysis supports stakeholders such as **investors**, **policy makers**, and **energy companies** by providing data-driven insights into market volatility and change patterns.

---

## 🎯 Business Objective

> To detect **key change points** in Brent oil prices from 1987 to 2022 and **associate them with real-world events**, such as wars, policy shifts, economic crises, or global pandemics, using statistical modeling (PyMC3).

---

## 🧪 Planned Workflow

### 📁 1. Data Collection & Preparation
- Load Brent oil prices from May 1987 to Sept 2022
- Manually compile 10–15 historical events relevant to oil prices
- Convert dates, clean nulls, format for modeling

### 📊 2. Exploratory Data Analysis (EDA)
- Visualize time series trends and price volatility
- Perform stationarity checks (e.g., ADF test)
- Transform prices into **log returns** to stabilize variance

### 🧠 3. Bayesian Change Point Modeling
- Apply PyMC3 model to detect structural breaks
- Model price shifts in mean or variance
- Estimate posterior distributions for change points

### 🧩 4. Event Correlation
- Match change points with historical events
- Quantify impact (e.g., “price jumped from $X to $Y”)
- Discuss limitations and potential confounders

### 💻 5. Dashboard (Planned for Final Submission)
- Flask backend + React frontend to visualize:
  - Price trends
  - Detected change points
  - Historical events overlay

---

## 📅 Events Dataset (Preview)
  
                 
Event_date    Event_name         Description
1990-08-02   | Conflict      | Iraq invades Kuwait                          |
| 2001-09-11 | Terrorism     | 9/11 attacks in the US                       |
| 2008-09-15 | Economic      | Lehman collapse, global financial crisis     |
| 2020-03-11 | Pandemic      | COVID-19 declared global pandemic            |
| 2022-02-24 | War           | Russia invades Ukraine                       |

Full list: [`data/raw/events.csv`](data/raw/events.csv)

---

## ⚖️ Assumptions & Limitations

- Change point ≠ causality; analysis focuses on **temporal correlation**
- Lagged impacts of events are not deeply modeled (yet)
- No macroeconomic variables (e.g., GDP, inflation) included at this stage

---

## ✅ Interim Deliverables

- `01_eda.ipynb` – Initial time series analysis
- `events.csv` – Structured geopolitical/economic event dataset
- `README.md` – Workflow plan and business alignment

Final submission will include:
- Full PyMC3 model
- Insight quantification
- Flask + React dashboard
- Final report or blog post

---
