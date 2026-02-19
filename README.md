# PFA Dashboard

A dark-themed interactive dashboard built with [Dash](https://dash.plotly.com/) for visualizing Portfolio Factor Analysis results. Switch between views via a dropdown — no page reloads, no clutter.

---

## Views

**Principal Component Analysis**
Displays cumulative explained variance as a bar chart and the top 3 principal components as line plots across assets.

**Risk Analysis**
Shows the covariance matrix as a heatmap and individual asset standard deviations as a bar chart.

---

## Preview

<img src="resources/PFA_PC.jpg" width="600" height="800"/>
<img src="resources/PFA_Risk.jpg" width="600" height="800"/>

---

## Setup

Install dependencies:

```bash
pip install dash plotly pandas numpy
```

Wire up your data source at the top of `pfa_dashboard.py`:

```python
from your_module import PFA

file_path = "your_data.csv"
pfa = PFA(file_path)
```

Then inside the callback, replace the dummy data blocks with:

```python
pc   = pfa.pc_analysis()
risk = pfa.risk_analysis()
```

Run the app:

```bash
python pfa_dashboard.py
```

Open [http://localhost:8050](http://localhost:8050) in your browser.

---

## Project Structure

```
├── pfa_dashboard.py   # Main Dash app
└── README.md
```
