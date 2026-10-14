# 🚚 Last Mile Delivery Performance Dashboard

An interactive Streamlit dashboard that analyses last-mile delivery data to help operations managers understand **what slows deliveries down** — weather, traffic, vehicle type, area, product category and agent performance.

Built for **LogiSight Analytics Pvt. Ltd.** as part of Formative Assessment 2 (Mathematics for AI-II).

## 🔗 Live Demo

**[Open the dashboard](https://logisightanalyticspvtltd.streamlit.app)**

## 📌 Project Overview

Last-mile delivery is the most expensive and delay-prone part of logistics. This dashboard turns a raw delivery dataset into clear, filterable visuals so a manager can quickly spot where delays happen and why.

This project builds on **FA1**, where the dashboard was designed as a storyboard and data flow. FA2 turns that design into a working, deployed application.

## 📊 Dataset

- **Records:** 43,739 deliveries
- **Key columns:** Order date, Delivery time, Weather, Traffic, Vehicle, Area, Product category, Agent age, Agent rating
- **File:** `Last_mile_Delivery_Data.csv`

## 🧹 Data Cleaning

| Issue found | How it was handled |
|---|---|
| Extra spaces in text columns (e.g. `"Jam "`) | Stripped whitespace from all text columns |
| Literal `"NaN"` text in Traffic and Weather | Converted to real missing values |
| 91 missing Weather and Traffic values | Filled with `"Unknown"` so no rows are lost |
| 54 missing Agent Rating values | Filled with the median rating |
| Order date stored as text | Converted to proper dates and extracted the month |
| Agent age is a raw number | Grouped into `<25`, `25-40` and `40+` |

After cleaning, all **43,739** rows are retained.

## ✨ Features

**Key metrics (update live with filters)**
- Total deliveries
- Average delivery time
- % late deliveries (a delivery is "late" if it takes longer than the average plus one standard deviation)
- Average agent rating

**Sidebar filters:** Weather, Traffic, Vehicle Type, Area, Product Category

**Five core visualisations**
1. **Delay Analyzer** – average delivery time by weather and by traffic (bar charts)
2. **Vehicle Comparison** – average delivery time by vehicle type (bar chart)
3. **Agent Performance** – agent rating vs delivery time, coloured by age group (scatter plot)
4. **Area Heatmap** – delivery time distribution across areas (heatmap)
5. **Category Visualizer** – delivery time spread by product category (box plot)

**Extra insights**
- Monthly trend of average delivery time
- Overall delivery time distribution with the late threshold marked
- % late deliveries by traffic condition
- Delivery volume per area

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – web app and filters
- **Pandas / NumPy** – data cleaning and analysis
- **Plotly Express** – interactive charts

## ▶️ Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/Het-thakkar/last-mile-delivery-dashboard.git
   cd last-mile-delivery-dashboard
   ```
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run app.py
   ```
4. Open `http://localhost:8501` in your browser.

## 📁 Project Structure

```
├── app.py                        # Streamlit dashboard
├── Last_mile_Delivery_Data.csv   # Dataset
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

## ⚠️ Notes and Limitations

- The dataset does not state the unit of delivery time; the dashboard treats it as minutes.
- The dashboard shows **association, not causation**. For example, longer delivery times during traffic jams do not by themselves prove that traffic is the only cause.
- Some groups are very small (for example, agents aged 40+ and the bicycle vehicle type), so their averages should be read with caution.

## 👤 Author

**Het Thakkar**
Mathematics for AI-II – Formative Assessment 2
