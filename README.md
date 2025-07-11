# US Traffic Accident Analytics (2016-2023) 🚔📈

## 📌 Overview
Analyzed 1.1 million accident records to identify temporal patterns, weather impacts, and infrastructure risk factors. This project demonstrates efficient large dataset processing and clear visual storytelling.

## 🔍 Key Insights
- **Temporal Analysis**: 
  - Peak accident hours: 4-6PM (17.2% of daily total)
  - Least safe day: Friday (15.8% of weekly accidents)
- **Environmental Factors**:
  - Top weather condition: "Fair" (412,000+ accidents)
  - 22% of accidents occur in low visibility (<5mi)
- **Infrastructure Risks**:
  - 34% of severe accidents occur near traffic signals
  - Railway crossings involved in 8% of high-severity cases

## 🛠️ Tech Stack
- **Python 3** with memory-optimized processing
- **Libraries**: Pandas (chunked processing), Seaborn, Matplotlib
- **Techniques**: Time-series decomposition, geospatial sampling


## 🚀 How to Run
1. Place `https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents` in project root
2. Install requirements:
   ```bash
   pip install pandas matplotlib seaborn
