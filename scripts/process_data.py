import os
from typing import Tuple
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from tabulate import tabulate

# Determining the project root
PROJECT_ROOT = Path(__file__).resolve().parents[1] if "__file__" in globals() else Path.cwd().parents[0]

# Input Path
DATA_PATH = PROJECT_ROOT / "data/raw/Calgary_Transit_Ridership.csv"

# Output Paths
REPORT_PATH = PROJECT_ROOT / "reports/data_processing_report.md"
PLOTS_PATH = PROJECT_ROOT / "visualizations/"

def bar_plot(data: pd.Series, title: str, xlabel: str, ylabel: str, rotation: int = 0) -> None:
    """
    Generate a bar plot.

    Args:
        data (pd.Series): The data to plot.
        title (str): The title of the plot.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
        rotation (int): The rotation of the x-axis
    Returns:
        None
    """
    # Use seaborn to plot the bar plot
    plt.figure(figsize=(15, 6))
    sns.barplot(x=data.index, y=data.values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Add the count values on top of the bars
    for i, value in enumerate(data.values):
        if value != 0:
            plt.text(i, value, str(value), ha="center", va="bottom")
    plt.xticks(rotation=rotation)

    # Save the plot
    plt.tight_layout()
    plt.savefig(PLOTS_PATH / f"{title.lower().replace(' ', '_')}.png")

def plot_annotated_heatmap(data: pd.DataFrame, title: str, xlabel: str, ylabel: str, rotation: int = 0) -> None:
    """
    Generate and save an annotated heatmap.
    Args:
        data (pd.DataFrame): The data to plot.
        title (str): The title of the plot.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
        rotation (int): The rotation of the x-axis
    Returns:
        None
    """

    # Create the heatmap
    plt.figure(figsize=(15, 6))
    ax = sns.heatmap(data, annot=True, fmt="d", cmap="coolwarm", cbar=False, linewidths=0.5)
    plt.title(title, fontsize=14, fontweight="bold")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation, ha="right", fontsize=10)

    # Save the plot
    plt.tight_layout()
    plt.savefig(PLOTS_PATH / f"{title.lower().replace(' ', '_')}.png")
    plt.close()

def generate_report(project_dataframe: pd.DataFrame, validation_df: pd.DataFrame, duplicate_count: int) -> None:
    """
    Generate a markdown report for the data validation.

    Args:
        project_dataframe (pd.DataFrame): The dataframe containing the project data.
        missing_values (pd.Series): Series containing the count of missing values per column.
        negative_values (pd.Series): Series containing the count of negative values per column.
        zero_values (pd.Series): Series containing the count of zero values per column.
        duplicate_count (int): The count of duplicate rows in the project dataframe.
    Returns:
        None
    """

    # Convert DataFrame to Markdown table
    validation_table = tabulate(validation_df, headers="keys", tablefmt="github", showindex=False)

    # Generate Markdown Report
    markdown_report = f"""# Data Processing Report  
**Dataset:** {DATA_PATH.name}  
**Total Rows:** {project_dataframe.shape[0]}  
**Total Columns:** {project_dataframe.shape[1]}  

## Summary Table
| Validation Check      | Value |
|----------------------|------:|
| **Total Duplicate Rows** | {duplicate_count} |

## Validation Details
{validation_table}

## Visualizations

### Missing Values Plots
The missing values are mostly before 2021, with "Weekend Group Pass Ridership" (158) and "Low Income Monthly Pass Ridership" (132) being the most affected. Some columns show 12 missing values per year, suggesting systematic gaps.
![Missing Values Heatmap](../visualizations/missing_values_per_column_per_year.png)
![Missing Values Bar Plot](../visualizations/missing_values_per_column.png)

### Zero Values Plots
Zero values are concentrated in "Airport BRT Ridership - Total Trips" (16), "Seniors Regular Pass Ridership" (12), and "Youth Book of Tickets Ridership" (9), suggesting periods of no reported ridership, possibly due to service suspensions or low demand. The majority of zero values appear in recent years (2020-2024), likely due to pandemic-related impacts or reporting gaps.
![Zero Values Heatmap](../visualizations/zero_values_per_column_per_year.png)
![Zero Values Bar Plot](../visualizations/zero_values_per_column.png)

### Negative Values Heatmap
Negative values are rare but found mainly in "Youth Day Pass Ridership" (10), "Youth Book of Tickets Ridership" (9), and "Adult Day Pass Ridership" (2). These may indicate data entry errors or adjustments. Most negative values appear before 2021, with a few scattered cases in later years, suggesting inconsistencies in earlier data collection
![Negative Values Heatmap](../visualizations/negative_values_per_column_per_year.png)
![Negative Values Bar Plot](../visualizations/negative_values_per_column.png)

## Data Cleaning Strategy
To ensure the **ridership data** is clean and ready for analysis, four key checks were performed:
1. **Duplicates:** There were {duplicate_count} duplicate rows in the dataset.
2. **Missing Values:**
    - The columns **`Airport BRT Ridership`** and **`Weekend Group Pass Ridership`** had missing values in almost all rows and were **removed** as they contribute minimally to ridership trends.
    - **Removing data from 2010 to 2014** significantly reduced missing values while keeping the analysis focused on recent trends.
    - Columns with only **one missing value** were **imputed using the mean ridership for the same month in previous years**, ensuring continuity in data.
3. **Zero Values:**
    - **`U-Pass Ridership`** had **zero values during the COVID-19 pandemic** due to university closures. These are **retained**, as they reflect real-world impacts.
    - **`Youth Cash-Single Ticket Ride Ridership`** had **zero values in 2014**, but since it contributes minimally to overall ridership, these are **ignored**.
4. **Negative Values:**
    - Since we do **not have access to SMEs**, these values cannot be **confirmed or corrected based on domain knowledge**.
    - Only **three columns** contained negative values, as shown in the **visualizations**.
    - These columns **contributed minimally** to total ridership each year.
    - **Dropping these columns** is a reasonable choice to ensure data integrity.

The processed dataset is available at [this link](../data/processed/Calgary_Transit_Ridership_Processed.csv).
    """

    # Save the report as a Markdown file
    REPORT_PATH.write_text(markdown_report)
    print(f"Validation report saved to: {REPORT_PATH}")

def visualize_data(missing_values: pd.Series, negative_values: pd.Series, zero_values: pd.Series) -> None:
    """
    Visualize the data using various plots.
    Args:
        missing_values (pd.Series): Series containing the count of missing values per column.
        negative_values (pd.Series): Series containing the count of negative values per column.
        zero_values (pd.Series): Series containing the count of zero values per column.
    Returns:
        None
    """

    # Generate heatmaps
    plot_annotated_heatmap(missing_values, "Missing Values per Column per Year", "Column Name", "Year", rotation=45)
    plot_annotated_heatmap(zero_values, "Zero Values per Column per Year", "Column Name", "Year", rotation=45)
    plot_annotated_heatmap(negative_values, "Negative Values per Column per Year", "Column Name", "Year", rotation=45)

    total_missing_values = missing_values.sum()
    total_negative_values = negative_values.sum()
    total_zero_values = zero_values.sum()

    # Combine all checks into a single DataFrame
    validation_df = pd.DataFrame({
        "Column Name": project_dataframe.columns,
        "Missing Values": [total_missing_values.get(col, 0) for col in project_dataframe.columns],
        "Negative Values": [total_negative_values.get(col, 0) for col in project_dataframe.columns],
        "Zero Values": [total_zero_values.get(col, 0) for col in project_dataframe.columns]
    })

    # Generate bar plots
    bar_plot(total_missing_values, "Missing Values Per Column", "Column Name", "Count", rotation=90)
    bar_plot(total_negative_values, "Negative Values Per Column", "Column Name", "Count", rotation=90)
    bar_plot(total_zero_values, "Zero Values Per Column", "Column Name", "Count", rotation=90)

    return validation_df

def prepare_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Prepare the data for analysis by validating the data and generating a report.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: 
        - project_dataframe: The original DataFrame loaded from the CSV file.
        - validation_df: A DataFrame containing the results of various data validation checks.
        - duplicate_count: The count of duplicate rows in the original DataFrame.
    """
    # Load the data
    project_dataframe = pd.read_csv(DATA_PATH)
    
    # Data Validation Checks
    # Extract the dataframe with the numeric columns
    numeric_df = project_dataframe.select_dtypes(include=["number"])

    # Duplicates
    duplicate_count = project_dataframe.duplicated().sum()

    # Missing Values
    missing_values = project_dataframe.groupby('Year')[numeric_df.columns].apply(lambda x: x.isnull().sum())

    # Negative Values
    negative_values = project_dataframe.groupby('Year')[numeric_df.columns].apply(lambda x: (x < 0).sum())
    """ Checking the zero values separately as they are not wrong to be 
    present in the data but they can be a cause of concern in some cases """
    zero_values = project_dataframe.groupby('Year')[numeric_df.columns].apply(lambda x: (x == 0).sum())

    return project_dataframe, missing_values, negative_values, zero_values, duplicate_count

def process_data(project_dataframe: pd.DataFrame) -> None:
    
    # Remove data from 2010 to 2014
    project_dataframe = project_dataframe[project_dataframe["Year"] > 2014]

    # Remove unnecessary columns with excessive missing values and negative values
    project_dataframe.drop(columns=["Airport BRT Ridership", "Weekend Group Pass Ridership", "Youth Day Pass Ridership", "Youth Book of Tickets Ridership"], inplace=True, errors='ignore')

    columns_with_missing_values = project_dataframe.columns[project_dataframe.isnull().sum() == 1]
    # get the month of the missing values in the columns
    missing_month = project_dataframe[columns_with_missing_values].isnull().idxmax()
    for col in columns_with_missing_values:
        month = project_dataframe.loc[missing_month[col], "Month"]
        project_dataframe.loc[missing_month[col], col] = project_dataframe[project_dataframe["Month"] == month][col].mean()
    
    # Save the processed data
    processed_data_path = PROJECT_ROOT / "data/processed/Calgary_Transit_Ridership_Processed.csv"
    project_dataframe.to_csv(processed_data_path, index=False)
    print(f"Processed data saved to: {processed_data_path}")

if __name__ == "__main__":
    project_dataframe, missing_values, negative_values, zero_values, duplicate_count = prepare_data()
    validation_data = visualize_data(missing_values, negative_values, zero_values)
    generate_report(project_dataframe, validation_data, duplicate_count)
    process_data(project_dataframe)
    