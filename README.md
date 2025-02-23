# Calgary Transit Ridership Analysis

## Overview
This project analyzes Calgary Transit ridership trends over multiple years to uncover **seasonal variations, yearly fluctuations, and fare-type usage patterns**. The goal is to provide actionable insights to Calgary Transit Authority and city planners to improve service efficiency, optimize schedules, and enhance commuter experience. This project is part of the Google Data Analytics Capstone.

### Business Task
- Investigate **Calgary Transit ridership patterns** over time.  
- Identify seasonal trends and **yearly fluctuations** in ridership.  
- Analyze the **impact of fare categories** on overall transit use.  
- Provide **data-driven recommendations** for service planning.

### Key Stakeholders  
- **Calgary Transit Authority** → Optimize transit services and fare pricing.  
- **City Planners** → Use data for future transit infrastructure improvements.  
- **Commuters** → Understand long-term ridership trends.  
---
## Data Sources

- **Name:** Calgary Transit Ridership Data  
- **Source:** [City of Calgary Open Data Portal](https://data.calgary.ca/Transportation-Transit/Calgary-Transit-Ridership/iema-jbc4)  
- **Format:** CSV
- **Dataset Info**: Dataset contains **178 rows** and **27 columns**
- **Timeframe:** Multi-year dataset with **monthly ridership counts**  
- **Variables:** Year, Month, Ridership by fare type, Transit mode, Special passes  
- **License:** Open Data Terms of Use ([See Terms](https://data.calgary.ca/stories/s/Open-Calgary-Terms-of-Use/u45n-7awa/))

---
## Establish Metrics  
- **Monthly & Yearly Ridership Trends** (overall growth or decline)  
- **Seasonal Variations** (summer vs. winter ridership patterns)  
- **Fare Category Analysis** (U-Pass, Adult, Youth, Senior ridership trends)  
- **Event-Based Ridership Impact** (if major events cause spikes in transit use)  
---

## Environment Setup
To ensure a consistent development environment, we use **Conda** for dependency management.

### **Creating the Conda Environment**
```bash
conda env create -f environment.yaml
conda activate calgary-ridership
```

To verify installed packages and versions:
```bash
conda list
```

If new dependencies are added to `environment.yaml`, update your environment with:
```bash
conda env update --file environment.yaml
```

If you need to delete the environment:
```bash
conda env remove --name calgary-ridership
```

## Processing Steps

To ensure data integrity, a **cleaning process** was applied before analysis. The following steps were taken:

1. **Handling Missing Values:**
   - **`Airport BRT Ridership`** and **`Weekend Group Pass Ridership`** were **dropped** due to excessive missing data.
   - Data from **2010-2014** was removed, reducing missing values significantly.
   - Columns with **only one missing value** were **imputed** using the **mean ridership for the same month in previous years**.

2. **Handling Zero Values:**
   - **`U-Pass Ridership`** had **zero values** during the **COVID-19 pandemic** (due to university closures) and was **kept** to reflect real-world impacts.
   - **`Youth Cash-Single Ticket Ride Ridership`** had **zero values in 2014**, but it was **ignored** due to minimal impact.

3. **Handling Negative Values:**
   - Since we **lack access to SMEs**, negative values cannot be confirmed.
   - Only **two columns** had negative values (after removing the 2010-2014 years), and they contributed **minimally** to overall ridership.
   - These columns were **dropped** from the dataset to maintain accuracy.  (**`Youth Day Pass Ridership`**, **`Youth Book of Tickets Ridership`**)

For a **detailed breakdown of data validation and cleaning**, see the **[full report](reports//data_processing_report.md)**.
